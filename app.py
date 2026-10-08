import streamlit as st
import pdfplumber
import os

from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -----------------------------
# Gemini Function
# -----------------------------
import time

def ask_gemini(prompt):

    for attempt in range(5):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if "503" in str(e):
                time.sleep(2 ** attempt)
            else:
                return f"Error: {str(e)}"

    return "Gemini servers are busy. Please try again later."
# -----------------------------
# PDF Extraction
# -----------------------------
def extract_text(pdf_file):
    text = ""

    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        return f"PDF Error: {str(e)}"

    return text

# -----------------------------
# Prompts
# -----------------------------
ROLE_PROMPT = """
You are a Senior HR Recruiter.

Analyze the resume and provide:

1. Resume Score (/100)
2. Strengths
3. Weaknesses
4. Improvements
5. Final Recommendation

Resume:
{resume}
"""

ATS_PROMPT = """
Act as an Applicant Tracking System.

Provide:

1. ATS Score (/100)
2. Missing Keywords
3. Formatting Issues
4. Suggestions

Resume:
{resume}
"""

INTERVIEW_PROMPT = """
You are a Technical Interviewer.

Generate:
- 10 Technical Questions
- 5 HR Questions

Resume:
{resume}
"""

CAREER_PROMPT = """
You are a Career Counselor.

Provide:

1. Suitable Career Paths
2. Skills To Learn
3. Certifications
4. 6 Month Roadmap

Resume:
{resume}
"""

COVER_PROMPT = """
Generate a professional cover letter based on this resume.

Resume:
{resume}
"""

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer & Career Assistant")
st.markdown("Prompt Engineering Project using Gemini AI")

# Test API
with st.expander("API Test"):
    if st.button("Test Gemini"):
        st.write(
            ask_gemini("Say hello in one sentence.")
        )

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    # IMPORTANT
    resume_text = resume_text[:8000]

    st.success("Resume Uploaded Successfully")

    with st.expander("View Resume Text"):
        st.text(resume_text[:3000])

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Resume Analysis",
            "ATS Checker",
            "Interview Questions",
            "Career Assistant",
            "Cover Letter"
        ]
    )

    # TAB 1
    with tab1:

        if st.button("Analyze Resume"):

            with st.spinner("Analyzing..."):

                prompt = ROLE_PROMPT.format(
                    resume=resume_text
                )

                st.markdown(
                    ask_gemini(prompt)
                )

    # TAB 2
    with tab2:

        if st.button("Check ATS Score"):

            with st.spinner("Checking ATS..."):

                prompt = ATS_PROMPT.format(
                    resume=resume_text
                )

                st.markdown(
                    ask_gemini(prompt)
                )

    # TAB 3
    with tab3:

        if st.button("Generate Interview Questions"):

            with st.spinner("Generating..."):

                prompt = INTERVIEW_PROMPT.format(
                    resume=resume_text
                )

                st.markdown(
                    ask_gemini(prompt)
                )

    # TAB 4
    with tab4:

        if st.button("Career Guidance"):

            with st.spinner("Generating Roadmap..."):

                prompt = CAREER_PROMPT.format(
                    resume=resume_text
                )

                st.markdown(
                    ask_gemini(prompt)
                )

    # TAB 5
    with tab5:

        if st.button("Generate Cover Letter"):

            with st.spinner("Generating Cover Letter..."):

                prompt = COVER_PROMPT.format(
                    resume=resume_text
                )

                st.markdown(
                    ask_gemini(prompt)
                )