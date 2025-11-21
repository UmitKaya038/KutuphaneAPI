from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class Yazar(Base):
    __tablename__ = "yazarlar"

    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, index=True, nullable=False)
    soyad = Column(String, index=True, nullable=False)
    biyografi = Column(String, nullable=True)

    # yazar silinirse kitapları da gitsin
    kitaplar = relationship("Kitap", back_populates="yazar", cascade="all, delete")

class Kategori(Base):
    __tablename__ = "kategoriler"

    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, unique=True, index=True, nullable=False)

    kitaplar = relationship("Kitap", back_populates="kategori")

class Kitap(Base):
    __tablename__ = "kitaplar"

    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String, index=True, nullable=False)
    isbn = Column(String, unique=True, index=True, nullable=False)
    yayin_yili = Column(Integer, nullable=True)
    yazar_id = Column(Integer, ForeignKey("yazarlar.id"))
    kategori_id = Column(Integer, ForeignKey("kategoriler.id"), nullable=True)

    yazar = relationship("Yazar", back_populates="kitaplar")
    kategori = relationship("Kategori", back_populates="kitaplar")
    odunc_kayitlari = relationship("OduncKayit", back_populates="kitap", cascade="all, delete")

class Kullanici(Base):
    __tablename__ = "kullanicilar"

    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, index=True, nullable=False)
    soyad = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    aktif_mi = Column(Boolean, default=True)

    odunc_kayitlari = relationship("OduncKayit", back_populates="kullanici", cascade="all, delete")

class OduncKayit(Base):
    __tablename__ = "odunc_kayitlari"

    id = Column(Integer, primary_key=True, index=True)
    kullanici_id = Column(Integer, ForeignKey("kullanicilar.id"))
    kitap_id = Column(Integer, ForeignKey("kitaplar.id"))
    alis_tarihi = Column(Date, nullable=False)
    teslim_tarihi = Column(Date, nullable=True) # Null ise henüz teslim edilmemiş

    kullanici = relationship("Kullanici", back_populates="odunc_kayitlari")
    kitap = relationship("Kitap", back_populates="odunc_kayitlari")
