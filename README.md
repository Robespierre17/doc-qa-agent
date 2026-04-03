# Doc QA Agent

A RAG-powered Q&A agent that answers questions about HR policy documents using semantic search, cosine similarity, and tool-calling capabilities. Deployed live on Railway.

**Live API:** [doc-qa-agent-production.up.railway.app](https://doc-qa-agent-production.up.railway.app)

## How It Works

Documents are chunked and embedded into vectors, then stored in PostgreSQL using pgvector. When a user asks a question, the query is embedded and matched against stored chunks using cosine similarity. The most relevant chunks are injected into a prompt with guardrails, and the LLM generates a grounded answer. The agent can also call tools for search and calculation tasks.

## Tech Stack

- **Python / FastAPI** — API framework with /ask and /ingest endpoints
- **PostgreSQL + pgvector** — Vector storage and semantic search
- **OpenAI API** — Embeddings and LLM completions
- **Railway** — Cloud deployment with CI/CD from GitHub

## Project Structure

- `src/embed.py` — Document chunking and embedding
- `src/ingest.py` — Multi-document ingestion into PostgreSQL with pgvector
- `src/retrieve.py` — Semantic search with cosine similarity
- `src/answer.py` — Prompt assembly with guardrails
- `src/agent.py` — AI agent with search and calculation tools
- `src/main.py` — FastAPI app with /ask, /ingest, and /setup endpoints

## Example

**Request:**
POST /ask
{"question": "How many sick days do employees get?"}

**Response:**
{"question": "How many sick days do employees get?", "answer": "Employees receive 10 days of paid sick leave per year."}

## What I Learned

- Building a full RAG pipeline from chunking to retrieval to generation
- Working with vector embeddings and pgvector for semantic search
- Designing an AI agent with tool use capabilities
- Deploying a Python API with a PostgreSQL database on Railway
