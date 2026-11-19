import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# You can change this to another model available to your Google AI API key.
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def _get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add your key to the .env file. "
            "See README.md for setup instructions."
        )
    return genai.Client(api_key=api_key)


def ask_gemini(pdf_text, question):
    """Ask Gemini a question using the extracted PDF text as context."""
    if not pdf_text.strip():
        raise ValueError("There is no extracted PDF text to analyze.")
    if not question.strip():
        raise ValueError("Please enter a question.")

    # Keep the prompt within a manageable size for this starter project.
    context = pdf_text[:50000]
    prompt = f"""
You are a helpful document analysis assistant.
Answer the user's question using the PDF content below.
If the answer is not present in the supplied content, say that clearly.
Do not invent facts. Use clear headings or bullet points when useful.

PDF CONTENT:
{context}

USER QUESTION:
{question}
"""
    response = _get_client().models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    answer = getattr(response, "text", None)
    if not answer:
        raise RuntimeError("Gemini returned an empty response. Please try again.")
    return answer


def summarize_pdf(pdf_text):
    prompt = """
Summarize this PDF in a student-friendly, well-organized format.
Include:
1. Overview and main topic
2. Important points
3. Key terms or findings
4. Conclusion

Only use information supported by the supplied PDF text. If a detail is
missing, do not make it up.
"""
    return ask_gemini(pdf_text, prompt)
