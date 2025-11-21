from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/odunc",
    tags=["Ödünç İşlemleri"]
)

@router.get("/", response_model=List[schemas.OduncResponse])
def get_odunc_kayitlari(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Kayıtları getir
    return db.query(models.OduncKayit).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.OduncResponse, status_code=201)
def create_odunc(odunc: schemas.OduncCreate, db: Session = Depends(get_db)):
    # Kitap müsait mi kontrol et
    aktif_odunc = db.query(models.OduncKayit).filter(
        models.OduncKayit.kitap_id == odunc.kitap_id,
        models.OduncKayit.teslim_tarihi == None
    ).first()
    if aktif_odunc:
        raise HTTPException(status_code=400, detail="Kitap şu an başkasında")

    new_odunc = models.OduncKayit(**odunc.model_dump())
    db.add(new_odunc)
    db.commit()
    db.refresh(new_odunc)
    return new_odunc

@router.get("/{id}", response_model=schemas.OduncResponse)
def get_odunc(id: int, db: Session = Depends(get_db)):
    kayit = db.query(models.OduncKayit).filter(models.OduncKayit.id == id).first()
    if kayit is None:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")
    return kayit

@router.patch("/{id}", response_model=schemas.OduncResponse)
def update_odunc(id: int, odunc_update: schemas.OduncUpdate, db: Session = Depends(get_db)):
    db_odunc = db.query(models.OduncKayit).filter(models.OduncKayit.id == id).first()
    if db_odunc is None:
        raise HTTPException(status_code=404, detail="Ödünç kaydı bulunamadı")
    
    update_data = odunc_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_odunc, key, value)
    
    db.commit()
    db.refresh(db_odunc)
    return db_odunc

@router.delete("/{id}", status_code=204)
def delete_odunc(id: int, db: Session = Depends(get_db)):
    kayit = db.query(models.OduncKayit).filter(models.OduncKayit.id == id).first()
    if kayit is None:
        raise HTTPException(status_code=404, detail="Silinecek kayıt yok")
    db.delete(kayit)
    db.commit()
    return None
