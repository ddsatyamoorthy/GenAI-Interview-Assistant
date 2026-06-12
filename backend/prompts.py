QUESTION_PROMPT = """
Generate one interview question.

Job Role: {job_role}

Experience Level: {experience}

Return only the question.
"""

ANSWER_EVALUATION_PROMPT = """
You are an expert technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Return ONLY valid JSON.

Example:

{{
    "score": 8,
    "feedback": "Good answer with examples.",
    "next_question": "Explain list and tuple in Python."
}}

Rules:

1. Return JSON only.
2. No markdown.
3. No explanation.
4. No ```json blocks.
5. No extra text before or after JSON.
"""

REPORT_PROMPT = """
Based on interview history:

{history}

Return only valid JSON:

{{
"strengths":[
"Good communication"
],

"improvement_areas":[
"Need more project experience"
],

"summary":"Overall summary"
}}
"""