import os
import time

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai

from pdf_utils import extract_text
from prompts import ATS_PROMPT, CAREER_PROMPT, COVER_PROMPT, INTERVIEW_PROMPT, ROLE_PROMPT

load_dotenv()

app = Flask(__name__)
MODEL_NAME = "gemini-3.5-flash-lite"
MAX_RESUME_CHARS = 8000

ANALYSES = (
    ("resume_analysis", ROLE_PROMPT),
    ("ats_check", ATS_PROMPT),
    ("interview_questions", INTERVIEW_PROMPT),
    ("career_assistant", CAREER_PROMPT),
    ("cover_letter", COVER_PROMPT),
)


def ask_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )
            if not response.text:
                raise RuntimeError("Gemini returned an empty response.")
            return response.text
        except Exception as error:
            if "503" in str(error) and attempt < 4:
                time.sleep(2**attempt)
                continue
            raise RuntimeError(str(error)) from error


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/analyze")
def analyze():
    uploaded_file = request.files.get("resume")
    if not uploaded_file or not uploaded_file.filename:
        return jsonify({"error": "Please choose a PDF resume."}), 400
    if not uploaded_file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF resumes are supported."}), 400

    try:
        resume_text = extract_text(uploaded_file).strip()[:MAX_RESUME_CHARS]
        if not resume_text:
            return jsonify({"error": "This PDF does not contain readable text."}), 422

        results = {
            key: ask_gemini(prompt.format(resume=resume_text))
            for key, prompt in ANALYSES
        }
        return jsonify({"filename": uploaded_file.filename, "results": results})
    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
