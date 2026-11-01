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

# Session state keys
RESULTS_KEYS = [
    "resume_analysis",
    "ats_check",
    "interview_questions",
    "career_assistant",
    "cover_letter"
]

for key in RESULTS_KEYS:
    if key not in st.session_state:
        st.session_state[key] = None

def run_all_analyses(resume_text):
    with st.status("🤖 Running all 5 analyses with Gemini AI...", expanded=True) as status:

        st.write("📊 Analyzing Resume (1/5)...")
        st.session_state["resume_analysis"] = ask_gemini(
            ROLE_PROMPT.format(resume=resume_text)
        )

        st.write("✅ Checking ATS Score (2/5)...")
        st.session_state["ats_check"] = ask_gemini(
            ATS_PROMPT.format(resume=resume_text)
        )

        st.write("❓ Generating Interview Questions (3/5)...")
        st.session_state["interview_questions"] = ask_gemini(
            INTERVIEW_PROMPT.format(resume=resume_text)
        )

        st.write("🎯 Career Guidance & Roadmap (4/5)...")
        st.session_state["career_assistant"] = ask_gemini(
            CAREER_PROMPT.format(resume=resume_text)
        )

        st.write("✉️ Generating Cover Letter (5/5)...")
        st.session_state["cover_letter"] = ask_gemini(
            COVER_PROMPT.format(resume=resume_text)
        )

        status.update(label="✅ All analyses complete! Switch tabs to view results.", state="complete", expanded=False)

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

    st.markdown("---")
    analyze_col, clear_col = st.columns([3, 1])

    with analyze_col:
        if st.button("🚀 Analyze My Resume (All 5 Sections)", type="primary", use_container_width=True):
            run_all_analyses(resume_text)
            st.rerun()

    with clear_col:
        if st.button("🧹 Clear Results", use_container_width=True):
            for key in RESULTS_KEYS:
                st.session_state[key] = None
            st.rerun()

    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 Resume Analysis",
            "✅ ATS Checker",
            "❓ Interview Questions",
            "🎯 Career Assistant",
            "✉️ Cover Letter"
        ]
    )

    # TAB 1
    with tab1:
        if st.session_state["resume_analysis"]:
            st.markdown(st.session_state["resume_analysis"])
        else:
            st.info("👆 Click **'Analyze My Resume'** above to run all analyses at once.")

    # TAB 2
    with tab2:
        if st.session_state["ats_check"]:
            st.markdown(st.session_state["ats_check"])
        else:
            st.info("👆 Click **'Analyze My Resume'** above to run all analyses at once.")

    # TAB 3
    with tab3:
        if st.session_state["interview_questions"]:
            st.markdown(st.session_state["interview_questions"])
        else:
            st.info("👆 Click **'Analyze My Resume'** above to run all analyses at once.")

    # TAB 4
    with tab4:
        if st.session_state["career_assistant"]:
            st.markdown(st.session_state["career_assistant"])
        else:
            st.info("👆 Click **'Analyze My Resume'** above to run all analyses at once.")

    # TAB 5
    with tab5:
        if st.session_state["cover_letter"]:
            st.markdown(st.session_state["cover_letter"])
        else:
            st.info("👆 Click **'Analyze My Resume'** above to run all analyses at once.")
