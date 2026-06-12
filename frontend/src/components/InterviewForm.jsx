import { useState } from "react";

function InterviewForm({ onStart }) {

    const [candidateName, setCandidateName] = useState("");
    const [jobRole, setJobRole] = useState("");
    const [experienceLevel, setExperienceLevel] = useState("");

    const handleSubmit = () => {

        onStart({
            candidate_name: candidateName,
            job_role: jobRole,
            experience_level: experienceLevel
        });

    };

    return (
        <div>

            <h2>Start Interview</h2>

            <input
                placeholder="Candidate Name"
                value={candidateName}
                onChange={(e)=>setCandidateName(e.target.value)}
            />

            <br /><br />

            <input
                placeholder="Job Role"
                value={jobRole}
                onChange={(e)=>setJobRole(e.target.value)}
            />

            <br /><br />

            <input
                placeholder="Experience Level"
                value={experienceLevel}
                onChange={(e)=>setExperienceLevel(e.target.value)}
            />

            <br /><br />

            <button onClick={handleSubmit}>
                Start Interview
            </button>

        </div>
    );
}

export default InterviewForm;