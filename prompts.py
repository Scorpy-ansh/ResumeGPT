ROLE_PROMPT = """
You are a Senior HR Recruiter with 15 years of experience.

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

Analyze this resume.

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

Based on this resume generate:

- 10 Technical Questions
- 5 HR Questions

Resume:
{resume}
"""

CAREER_PROMPT = """
You are a Career Counselor.

Analyze this resume.

Provide:

1. Suitable Career Paths
2. Skills To Learn
3. Recommended Certifications
4. 6 Month Roadmap

Resume:
{resume}
"""

COVER_PROMPT = """
Generate a professional cover letter based on this resume.

Resume:
{resume}
"""