import os
from openai import OpenAI
from dotenv import load_dotenv
from retrieve import retrieve

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def answer_question(question):
    # Step 1: Retrieve relevant chunks
    results = retrieve(question)
    context = "\n\n".join([content for content, similarity in results])

    # Step 2: Build the prompt with context + question
    prompt = f"""You are a helpful HR assistant. Answer the question based only on the provided context. If the answer is not in the context, say "I don't have that information."

Context:
{context}

Question: {question}"""

    # Step 3: Send to the LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    question = input("\nAsk a question: ")
    print(f"\nAnswer: {answer_question(question)}")