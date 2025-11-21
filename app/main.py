from fastapi import FastAPI
from .database import engine, Base
from .routers import kitaplar, yazarlar, kategoriler, kullanicilar, odunc

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kütüphane Yönetim Sistemi API",
    description="Kitap, yazar, kategori, kullanıcılar ve ödünç işlemlerini yöneten RESTful API.",
    version="1.0.0"
)

# Router'ları dahil et
app.include_router(kitaplar.router)
app.include_router(yazarlar.router)
app.include_router(kategoriler.router)
app.include_router(kullanicilar.router)
app.include_router(odunc.router)

@app.get("/")
def read_root():
    return {"message": "Kütüphane API'ye Hoşgeldiniz! Dokümantasyon için /docs adresine gidin."}
