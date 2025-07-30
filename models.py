from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, Text
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
from database import Base

class Diseases(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    pdf = Column(LargeBinary, nullable=False)

    chunks = relationship("Diaseases_Pdf_Chunks", back_populates="disease", cascade="all, delete")
    
class Diaseases_Pdf_Chunks(Base):
    __tablename__ = "diaseases_pdf_chunks"

    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(Integer, ForeignKey('diseases.id', ondelete='CASCADE'), nullable=False)
    embedding = Column(Vector(768))
    text_chunk  = Column(Text)

    disease = relationship("Diseases", back_populates="chunks")