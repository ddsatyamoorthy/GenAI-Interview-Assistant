import { useState } from "react";

function QuestionBox({
    question,
    interviewId,
    onSubmitAnswer
}) {

    const [answer, setAnswer] = useState("");

    const handleSubmit = () => {

        onSubmitAnswer({
            interview_id: interviewId,
            question: question,
            answer: answer
        });

        setAnswer("");

    };

    return (

        <div>

            <h2>Question</h2>

            <p>{question}</p>

            <textarea
                rows="5"
                cols="50"
                value={answer}
                onChange={(e)=>setAnswer(e.target.value)}
            />

            <br /><br />

            <button onClick={handleSubmit}>
                Submit Answer
            </button>

        </div>

    );
}

export default QuestionBox;