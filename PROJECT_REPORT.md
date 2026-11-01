# ResumeIQ Project Report

## 1. Project overview

ResumeIQ is an AI-powered resume analysis platform. It accepts a PDF resume and transforms it into practical career guidance through five focused outputs: resume review, ATS checking, interview preparation, career planning, and cover-letter generation.

The project has two supported interfaces:

- **Standalone website:** a Flask backend with a custom HTML, CSS, and JavaScript frontend, deployed at [resume-gpt-omega.vercel.app](https://resume-gpt-omega.vercel.app/).
- **Original Streamlit application:** preserved in `app.py` for compatibility with the earlier version of the project.

## 2. Problem statement

Job seekers often receive limited feedback about why a resume is not performing well. Existing tools may focus on only one area, such as grammar or ATS keywords, while leaving the candidate to connect the results themselves.

ResumeIQ addresses this by combining multiple resume-related tasks into one guided workflow. It gives the user a structured view of resume quality, discoverability, interview readiness, career direction, and application writing.

## 3. Objectives

The main objectives were:

1. Build a simple PDF upload workflow.
2. Extract resume text reliably from text-based PDFs.
3. Use specialized prompts for different career tasks.
4. Present results in a clear, minimal, responsive interface.
5. Support both light and dark themes.
6. Deploy the website through Vercel.
7. Preserve the existing Streamlit implementation.
8. Avoid storing secrets or uploaded documents in source control.

## 4. Functional features

### 4.1 Resume review

The system asks Gemini to act as a senior HR recruiter and return:

- Resume score out of 100
- Strengths
- Weaknesses
- Improvements
- Final recommendation

### 4.2 ATS checker

The ATS workflow evaluates:

- ATS score
- Missing keywords
- Formatting issues
- Suggestions to improve screening compatibility

### 4.3 Interview preparation

The interview workflow generates:

- Ten technical interview questions
- Five HR interview questions

Questions are based on the experience and skills extracted from the uploaded resume.

### 4.4 Career roadmap

The career assistant produces:

- Suitable career paths
- Skills to learn
- Recommended certifications
- A six-month roadmap

### 4.5 Cover letter

The cover-letter workflow creates a professional draft based on the candidate's resume. The result is intended as a starting point and should be customized for each job application.

## 5. System architecture

```text
Browser
   |
   | POST /api/analyze with PDF
   v
Flask application (web_app.py)
   |
   +--> pdf_utils.py ------> Extract resume text
   |
   +--> prompts.py --------> Build five role-specific prompts
   |
   +--> Google Gemini ------> Generate five analysis responses
   |
   v
JSON response
   |
   v
Browser report tabs
```

The Streamlit version follows the same extraction and Gemini workflow but renders the interface through Streamlit widgets.

## 6. Technology stack

| Layer | Technology |
| --- | --- |
| Frontend | HTML, CSS, vanilla JavaScript |
| Website backend | Flask |
| Original interface | Streamlit |
| AI provider | Google Gemini through `google-genai` |
| PDF processing | `pdfplumber` |
| Configuration | Environment variables and `python-dotenv` |
| Deployment | Vercel |

## 7. User workflow

1. Open the website.
2. Choose a PDF resume or drag it into the upload area.
3. Select **Analyze my resume**.
4. Wait while the five Gemini analyses are generated.
5. Review the report using the result tabs.
6. Switch between light and dark mode when needed.
7. Start a new analysis without refreshing the page.

## 8. Interface design

The website uses a minimal visual system:

- High-contrast typography
- Large, focused upload area
- Indigo accent color for primary actions
- Card-based sections with restrained borders
- Responsive layout for smaller screens
- Dark mode with matching contrast and spacing
- Dedicated result summary area for scores and key signals

The design intentionally avoids a dense dashboard so that the user can focus on one career decision at a time.

## 9. Error handling

The application reports errors for:

- Missing resume uploads
- Non-PDF files
- PDFs with no readable text
- Missing Gemini API credentials
- Empty Gemini responses
- Gemini service availability errors

Temporary Gemini 503 responses are retried with exponential backoff. API keys are never included in the repository.

## 10. Testing and verification

The following checks were used during development:

- Python syntax validation for the Flask entry point
- Import validation for `web_app:app`
- Dependency/import resolution checks
- Git whitespace validation
- Local HTTP health verification
- Browser verification of the deployed landing page
- Browser verification of the theme toggle
- Verification that the Vercel entry point resolves to `web_app:app`

## 11. Deployment configuration

Vercel is configured through `pyproject.toml`:

```toml
[tool.vercel]
entrypoint = "web_app:app"
```

The deployment requires this environment variable:

```text
GEMINI_API_KEY
```

The value must be created in Vercel's Environment Variables settings and should be enabled for every environment that will run the application.

## 12. Security considerations

- Never commit `.env`.
- Never paste an API key into GitHub issues, README files, screenshots, or chat messages.
- Rotate any key that has been exposed.
- Keep the Gemini key in Vercel Environment Variables for production.
- Avoid logging full resume contents or API responses in production logs.
- Consider adding rate limiting before making the public deployment widely available.

## 13. Limitations

The current version has several known limitations:

1. It extracts text from text-based PDFs but does not perform OCR.
2. AI responses are not guaranteed to be factually correct.
3. Results are generated sequentially, so a complete report may take time.
4. Very long resumes are truncated to 8,000 characters.
5. There is no user account or saved-report system.
6. There is no job-description comparison workflow yet.

## 14. Future enhancements

Potential future improvements include:

- OCR for scanned resumes
- Job description matching and keyword gap analysis
- Downloadable PDF or DOCX reports
- User accounts and private report history
- Streaming model responses
- Rate limiting and usage quotas
- Automated tests for the API endpoint
- Structured JSON responses for more precise score cards
- Accessibility improvements such as richer keyboard and screen-reader testing

## 15. Conclusion

ResumeIQ demonstrates how a focused AI workflow can combine document processing, prompt engineering, and a polished web interface into a practical career tool. The standalone website is deployable on Vercel, while the original Streamlit application remains available for continuity and comparison.
