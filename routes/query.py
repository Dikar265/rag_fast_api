from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from utils.embeddings import generate_embedding
from sqlalchemy import text, bindparam
from pgvector.sqlalchemy import Vector
import ollama
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST")

ollama_client = ollama.Client(host=OLLAMA_HOST)

router = APIRouter(
    prefix="/query",
    tags=["Ask About Diseases"]
)

@router.get("/{disease_id}/")
async def ask_question(disease_id: int, question: str, db: Session = Depends(get_db)):
    query_embedding = generate_embedding(question)

    stmt = text("""
        SELECT text_chunk, embedding <-> :query_embedding AS distance
        FROM diaseases_pdf_chunks
        WHERE pdf_id = :disease_id
        ORDER BY distance
        LIMIT 5
    """).bindparams(bindparam("query_embedding", type_=Vector(len(query_embedding))))

    result = db.execute(stmt, {"query_embedding": query_embedding, "disease_id": disease_id}).fetchall()

    if not result:
        return {"message": "No relevant chunks found."}
    
    context = "\n".join([row[0] for row in result])

    prompt = f"""
    Use the following information as context to answer the question.
    Context: {context}
    Question: {question}

    Answer:
    """

    response = ollama_client.chat(
        model="mistral",
        messages=[
        {"role": "user", "content": prompt}
    ])

    return {
        "question": question,
        "answer": response["message"]["content"],
        #"context": context
    }