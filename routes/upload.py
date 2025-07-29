from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import Diseases, Diaseases_Pdf_Chunks
from utils.pdf_utils import extract_text_from_pdf
from utils.embeddings import generate_embedding
from utils.text_utils import chunk_text

router = APIRouter(
    prefix="/Diaseases",
    tags=["Diaseases"]
)

@router.post("/")
async def upload_pdf(name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    diseases = Diseases(name=name, pdf=pdf_bytes)
    db.add(diseases)
    db.commit()
    db.refresh(diseases)

    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = generate_embedding(chunk)
        chunk_record = Diaseases_Pdf_Chunks(
            pdf_id=diseases.id,
            text_chunk=chunk,
            embedding=embedding
        )
        db.add(chunk_record)

    db.commit()

    return {"id": diseases.id, "name": diseases.name, "chunks_saved": len(chunks)}

@router.get("/")
def list_pdfs(db: Session = Depends(get_db)):
    pdfs = db.execute(select(Diseases)).scalars().all()
    return [{"id": pdf.id, "name": pdf.name, "chunks": len(pdf.chunks)} for pdf in pdfs]


@router.get("/{pdf_id}/")
def get_pdf(pdf_id: int, db: Session = Depends(get_db)):
    pdf = db.get(Diseases, pdf_id)
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF no finded")
    return {"id": pdf.id, "name": pdf.name, "chunks": len(pdf.chunks)}


@router.put("/pdfs/{pdf_id}/")
async def update_pdf(
    pdf_id: int, 
    name: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    pdf = db.get(Diseases, pdf_id)
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF no finded")
    
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    pdf.name = name
    pdf.pdf = pdf_bytes

    db.query(Diaseases_Pdf_Chunks).filter(Diaseases_Pdf_Chunks.pdf_id == pdf.id).delete()

    chunks = chunk_text(text)
    for chunk in chunks:
        embedding = generate_embedding(chunk)
        chunk_record = Diaseases_Pdf_Chunks(
            pdf_id=pdf.id,
            text_chunk=chunk,
            embedding=embedding
        )
        db.add(chunk_record)

    db.commit()
    db.refresh(pdf)

    return {
        "message": "PDF updated successfully",
        "id": pdf.id,
        "name": pdf.name,
        "chunks_guardados": len(chunks)
    }

@router.delete("/{pdf_id}/")
def delete_pdf(pdf_id: int, db: Session = Depends(get_db)):
    pdf = db.get(Diseases, pdf_id)
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF no finded")
    
    db.delete(pdf)
    db.commit()
    return {"message": f"PDF with id {pdf_id} deleted successfully."}
