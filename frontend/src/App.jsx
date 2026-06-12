import { useState } from "react";
import axios from "axios";

import InterviewForm from "./components/InterviewForm";
import QuestionBox from "./components/QuestionBox";
import ReportBox from "./components/ReportBox";

function App() {

    // Stores interview id
    const [interviewId, setInterviewId] = useState("");

    // Stores current question
    const [question, setQuestion] = useState("");

    // Stores score
    const [score, setScore] = useState("");

    // Stores feedback
    const [feedback, setFeedback] = useState("");

    // Stores final report
    const [report, setReport] = useState(null);


    //-----------------------------------------
    // Start Interview
    //-----------------------------------------
    const startInterview = async (data) => {

        try {

            const response = await axios.post(
                "https://genai-interview-assistant.onrender.com/start-interview",
                data
            );

            setInterviewId(response.data.interview_id);

            setQuestion(response.data.question);

        }

        catch (error) {

            console.log(error);

            alert("Failed to start interview");

        }

    };


    //-----------------------------------------
    // Submit Answer
    //-----------------------------------------
    const submitAnswer = async (data) => {

        try {

            const response = await axios.post(
                "https://genai-interview-assistant.onrender.com/submit-answer",
                data
            );

            setScore(response.data.score);

            setFeedback(response.data.feedback);

            setQuestion(response.data.next_question);

        }

        catch (error) {

            console.log(error);

            alert("Failed to submit answer");

        }

    };


    //-----------------------------------------
    // Get Final Report
    //-----------------------------------------
    const getReport = async () => {

        try {

            const response = await axios.get(
                `https://genai-interview-assistant.onrender.com/report/${interviewId}`
            );

            setReport(response.data);

        }

        catch (error) {

            console.log(error);

            alert("Failed to generate report");

        }

    };


    //-----------------------------------------
    // Download Report
    //-----------------------------------------
    const downloadReport = () => {

        try {

            window.open(

                `https://genai-interview-assistant.onrender.com/download-report/${interviewId}`,

                "_blank"

            );

        }

        catch (error) {

            console.log(error);

            alert("Failed to download report");

        }

    };


    //-----------------------------------------
    // UI
    //-----------------------------------------
    return (

        <div>

            <h1>AI Interview Assistant</h1>

            <hr />

            <InterviewForm
                onStart={startInterview}
            />

            <hr />

            {

                question &&

                <QuestionBox

                    question={question}

                    interviewId={interviewId}

                    onSubmitAnswer={submitAnswer}

                />

            }

            <br />

            {

                score !== "" &&

                <>

                    <h2>Score</h2>

                    <p>{score}</p>

                    <h2>Feedback</h2>

                    <p>{feedback}</p>

                </>

            }

            <br />

            {

                interviewId &&

                <button
                    onClick={getReport}
                >

                    Get Final Report

                </button>

            }

            <br />
            <br />

            <ReportBox report={report} />

            <br />

            {

                report &&

                <button
                    onClick={downloadReport}
                >

                    Download Report

                </button>

            }

        </div>

    );

}

export default App;