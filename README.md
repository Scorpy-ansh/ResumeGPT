# ResumeIQ

This repository contains **two separate apps**:

1. `app.py` is the original Streamlit application. It remains available and unchanged as the Streamlit version.
2. `web_app.py` is the new standalone browser website with a custom HTML/CSS/JavaScript interface.

The website is a minimal, AI-powered resume analyzer using Flask and Google Gemini. Upload a text-based PDF resume to receive five practical job-search tools in one place:

- **Resume review:** recruiter-style score, strengths, weaknesses, improvements, and recommendation
- **ATS checker:** ATS score, missing keywords, formatting issues, and suggestions
- **Interview prep:** 10 technical and 5 HR questions tailored to the resume
- **Career roadmap:** suitable paths, skills, certifications, and a six-month roadmap
- **Cover letter:** a professional cover letter based on the candidate profile

The interface includes a responsive dashboard, cached results for the current session, a connection test, and a Light/Dark appearance switch.

## Run the website locally

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

Start the website backend:

```bash
python web_app.py
```

Open `http://localhost:5000` in your browser.

## Run the original Streamlit version

The original Streamlit app is still in `app.py`:

```bash
streamlit run app.py
```

It opens at `http://localhost:8501`.

## Deploy the website

The website can be deployed to any Python host that supports Flask. Set the start command to:

```bash
gunicorn web_app:app
```

For local Windows use, `python web_app.py` is sufficient.

### Deploy on Vercel

Import this repository into Vercel and deploy from the `main` branch. The included
`pyproject.toml` explicitly points Vercel to the standalone website entry point:

```toml
[tool.vercel]
entrypoint = "web_app:app"
```

In the Vercel project settings, add this environment variable:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not set the Vercel entry point to `app.py`; that file is the preserved Streamlit
application. Vercel should deploy `web_app:app`.

## Deploy the Streamlit version with Streamlit Community Cloud

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
app.py          # Original Streamlit application (preserved)
web_app.py      # Separate Flask website backend
templates/      # Website HTML
static/         # Website CSS and JavaScript
pdf_utils.py    # PDF text extraction
prompts.py      # Analysis prompt templates
requirements.txt
test.py         # Simple Gemini connection test
```
