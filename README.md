# AI Resume Analyzer & Career Assistant

An intelligent resume analysis platform built with Streamlit and powered by Google Gemini AI. Upload any resume PDF and get instant HR analysis, ATS scoring, interview questions, career guidance, and a professional cover letter — all in one place.

## ✨ Features

| Tab | Description |
|-----|-------------|
| **Resume Analysis** | HR-style scoring (/100), strengths, weaknesses, improvements & final recommendation |
| **ATS Checker** | Applicant Tracking System score, missing keywords, formatting issues & suggestions |
| **Interview Questions** | 10 technical + 5 HR questions tailored to the candidate's profile |
| **Career Assistant** | Suitable career paths, skills to learn, certifications & 6-month roadmap |
| **Cover Letter** | Professionally generated cover letter based on the resume |

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **AI Model:** Google Gemini 3.5 Flash Lite (`gemini-3.5-flash-lite`)
- **PDF Parsing:** [pdfplumber](https://github.com/jsvine/pdfplumber)
- **Env Management:** python-dotenv

## 📦 Project Structure

```
AI Resume Analyzer Chatgpt/
├── app.py              # Main Streamlit application
├── pdf_utils.py        # PDF text extraction utilities
├── prompts.py          # Gemini prompt templates
├── test.py             # Quick API test script
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── .env                # (Create this) Store your GEMINI_API_KEY
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A Google Gemini API key ([get one free](https://aistudio.google.com/apikey))

### 1. Clone the Repository

```bash
git clone https://github.com/Scorpy-ansh/ResumeGPT.git
cd ResumeGPT
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a file named **`.env`** in the project root and add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace `your_gemini_api_key_here` with your actual key from [Google AI Studio](https://aistudio.google.com/apikey).

### 5. Run the App Locally

```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`

---

## 📤 Deploy to Streamlit Community Cloud

### Step 1 — Push Code to GitHub

(Already done! Repo is live at `https://github.com/Scorpy-ansh/ResumeGPT`)

### Step 2 — Deploy on Streamlit

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. Click **New app**
3. Fill in:
   - **Repository:** `Scorpy-ansh/ResumeGPT`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Advanced settings...** → **Secrets** and paste:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
5. Click **Save** and then **Deploy!**

### Step 3 — Share Your App

After deployment, you'll get a public URL like:
`https://your-username-resumegpt.streamlit.app`

Share this link with anyone — no setup required on their end!

---

## 📝 Usage Tips

1. Upload a **PDF resume** (max ~8k characters processed for context limits)
2. Click any tab button to run the corresponding analysis
3. Each request uses Gemini AI — responses take 2-10 seconds depending on server load
4. The built-in retry logic handles transient 503 errors automatically

## 🔒 Security Notes

- **Never** commit your `.env` file or expose API keys in code (already handled by `.gitignore`)
- Streamlit Secrets are the safe way to store keys in production
- Rotate your API key immediately if you suspect it has been leaked

## 📚 How It Works

1. **PDF Upload →** `pdfplumber` extracts raw text from the uploaded resume
2. **Prompt Engineering →** The extracted text is injected into role-specific system prompts (HR Recruiter, ATS Scanner, Interviewer, etc.)
3. **Gemini API Call →** The combined prompt is sent to Google's Gemini model with exponential backoff retry logic
4. **Streamlit Render →** The AI response is displayed as formatted Markdown in the UI

---

**Built as a Prompt Engineering & AI Integration project.** 🎓
