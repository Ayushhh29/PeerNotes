# import nltk
# from nltk.tokenize import sent_tokenize

# nltk.download('punkt')


# def generate_quiz(text):

#     sentences = sent_tokenize(text)

#     quiz = []

#     # meaningful sentences only
#     sentences = [s for s in sentences if len(s.split()) > 8][:5]

#     for i, sentence in enumerate(sentences):

#         words = sentence.split()

#         # answer = important keyword
#         answer = words[0]

#         # create blank
#         question = sentence.replace(answer, "_____ ", 1)

#         # fake options
#         options = [
#             answer,
#             "Machine Learning",
#             "Computer Vision",
#             "Neural Network"
#         ]

#         quiz.append(f"""
# Question {i+1}

# {question}

# A. {options[0]}
# B. {options[1]}
# C. {options[2]}
# D. {options[3]}

# Answer: {answer}

# --------------------------------
# """)

#     return "\n".join(quiz)


from services.gemini import generate_quiz as gemini_quiz


def generate_quiz(text):
    """
    Generate quiz using Gemini.
    """

    return gemini_quiz(text)