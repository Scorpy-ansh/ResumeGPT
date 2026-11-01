import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai

from pdf_utils import extract_text
from prompts import (
    ATS_PROMPT,
    CAREER_PROMPT,
    COVER_PROMPT,
    INTERVIEW_PROMPT,
    ROLE_PROMPT,
)

load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"
MAX_RESUME_CHARS = 8000
RESULTS_KEYS = (
    "resume_analysis",
    "ats_check",
    "interview_questions",
    "career_assistant",
    "cover_letter",
)

ANALYSIS_SECTIONS = (
    ("resume_analysis", "Resume review", "Scoring, strengths, weaknesses, and recommendations", ROLE_PROMPT),
    ("ats_check", "ATS checker", "Keywords, formatting, and screening improvements", ATS_PROMPT),
    ("interview_questions", "Interview prep", "Technical and HR questions tailored to the resume", INTERVIEW_PROMPT),
    ("career_assistant", "Career roadmap", "Career paths, skills, certifications, and a six-month plan", CAREER_PROMPT),
    ("cover_letter", "Cover letter", "A professional letter based on the candidate profile", COVER_PROMPT),
)

def get_api_key():
    """Read the API key without exposing it in the application or logs."""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key

    try:
        return st.secrets.get("GEMINI_API_KEY")
    except (FileNotFoundError, KeyError):
        return None


def ask_gemini(prompt):
    api_key = get_api_key()
    if not api_key:
        return (
            "Error: Gemini API key is not configured. Add `GEMINI_API_KEY` to your "
            "`.env` file or Streamlit secrets."
        )

    client = genai.Client(api_key=api_key)
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )
            if not response.text:
                return "Error: Gemini returned an empty response. Please try again."
            return response.text
        except Exception as error:
            if "503" in str(error) and attempt < 4:
                time.sleep(2**attempt)
                continue
            return f"Error: {error}"

    return "Gemini servers are busy. Please try again later."


def clear_results():
    for key in RESULTS_KEYS:
        st.session_state[key] = None


def run_all_analyses(resume_text):
    with st.status("Running your complete resume review...", expanded=True) as status:
        for index, (key, title, _, prompt_template) in enumerate(ANALYSIS_SECTIONS, start=1):
            st.write(f"{index}/5 · {title}")
            st.session_state[key] = ask_gemini(prompt_template.format(resume=resume_text))

        status.update(
            label="Analysis complete — your insights are ready.",
            state="complete",
            expanded=False,
        )


