from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/kategoriler",
    tags=["Kategoriler"]
)

@router.get("/", response_model=List[schemas.KategoriResponse])
def get_kategoriler(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Kategorileri listele
    return db.query(models.Kategori).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.KategoriResponse, status_code=201)
def create_kategori(kategori: schemas.KategoriCreate, db: Session = Depends(get_db)):
    new_kat = models.Kategori(**kategori.model_dump())
    db.add(new_kat)
    db.commit()
    db.refresh(new_kat)
    return new_kat

@router.get("/{id}", response_model=schemas.KategoriResponse)
def get_kategori(id: int, db: Session = Depends(get_db)):
    kat = db.query(models.Kategori).filter(models.Kategori.id == id).first()
    if kat is None:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    return kat

@router.patch("/{id}", response_model=schemas.KategoriResponse)
def update_kategori(id: int, kategori_update: schemas.KategoriUpdate, db: Session = Depends(get_db)):
    db_kategori = db.query(models.Kategori).filter(models.Kategori.id == id).first()
    if db_kategori is None:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    
    update_data = kategori_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_kategori, key, value)
    
    db.commit()
    db.refresh(db_kategori)
    return db_kategori

@router.delete("/{id}", status_code=204)
def delete_kategori(id: int, db: Session = Depends(get_db)):
    kat = db.query(models.Kategori).filter(models.Kategori.id == id).first()
    if kat is None:
        raise HTTPException(status_code=404, detail="Silinecek kategori yok")
    db.delete(kat)
    db.commit()
    return None
