# ResumeIQ

ResumeIQ is a minimal, AI-powered resume analyzer built with Streamlit and Google Gemini. Upload a text-based PDF resume to receive five practical job-search tools in one place:

- **Resume review:** recruiter-style score, strengths, weaknesses, improvements, and recommendation
- **ATS checker:** ATS score, missing keywords, formatting issues, and suggestions
- **Interview prep:** 10 technical and 5 HR questions tailored to the resume
- **Career roadmap:** suitable paths, skills, certifications, and a six-month roadmap
- **Cover letter:** a professional cover letter based on the candidate profile

The interface includes a responsive dashboard, cached results for the current session, a connection test, and a Light/Dark appearance switch.

## Run locally

### Requirements

- Python 3.10+
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### Setup

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Start the app:

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Deploy with Streamlit Community Cloud

1. Push this repository to GitHub.
2. Create a new app at [share.streamlit.io](https://share.streamlit.io).
3. Select this repository, the `main` branch, and `app.py`.
4. Add the following secret in **Advanced settings**:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Never commit `.env` or expose an API key in source control. The `.gitignore` file already excludes local secrets and Python cache files.

## Project structure

```text
app.py          # Streamlit interface and Gemini orchestration
pdf_utils.py    # PDF text extraction
prompts.py      # Analysis prompt templates
requirements.txt
test.py         # Simple Gemini connection test
```
