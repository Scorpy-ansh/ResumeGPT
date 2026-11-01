# ResumeIQ

> **A focused AI career companion for turning a resume into a practical job-search plan.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-resume--gpt--omega.vercel.app-625bf4?style=for-the-badge)](https://resume-gpt-omega.vercel.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Website-Flask-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-8E75B2?style=flat-square)](https://ai.google.dev/)

ResumeIQ analyzes a text-based PDF resume and returns recruiter-style feedback, ATS guidance, interview questions, career direction, and a tailored cover letter. The project includes a standalone browser website and preserves the original Streamlit application.

## Live website

Open the deployed application at **[resume-gpt-omega.vercel.app](https://resume-gpt-omega.vercel.app/)**.

The website provides:

- A clean, responsive upload experience
- Light and dark mode
- Drag-and-drop PDF selection
- Separate result tabs for each analysis
- Score summaries when an AI response includes a score
- Mobile-friendly report layout

## Features

| Tool | What it provides |
| --- | --- |
| **Resume review** | Resume score, strengths, weaknesses, improvements, and final recommendation |
| **ATS checker** | ATS score, missing keywords, formatting issues, and suggestions |
| **Interview prep** | Ten technical questions and five HR questions tailored to the resume |
| **Career roadmap** | Suitable career paths, skills to learn, certifications, and a six-month roadmap |
| **Cover letter** | A professional cover letter based on the candidate's experience |

## How it works

1. The user uploads a PDF resume in the browser.
2. The Flask API extracts readable text with `pdfplumber`.
3. The text is limited to 8,000 characters for predictable model input.
4. Five specialized prompts are sent to Google Gemini.
5. The website presents the responses in separate, readable report tabs.

## Run the website locally

### Prerequisites

- Python 3.10 or newer
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### Windows setup

```powershell
cd "C:\path\to\ResumeGPT"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a local `.env` file. Do not commit this file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Start the standalone website:

```powershell
python web_app.py
```

Visit [http://localhost:5000](http://localhost:5000).

## Deploy on Vercel

This repository already contains the Vercel configuration for the standalone Flask website:

```toml
[tool.vercel]
entrypoint = "web_app:app"
```

In the Vercel project settings, add the following environment variable for Production, Preview, and Development:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

After saving the variable, redeploy the project. Never put the real API key in GitHub, source files, screenshots, or documentation.

## Original Streamlit application

The original Streamlit version remains preserved in `app.py`:

```powershell
streamlit run app.py
```

It opens at [http://localhost:8501](http://localhost:8501).

The website and Streamlit app share the same PDF extraction and prompt modules, but they are separate entry points.

## Project structure

```text
app.py                 # Preserved original Streamlit application
web_app.py             # Flask website backend and API
templates/index.html   # Website markup
static/styles.css      # Website design system and responsive layout
static/app.js          # Upload, theme, tabs, and report interactions
pdf_utils.py           # PDF text extraction
prompts.py             # Gemini analysis prompt templates
requirements.txt       # Python dependencies
pyproject.toml         # Vercel entry point and deployment dependencies
PROJECT_REPORT.md      # Detailed project report
test.py                # Basic Gemini connection test
```

## Security and privacy

- API keys are read from environment variables.
- `.env` is ignored by Git.
- Resume text is sent to Gemini only when the user requests analysis.
- The current implementation does not permanently store uploaded resumes or generated reports.
- Use a text-based PDF for the best extraction quality.

## Limitations

- Scanned/image-only PDFs need OCR support, which is not currently included.
- AI output quality depends on the completeness and formatting of the uploaded resume.
- Each complete analysis makes five Gemini requests.
- The 8,000-character input limit may omit content from very long resumes.

## License

This project is intended for educational and portfolio use. Add a project-specific license before distributing it as an open-source package.
