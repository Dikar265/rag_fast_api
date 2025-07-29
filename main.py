from fastapi import FastAPI
from database import engine, Base
from routes import query, upload
from sqlalchemy import text

app = FastAPI(title="RAG FastAPI", description="API for managing diseases and their PDFs with embeddings")

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()
    
Base.metadata.create_all(bind=engine)

app.include_router(upload.router)
app.include_router(query.router)  