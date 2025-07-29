from pydantic import BaseModel

class DiseasesCreate(BaseModel):
    nombre: str

class DiseasesResponse(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True
