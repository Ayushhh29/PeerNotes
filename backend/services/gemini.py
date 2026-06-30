import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_summary(text):

    prompt = f"""
    Summarize the following study notes.
    Use simple language and bullet points.
    Keep the summary useful for revision.

    Notes:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text


def generate_answer(prompt):

    response = model.generate_content(prompt)

    return response.text


def generate_quiz(text):
    """
    Generate a multiple-choice quiz using Gemini.
    """

    prompt = f"""
    You are an expert teacher.

    Create a quiz from the following study notes.

    Requirements:
    - Generate exactly 10 multiple-choice questions.
    - Each question should have 4 options.
    - Mark the correct answer.
    - Questions should test understanding, not memorization.
    - Format:

    Question 1:
    ...

    A.
    B.
    C.
    D.

    Answer:

    Notes:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text


def generate_flashcards(text):
    """
    Generate revision flashcards using Gemini.
    """

    prompt = f"""
    You are an expert teacher.

    Create 15 revision flashcards from the following study notes.

    Rules:
    - Each flashcard should have one question and one answer.
    - Questions should help students revise concepts.
    - Answers should be short and precise.
    - Use only the information present in the notes.

    Format:

    Flashcard 1

    Q: ...

    A: ...

    Flashcard 2

    Q: ...

    A: ...

    Notes:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text

def chat_with_notes(notes, question):
    """
    Answer questions using only the uploaded notes.
    """

    prompt = f"""
You are PeerNotes AI.

You help students understand their uploaded study notes.

Rules:
- Answer ONLY from the notes below.
- If the answer is not present, reply:
  "I couldn't find this information in the uploaded notes."
- Explain in simple language.
- Use bullet points whenever helpful.
- If appropriate, include a short example.

Notes:
{notes}

Student Question:
{question}
"""

    response = model.generate_content(prompt)

    return response.text