def inject_styles(theme):
    if theme == "Dark":
        colors = {
            "background": "#0b1120",
            "surface": "#111a2e",
            "surface_alt": "#17233b",
            "text": "#f8fafc",
            "muted": "#a7b5cf",
            "border": "#263653",
        }
    else:
        colors = {
            "background": "#f7f9fc",
            "surface": "#ffffff",
            "surface_alt": "#eef3ff",
            "text": "#182033",
            "muted": "#65708a",
            "border": "#dfe6f2",
        }

    st.markdown(
        f"""
        <style>
        :root {{
            --bg: {colors["background"]};
            --surface: {colors["surface"]};
            --surface-alt: {colors["surface_alt"]};
            --text: {colors["text"]};
            --muted: {colors["muted"]};
            --border: {colors["border"]};
            --accent: #5b5cf0;
            --accent-soft: #e8e9ff;
        }}
        .stApp {{ background: var(--bg); color: var(--text); }}
        [data-testid="stHeader"] {{ background: transparent; }}
        [data-testid="stSidebar"] {{ background: var(--surface); border-right: 1px solid var(--border); }}
        [data-testid="stSidebar"] * {{ color: var(--text); }}
        h1, h2, h3, h4, p, label, .stMarkdown {{ color: var(--text); }}
        .muted {{ color: var(--muted); }}
        .hero {{
            padding: 2rem 2.25rem;
            border: 1px solid var(--border);
            border-radius: 24px;
            background: linear-gradient(135deg, var(--surface) 0%, var(--surface-alt) 100%);
            margin-bottom: 1.25rem;
        }}
        .eyebrow {{ color: #6869f4; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: .75rem; }}
        .hero h1 {{ font-size: clamp(2rem, 5vw, 3.5rem); line-height: 1.05; margin: .45rem 0 .75rem; }}
        .feature-card {{
            border: 1px solid var(--border); border-radius: 16px; padding: 1rem;
            background: var(--surface); min-height: 112px; margin-bottom: .75rem;
        }}
        .feature-card strong {{ display: block; margin-bottom: .35rem; }}
        .feature-card span {{ color: var(--muted); font-size: .86rem; line-height: 1.4; }}
        .upload-card {{
            border: 1px dashed #7b7cf6; border-radius: 18px; padding: .5rem;
            background: var(--surface);
        }}
        .stButton > button {{ border-radius: 10px; font-weight: 650; min-height: 2.7rem; }}
        [data-testid="stFileUploader"] {{ background: var(--surface); border-radius: 14px; }}
        [data-testid="stExpander"], [data-testid="stStatusWidget"] {{
            border-color: var(--border); background: var(--surface); border-radius: 14px;
        }}
        .result-empty {{ padding: 2rem; text-align: center; border: 1px dashed var(--border); border-radius: 16px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="ResumeIQ", page_icon="✦", layout="wide")

for key in RESULTS_KEYS:
    st.session_state.setdefault(key, None)
st.session_state.setdefault("theme", "Light")

with st.sidebar:
    st.markdown("## ✦ ResumeIQ")
    st.caption("A clearer path from resume to next opportunity.")
    st.divider()
    st.selectbox("Appearance", ("Light", "Dark"), key="theme")
    st.divider()
    st.markdown("### What you get")
    st.markdown("**01** Resume score & feedback")
    st.markdown("**02** ATS readiness")
    st.markdown("**03** Interview preparation")
    st.markdown("**04** Career roadmap")
    st.markdown("**05** Tailored cover letter")
    st.divider()
    st.caption("Powered by Gemini AI · Your resume is processed for this session.")

inject_styles(st.session_state["theme"])

st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">AI career companion</div>
        <h1>Make your resume<br>work harder.</h1>
        <p class="muted">Upload a PDF and get practical, recruiter-style guidance across every stage of your job search.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

feature_columns = st.columns(5)
for column, (_, title, description, _) in zip(feature_columns, ANALYSIS_SECTIONS):
    with column:
        st.markdown(
            f'<div class="feature-card"><strong>{title}</strong><span>{description}</span></div>',
            unsafe_allow_html=True,
        )

st.markdown("### Start with your resume")
st.markdown('<div class="upload-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop your resume PDF here or browse your files",
    type=["pdf"],
    label_visibility="visible",
)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    try:
        resume_text = extract_text(uploaded_file).strip()
    except Exception as error:
        st.error(f"Could not read this PDF: {error}")
        st.stop()

    if not resume_text:
        st.error("This PDF does not contain readable text. Please upload a text-based resume.")
        st.stop()

    resume_text = resume_text[:MAX_RESUME_CHARS]
    st.success(f"{uploaded_file.name} is ready · {len(resume_text):,} characters processed")

    with st.expander("Preview extracted resume text"):
        st.text(resume_text[:3000])

    action_col, clear_col = st.columns([3, 1])
    with action_col:
        if st.button("✦ Analyze my resume", type="primary", use_container_width=True):
            run_all_analyses(resume_text)
            st.rerun()
    with clear_col:
        if st.button("Clear results", use_container_width=True):
            clear_results()
            st.rerun()

    st.markdown("### Your insights")
    tabs = st.tabs([f"{title}" for _, title, _, _ in ANALYSIS_SECTIONS])
    for tab, (key, title, _, _) in zip(tabs, ANALYSIS_SECTIONS):
        with tab:
            if st.session_state[key]:
                st.markdown(st.session_state[key])
            else:
                st.markdown(
                    f'<div class="result-empty"><strong>{title} is waiting for your analysis.</strong>'
                    '<p class="muted">Click “Analyze my resume” above to generate your personalized results.</p></div>',
                    unsafe_allow_html=True,
                )
else:
    st.info("Upload a PDF resume to unlock your personalized analysis.")

with st.sidebar:
    with st.expander("Connection test"):
        if st.button("Test Gemini", use_container_width=True):
            with st.spinner("Checking connection..."):
                st.write(ask_gemini("Say hello in one sentence."))
