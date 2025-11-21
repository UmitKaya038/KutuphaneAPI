from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/kitaplar",
    tags=["Kitaplar"]
)

@router.get("/", response_model=List[schemas.KitapResponse])
def get_kitaplar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Tüm kitapları çekelim
    query = db.query(models.Kitap)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.KitapResponse, status_code=201)
def create_kitap(kitap: schemas.KitapCreate, db: Session = Depends(get_db)):
    new_kitap = models.Kitap(**kitap.model_dump())
    db.add(new_kitap)
    db.commit()
    db.refresh(new_kitap)
    return new_kitap

@router.get("/{id}", response_model=schemas.KitapResponse)
def get_kitap(id: int, db: Session = Depends(get_db)):
    k = db.query(models.Kitap).filter(models.Kitap.id == id).first()
    if k is None:
        raise HTTPException(status_code=404, detail="Aradığınız kitap sistemde yok")
    return k

@router.patch("/{id}", response_model=schemas.KitapResponse)
def update_kitap(id: int, kitap_update: schemas.KitapUpdate, db: Session = Depends(get_db)):
    db_kitap = db.query(models.Kitap).filter(models.Kitap.id == id).first()
    if db_kitap is None:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    
    update_data = kitap_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_kitap, key, value)
    
    db.commit()
    db.refresh(db_kitap)
    return db_kitap

@router.delete("/{id}", status_code=204)
def delete_kitap(id: int, db: Session = Depends(get_db)):
    k = db.query(models.Kitap).filter(models.Kitap.id == id).first()
    if k is None:
        raise HTTPException(status_code=404, detail="Silinecek kitap bulunamadı")
    
    db.delete(k)
    db.commit()
    return None
