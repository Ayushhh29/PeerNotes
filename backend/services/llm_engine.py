from transformers import pipeline

print("Loading shared AI model...")

llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

