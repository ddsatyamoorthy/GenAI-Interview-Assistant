import google.generativeai as genai
from dotenv import load_dotenv
import os
from prompts import ANSWER_EVALUATION_PROMPT
import json
from prompts import ANSWER_EVALUATION_PROMPT
import json
import re

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

from prompts import QUESTION_PROMPT


def generate_question(job_role, experience):

    prompt = QUESTION_PROMPT.format(
        job_role=job_role,
        experience=experience
    )

    response = model.generate_content(prompt)

    return response.text




def evaluate_answer(question, answer):

    prompt = ANSWER_EVALUATION_PROMPT.format(
        question=question,
        answer=answer
    )

    response = model.generate_content(prompt)

    raw_response = response.text.strip()

    print("\n========== Gemini Raw Response ==========")
    print(raw_response)
    print("=========================================\n")

    # Remove markdown if present
    raw_response = raw_response.replace("```json", "")
    raw_response = raw_response.replace("```", "")
    raw_response = raw_response.strip()

    try:

        # Extract JSON object using regex
        match = re.search(r'\{.*\}', raw_response, re.DOTALL)

        if match:

            json_string = match.group()

            result = json.loads(json_string)

        else:

            raise Exception("No JSON found")

    except Exception as e:

        print("JSON Parsing Error:")
        print(e)

        result = {

            "score": 5,

            "feedback":
                "Unable to parse Gemini response",

            "next_question":
                "Tell me about OOP."

        }

    return result