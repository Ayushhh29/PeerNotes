from services.gemini import (
    generate_summary as gemini_summary,
    generate_answer as gemini_answer
)


def generate_summary(text):

    return gemini_summary(text)


def split_text(text, max_length=500):

    words = text.split()

    chunks = []

    for i in range(0, len(words), max_length):
        chunks.append(" ".join(words[i:i + max_length]))

    return chunks


def summarize_large_text(text):

    chunks = split_text(text)

    summaries = []

    for chunk in chunks:
        summaries.append(generate_summary(chunk))

    return "\n\n".join(summaries)


def generate_answer(prompt):

    return gemini_answer(prompt)