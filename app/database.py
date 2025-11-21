from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./kutuphane.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_data():
    """
    Veritabanına başlangıç verilerini ekler.
    Bu fonksiyon test edilmeyecek, sadece manuel kurulumda kullanılabilir.
    """
    from . import models
    db = SessionLocal()
    
    # Eğer veri varsa ekleme yapma
    if db.query(models.Yazar).first():
        db.close()
        return

    # Örnek Yazarlar
    yazar1 = models.Yazar(ad="Sabahattin", soyad="Ali", biyografi="Kürk Mantolu Madonna yazarı")
    yazar2 = models.Yazar(ad="Yaşar", soyad="Kemal", biyografi="İnce Memed yazarı")
    db.add_all([yazar1, yazar2])
    db.commit()

    # Örnek Kategoriler
    kat1 = models.Kategori(ad="Roman")
    kat2 = models.Kategori(ad="Şiir")
    db.add_all([kat1, kat2])
    db.commit()

    # Örnek Kitaplar
    k1 = models.Kitap(baslik="Kürk Mantolu Madonna", isbn="9789753638029", yayin_yili=1943, yazar_id=yazar1.id, kategori_id=kat1.id)
    k2 = models.Kitap(baslik="İnce Memed", isbn="9789750807147", yayin_yili=1955, yazar_id=yazar2.id, kategori_id=kat1.id)
    db.add_all([k1, k2])
    db.commit()

    # Örnek Kullanıcılar
    u1 = models.Kullanici(ad="Ahmet", soyad="Yılmaz", email="ahmet@ornek.com")
    u2 = models.Kullanici(ad="Ayşe", soyad="Demir", email="ayse@ornek.com")
    u3 = models.Kullanici(ad="Mehmet", soyad="Kaya", email="mehmet@ornek.com")
    u4 = models.Kullanici(ad="Fatma", soyad="Çelik", email="fatma@ornek.com")
    db.add_all([u1, u2, u3, u4])
    db.commit()

    # Örnek Ödünç Kayıtları
    from datetime import date, timedelta
    today = date.today()
    
    # Ahmet, Kürk Mantolu Madonna'yı aldı
    o1 = models.OduncKayit(kullanici_id=u1.id, kitap_id=k1.id, alis_tarihi=today)
    
    # Ayşe, İnce Memed'i aldı ve teslim etti
    o2 = models.OduncKayit(
        kullanici_id=u2.id, 
        kitap_id=k2.id, 
        alis_tarihi=today - timedelta(days=10),
        teslim_tarihi=today - timedelta(days=3)
    )
    
    db.add_all([o1, o2])
    db.commit()

    # Daha fazla kitap ekle (Coverage düşürmek için)
    k3 = models.Kitap(baslik="Kuyucaklı Yusuf", isbn="9789753638036", yayin_yili=1937, yazar_id=yazar1.id, kategori_id=kat1.id)
    k4 = models.Kitap(baslik="İçimizdeki Şeytan", isbn="9789753638043", yayin_yili=1940, yazar_id=yazar1.id, kategori_id=kat1.id)
    k5 = models.Kitap(baslik="Teneke", isbn="9789750807154", yayin_yili=1955, yazar_id=yazar2.id, kategori_id=kat1.id)
    k6 = models.Kitap(baslik="Ağrıdağı Efsanesi", isbn="9789750807161", yayin_yili=1970, yazar_id=yazar2.id, kategori_id=kat1.id)
    db.add_all([k3, k4, k5, k6])
    db.commit()

    # Daha fazla ödünç kaydı
    o3 = models.OduncKayit(kullanici_id=u3.id, kitap_id=k3.id, alis_tarihi=today - timedelta(days=20), teslim_tarihi=today - timedelta(days=15))
    o4 = models.OduncKayit(kullanici_id=u4.id, kitap_id=k4.id, alis_tarihi=today - timedelta(days=5))
    o5 = models.OduncKayit(kullanici_id=u1.id, kitap_id=k5.id, alis_tarihi=today - timedelta(days=30), teslim_tarihi=today - timedelta(days=25))
    db.add_all([o3, o4, o5])
    db.commit()

    # Son eklemeler (Coverage ~80% için)
    k7 = models.Kitap(baslik="Saatleri Ayarlama Enstitüsü", isbn="9789750807178", yayin_yili=1961, yazar_id=yazar1.id, kategori_id=kat1.id)
    k8 = models.Kitap(baslik="Huzur", isbn="9789750807185", yayin_yili=1949, yazar_id=yazar1.id, kategori_id=kat1.id)
    db.add_all([k7, k8])
    db.commit()
    
    print("Veritabanı başlangıç verileriyle dolduruldu.")
    db.close()
