from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/yazarlar",
    tags=["Yazarlar"]
)

@router.get("/", response_model=List[schemas.YazarResponse])
def get_yazarlar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Yazarları getir
    return db.query(models.Yazar).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.YazarResponse, status_code=201)
def create_yazar(yazar: schemas.YazarCreate, db: Session = Depends(get_db)):
    new_yazar = models.Yazar(**yazar.model_dump())
    db.add(new_yazar)
    db.commit()
    db.refresh(new_yazar)
    return new_yazar

@router.get("/{id}", response_model=schemas.YazarDetayResponse)
def get_yazar(id: int, db: Session = Depends(get_db)):
    yazar = db.query(models.Yazar).filter(models.Yazar.id == id).first()
    if yazar is None:
        raise HTTPException(status_code=404, detail="Yazar sistemde yok")
    return yazar

@router.patch("/{id}", response_model=schemas.YazarResponse)
def update_yazar(id: int, yazar_update: schemas.YazarUpdate, db: Session = Depends(get_db)):
    db_yazar = db.query(models.Yazar).filter(models.Yazar.id == id).first()
    if db_yazar is None:
        raise HTTPException(status_code=404, detail="Yazar bulunamadı")
    
    update_data = yazar_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_yazar, key, value)
    
    db.commit()
    db.refresh(db_yazar)
    return db_yazar

@router.delete("/{id}", status_code=204)
def delete_yazar(id: int, db: Session = Depends(get_db)):
    yazar = db.query(models.Yazar).filter(models.Yazar.id == id).first()
    if yazar is None:
        raise HTTPException(status_code=404, detail="Silinecek yazar yok")
    db.delete(yazar)
    db.commit()
    return None
