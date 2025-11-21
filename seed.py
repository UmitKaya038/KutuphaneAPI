from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models
from datetime import date, timedelta

# Veritabanı tablolarını sıfırdan oluştur (Temiz başlangıç için)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def veri_ekle():
    print("Veri girişi başlıyor...")

    # --- KATEGORİLER ---
    kategoriler = [
        models.Kategori(ad="Türk Edebiyatı"),
        models.Kategori(ad="Dünya Klasikleri"),
        models.Kategori(ad="Bilim Kurgu"),
        models.Kategori(ad="Tarih"),
        models.Kategori(ad="Kişisel Gelişim")
    ]
    db.add_all(kategoriler)
    db.commit()
    print(f"{len(kategoriler)} kategori eklendi.")

    # --- YAZARLAR ---
    yazarlar = [
        models.Yazar(ad="Sabahattin", soyad="Ali", biyografi="Kürk Mantolu Madonna'nın yazarı."),
        models.Yazar(ad="Ahmet Hamdi", soyad="Tanpınar", biyografi="Saatleri Ayarlama Enstitüsü ile tanınır."),
        models.Yazar(ad="Fyodor", soyad="Dostoyevski", biyografi="Rus edebiyatının en büyük yazarlarından."),
        models.Yazar(ad="George", soyad="Orwell", biyografi="Distopik romanlarıyla ünlüdür."),
        models.Yazar(ad="İlber", soyad="Ortaylı", biyografi="Türk tarihçi ve yazar.")
    ]
    db.add_all(yazarlar)
    db.commit()
    print(f"{len(yazarlar)} yazar eklendi.")

    # --- KİTAPLAR ---
    # ID'leri veritabanından çekmek yerine sırayla eklediğimiz için index kullanabiliriz
    # Kategoriler: 0:Türk Ed, 1:Dünya K, 2:Bilim K, 3:Tarih, 4:Kişisel G
    # Yazarlar: 0:S.Ali, 1:Tanpınar, 2:Dostoyevski, 3:Orwell, 4:Ortaylı
    
    kitaplar = [
        models.Kitap(baslik="Kürk Mantolu Madonna", isbn="9789753638029", yayin_yili=1943, yazar_id=1, kategori_id=1),
        models.Kitap(baslik="Kuyucaklı Yusuf", isbn="9789753638050", yayin_yili=1937, yazar_id=1, kategori_id=1),
        models.Kitap(baslik="Saatleri Ayarlama Enstitüsü", isbn="9789753638005", yayin_yili=1961, yazar_id=2, kategori_id=1),
        models.Kitap(baslik="Suç ve Ceza", isbn="9789750719387", yayin_yili=1866, yazar_id=3, kategori_id=2),
        models.Kitap(baslik="Karamazov Kardeşler", isbn="9789750719394", yayin_yili=1880, yazar_id=3, kategori_id=2),
        models.Kitap(baslik="1984", isbn="9789750718533", yayin_yili=1949, yazar_id=4, kategori_id=3),
        models.Kitap(baslik="Hayvan Çiftliği", isbn="9789750719380", yayin_yili=1945, yazar_id=4, kategori_id=3),
        models.Kitap(baslik="Bir Ömür Nasıl Yaşanır?", isbn="9786057635117", yayin_yili=2019, yazar_id=5, kategori_id=5)
    ]
    db.add_all(kitaplar)
    db.commit()
    print(f"{len(kitaplar)} kitap eklendi.")

    # --- KULLANICILAR ---
    kullanicilar = [
        models.Kullanici(ad="Ali", soyad="Yılmaz", email="ali.yilmaz@example.com"),
        models.Kullanici(ad="Ayşe", soyad="Demir", email="ayse.demir@example.com"),
        models.Kullanici(ad="Mehmet", soyad="Kaya", email="mehmet.kaya@example.com")
    ]
    db.add_all(kullanicilar)
    db.commit()
    print(f"{len(kullanicilar)} kullanıcı eklendi.")

    # --- ÖDÜNÇ KAYITLARI ---
    odunc_kayitlari = [
        # Ali, Kürk Mantolu Madonna'yı almış, henüz teslim etmemiş
        models.OduncKayit(kullanici_id=1, kitap_id=1, alis_tarihi=date.today() - timedelta(days=5)),
        # Ayşe, 1984'ü almış ve teslim etmiş
        models.OduncKayit(kullanici_id=2, kitap_id=6, alis_tarihi=date.today() - timedelta(days=20), teslim_tarihi=date.today() - timedelta(days=5)),
        # Mehmet, Suç ve Ceza'yı yeni almış
        models.OduncKayit(kullanici_id=3, kitap_id=4, alis_tarihi=date.today())
    ]
    db.add_all(odunc_kayitlari)
    db.commit()
    print(f"{len(odunc_kayitlari)} ödünç kaydı eklendi.")

    print("Veri girişi başarıyla tamamlandı!")

if __name__ == "__main__":
    try:
        veri_ekle()
    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        db.close()
