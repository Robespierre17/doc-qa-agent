import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from ingest import ingest_all_documents
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


load_dotenv()

from answer import answer_question

app = FastAPI(title="Doc QA Agent")

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "running", "service": "Doc QA Agent"}

@app.post("/ask")
def ask(q: Question):
    response = answer_question(q.question)
    return {"question": q.question, "answer": response}

@app.post("/setup")
def setup():
    ingest_all_documents()
    return {"status": "Database initialized and documents ingested"}

@app.post("/ingest")
async def ingest():
    result = ingest_all_documents()
    return {"status": "ok", "result": result}

@app.get("/demo")
def demo():
    return FileResponse(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "index.html"))