import os
import glob
import psycopg2
from dotenv import load_dotenv
from embed import chunk_text, get_embedding

load_dotenv()

def ingest_all_documents():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            source TEXT,
            content TEXT,
            embedding vector(1536)
        )
    """)

    # Clear old data so we can re-ingest cleanly
    cursor.execute("DELETE FROM document_chunks")

    # Find all .txt files in the documents folder
    files = glob.glob(os.path.join(os.path.dirname(__file__), "..", "documents", "*.txt"))
    print(f"Found {len(files)} documents\n")

    total_chunks = 0
    for filepath in files:
        filename = os.path.basename(filepath)
        with open(filepath, "r") as f:
            text = f.read()

        chunks = chunk_text(text)
        print(f"{filename}: {len(chunks)} chunks")

        for chunk in chunks:
            embedding = get_embedding(chunk)
            cursor.execute(
                "INSERT INTO document_chunks (source, content, embedding) VALUES (%s, %s, %s)",
                (filename, chunk, embedding)
            )
            total_chunks += 1

    conn.commit()
    conn.close()
    print(f"\nDone! Ingested {total_chunks} chunks total.")

if __name__ == "__main__":
    ingest_all_documents()
