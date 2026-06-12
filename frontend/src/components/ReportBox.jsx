function ReportBox({ report }) {

    if (!report) return null;

    return (

        <div>

            <h2>Final Report</h2>

            <h3>
                Candidate:
                {report.candidate_name}
            </h3>

            <h3>
                Job Role:
                {report.job_role}
            </h3>

            <h3>
                Overall Score:
                {report.overall_score}
            </h3>

            <h3>Strengths</h3>

            <ul>

                {
                    report.strengths?.map(

                        (item,index)=>

                        <li key={index}>
                            {item}
                        </li>

                    )
                }

            </ul>

            <h3>Improvement Areas</h3>

            <ul>

                {
                    report.improvement_areas?.map(

                        (item,index)=>

                        <li key={index}>
                            {item}
                        </li>

                    )
                }

            </ul>

            <h3>Summary</h3>

            <p>

                {report.summary}

            </p>

        </div>

    );

}

export default ReportBox;