import os
from openai import OpenAI # type:ignore
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chunk_text(text, chunk_size=500):
    sentences = text.replace("\n\n", "\n").split("\n")
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += "\n" + sentence
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks


def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


if __name__ == "__main__":
    with open("documents/sample_policy.txt", "r") as f:
        text = f.read()

    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks:\n")

    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} ---")
        print(chunk[:100] + "...")
        print()

    embedding = get_embedding(chunks[0])
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")