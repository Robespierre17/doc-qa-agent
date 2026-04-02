import os
import psycopg2
from dotenv import load_dotenv
from embed import chunk_text, get_embedding

load_dotenv()


def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def setup_schema(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS document_chunks (
                id SERIAL PRIMARY KEY,
                source TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding vector(1536) NOT NULL
            );
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx
            ON document_chunks
            USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 10);
        """)
    conn.commit()


def ingest_file(filepath: str, conn):
    source = os.path.basename(filepath)

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM document_chunks WHERE source = %s", (source,))
        if cur.fetchone()[0] > 0:
            print(f"'{source}' already ingested, skipping.")
            return

    with open(filepath, "r") as f:
        text = f.read()

    chunks = chunk_text(text)
    print(f"Ingesting '{source}': {len(chunks)} chunks...")

    with conn.cursor() as cur:
        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            cur.execute(
                "INSERT INTO document_chunks (source, content, embedding) VALUES (%s, %s, %s)",
                (source, chunk, embedding),
            )
            print(f"  Stored chunk {i + 1}/{len(chunks)}")
    conn.commit()
    print(f"Done.")


if __name__ == "__main__":
    conn = get_conn()
    setup_schema(conn)
    ingest_file("documents/sample_policy.txt", conn)
    conn.close()
