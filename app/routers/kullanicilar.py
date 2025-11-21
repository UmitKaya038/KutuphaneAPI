from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/kullanicilar",
    tags=["Kullanıcılar"]
)

@router.get("/", response_model=List[schemas.KullaniciResponse])
def get_kullanicilar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Listeyi çek
    return db.query(models.Kullanici).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.KullaniciResponse, status_code=201)
def create_kullanici(kullanici: schemas.KullaniciCreate, db: Session = Depends(get_db)):
    new_user = models.Kullanici(**kullanici.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.KullaniciResponse)
def get_kullanici(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Kullanici).filter(models.Kullanici.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Böyle bir kullanıcı yok")
    return user

@router.patch("/{id}", response_model=schemas.KullaniciResponse)
def update_kullanici(id: int, kullanici_update: schemas.KullaniciUpdate, db: Session = Depends(get_db)):
    db_kullanici = db.query(models.Kullanici).filter(models.Kullanici.id == id).first()
    if db_kullanici is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    update_data = kullanici_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_kullanici, key, value)
    
    db.commit()
    db.refresh(db_kullanici)
    return db_kullanici

@router.delete("/{id}", status_code=204)
def delete_kullanici(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Kullanici).filter(models.Kullanici.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Silinecek kullanıcı yok")
    db.delete(user)
    db.commit()
    return None
