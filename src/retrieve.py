import os
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def retrieve(question, top_k=3):
    # Step 1: Turn the question into a vector
    question_embedding = get_embedding(question)

    # Step 2: Connect to the database
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()


    # Step 3: Find the closest chunks using cosine similarity
    cursor.execute("SET ivfflat.probes = 10")
    cursor.execute("""
        SELECT content, 1 - (embedding <=> %s::vector) AS similarity
        FROM document_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (question_embedding, question_embedding, top_k))


    results = cursor.fetchall()
    conn.close()

    return results

if __name__ == "__main__":
    question = "How many vacation days do employees get?"
    results = retrieve(question)

    print(f"Question: {question}\n")
    for i, (content, similarity) in enumerate(results):
        print(f"--- Result {i+1} (similarity: {similarity:.4f}) ---")
        print(content[:200])
        print()