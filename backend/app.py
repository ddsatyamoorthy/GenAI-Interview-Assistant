from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from database import engine
import pandas as pd
from fastapi.responses import FileResponse
from schemas import StartInterviewRequest, SubmitAnswerRequest
from gemini_service import generate_question, evaluate_answer
from database import SessionLocal
import models
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://https://gen-ai-interview-assistant.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


# -----------------------------------
# Start Interview
# -----------------------------------
@app.post("/start-interview")
def start_interview(request: StartInterviewRequest):

    db = SessionLocal()

    try:
        interview_id = str(uuid.uuid4())

        question = generate_question(
            request.job_role,
            request.experience_level
        )

        new_interview = models.Interview(
            id=interview_id,
            candidate_name=request.candidate_name,
            job_role=request.job_role,
            experience_level=request.experience_level
        )

        db.add(new_interview)
        db.commit()

        return {
            "interview_id": interview_id,
            "question": question
        }

    finally:
        db.close()


# -----------------------------------
# Submit Answer
# -----------------------------------
@app.post("/submit-answer")
def submit_answer(request: SubmitAnswerRequest):

    db = SessionLocal()

    try:

        interview = db.query(
            models.Interview
        ).filter(
            models.Interview.id == request.interview_id
        ).first()

        if not interview:
            raise HTTPException(
                status_code=404,
                detail="Interview not found"
            )

        # Evaluate answer
        result = evaluate_answer(
            request.question,
            request.answer
        )

        # Save conversation history
        history = models.ConversationHistory(
            interview_id=request.interview_id,
            question=request.question,
            answer=request.answer,
            score=result["score"],
            feedback=result["feedback"]
        )

        db.add(history)
        db.commit()

        # Generate next question
        next_question = generate_question(
            interview.job_role,
            interview.experience_level
        )

        return {
            "score": result["score"],
            "feedback": result["feedback"],
            "next_question": next_question
        }

    finally:
        db.close()


# -----------------------------------
# Generate Report
# -----------------------------------
@app.get("/report/{interview_id}")
def get_report(interview_id: str):

    db = SessionLocal()

    interview = (
        db.query(models.Interview)
        .filter(models.Interview.id == interview_id)
        .first()
    )

    history = (
        db.query(models.ConversationHistory)
        .filter(
            models.ConversationHistory.interview_id == interview_id
        )
        .all()
    )

    scores = [item.score for item in history]

    overall_score = round(
        sum(scores)/len(scores),
        2
    )

    strengths = []

    if overall_score >= 8:

        strengths = [
            "Strong technical understanding",
            "Good communication"
        ]

        improvements = [
            "Add more real-world examples"
        ]

        summary = (
            "Candidate performed very well."
        )

    elif overall_score >= 5:

        strengths = [
            "Basic understanding"
        ]

        improvements = [
            "Need more project experience",
            "Improve technical depth"
        ]

        summary = (
            "Candidate has moderate knowledge."
        )

    else:

        strengths = [
            "Shows willingness to learn"
        ]

        improvements = [
            "Need stronger fundamentals",
            "Need more practical exposure"
        ]

        summary = (
            "Candidate requires additional preparation."
        )

    return {

        "candidate_name":
            interview.candidate_name,

        "job_role":
            interview.job_role,

        "overall_score":
            overall_score,

        "strengths":
            strengths,

        "improvement_areas":
            improvements,

        "summary":
            summary

    }
        
@app.get("/download-report/{interview_id}")
def download_report(interview_id: str):

    db = SessionLocal()

    interview = (
        db.query(models.Interview)
        .filter(models.Interview.id == interview_id)
        .first()
    )

    history = (
        db.query(models.ConversationHistory)
        .filter(
            models.ConversationHistory.interview_id == interview_id
        )
        .all()
    )

    scores = [item.score for item in history]

    overall_score = round(
        sum(scores)/len(scores),2
    )


    rows = []

    for item in history:

        rows.append({

            "Question": item.question,
            "Answer": item.answer,
            "Score": item.score,
            "Feedback": item.feedback

        })


    df = pd.DataFrame(rows)


    # Add summary row
    df.loc[len(df)] = [
        "",
        "",
        overall_score,
        "Overall Score"
    ]


    filename = f"{interview.candidate_name}_report.csv"

    df.to_csv(
        filename,
        index=False
    )

    return FileResponse(

        filename,

        media_type="text/csv",

        filename=filename

    )