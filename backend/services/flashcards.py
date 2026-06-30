# import nltk
# from nltk.tokenize import sent_tokenize

# nltk.download('punkt')

# def generate_flashcards(text):

#     sentences = sent_tokenize(text)

#     flashcards = []

#     # Take meaningful sentences
#     sentences = [s for s in sentences if len(s.split()) > 8][:5]

#     for i, sentence in enumerate(sentences):

#         words = sentence.split()

#         # create simple question
#         question = f"What is meant by: {' '.join(words[:6])}...?"

#         answer = sentence

#         flashcards.append(
#             f"""
# Flashcard {i+1}

# Q: {question}

# A: {answer}
# """
#         )

#     return "\n".join(flashcards)

from services.gemini import generate_flashcards as gemini_flashcards


def generate_flashcards(text):
    """
    Generate flashcards using Gemini.
    """

    return gemini_flashcards(text)