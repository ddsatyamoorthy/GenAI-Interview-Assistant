from pydantic import BaseModel


class StartInterviewRequest(BaseModel):
    candidate_name: str
    job_role: str
    experience_level: str
    
class StartInterviewResponse(BaseModel):
    interview_id: str
    question: str

class SubmitAnswerRequest(BaseModel):
    interview_id: str
    question: str
    answer: str

class SubmitAnswerResponse(BaseModel):
    score: float
    feedback: str
    next_question: str

class ReportResponse(BaseModel):
    candidate_name: str
    job_role: str
    overall_score: float
    strengths: list
    improvement_areas: list
    summary: str