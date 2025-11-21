# Kütüphane Yönetim Sistemi API

Python ve FastAPI ile geliştirdiğim kütüphane yönetim sistemi projesi.

[![CI/CD & Coverage](https://github.com/UmitKaya038/KutuphaneAPI/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/UmitKaya038/KutuphaneAPI/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/UmitKaya038/KutuphaneAPI/graph/badge.svg?token=2a29c151-2905-42e5-9de8-5508c72e2418)](https://codecov.io/gh/UmitKaya038/KutuphaneAPI)

## Ne İşe Yarar?

Bu API ile kitapları, yazarları, kategorileri ve kullanıcıları yönetebiliyoruz. Ayrıca kim hangi kitabı ne zaman almış, ne zaman geri getirecek gibi ödünç işlemlerini de takip ediyor.

**Temel özellikler:**
*   Kitap, Yazar, Kategori, Kullanıcı ekleme/silme/güncelleme (CRUD).
*   Ödünç alma ve iade etme süreçleri.
*   SQLite veritabanı kullanıyor.
*   Otomatik dokümantasyonu var (Swagger UI).

## Veritabanı Tasarımı (ER Şeması)

```mermaid
erDiagram
    YAZAR ||--o{ KITAP : "yazar"
    KATEGORI ||--o{ KITAP : "kategori"
    KULLANICI ||--o{ ODUNC : "odunc_alir"
    KITAP ||--o{ ODUNC : "odunc_verilir"

    YAZAR {
        int id PK
        string ad
        string soyad
        string biyografi
    }

    KATEGORI {
        int id PK
        string ad
    }

    KITAP {
        int id PK
        string baslik
        string isbn
        int yayin_yili
        int yazar_id FK
        int kategori_id FK
    }

    KULLANICI {
        int id PK
        string ad
        string soyad
        string email
        bool aktif_mi
    }

    ODUNC {
        int id PK
        int kullanici_id FK
        int kitap_id FK
        date alis_tarihi
        date teslim_tarihi
    }
```

## Kurulum

Projeyi çalıştırmak için Python kurulu olması lazım.

1.  Repoyu indirin:
    ```bash
    git clone https://github.com/UmitKaya038/KutuphaneAPI.git
    cd KutuphaneAPI
    ```

2.  Windows kullanıyorsanız direkt `run.bat` dosyasına çift tıklayın veya cmd'den çalıştırabilirsiniz.
    ```cmd
    run.bat
    ```

3.  Elle kurmak isterseniz:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    ```

## Nasıl Kullanılır?

Uygulama ayağa kalkınca tarayıcıdan şuraya gidin:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Buradan bütün endpointleri deneyebilirsiniz.

### Örnek İstekler

**Kitap Ekleme:**
POST `/api/kitaplar/`
```json
{
  "baslik": "İnce Memed",
  "isbn": "978-975-08-0714-7",
  "yayin_yili": 1955,
  "yazar_id": 1,
  "kategori_id": 2
}
```

**Ödünç Verme:**
POST `/api/odunc/`
```json
{
  "kullanici_id": 5,
  "kitap_id": 12,
  "alis_tarihi": "2023-11-20"
}
```

## Testler

Testleri çalıştırmak isterseniz:
```bash
pytest
```
Coverage raporu için:
```bash
pytest --cov=app --cov-report=term-missing
```

## Proje Yapısı
Klasik FastAPI yapısı aslında. `app` klasöründe kodlar, `tests` klasöründe testler var.

```text
KutuphaneAPI/
├── app/
│   ├── routers/      # Endpointler (kitap, yazar vs.)
│   ├── models.py     # Veritabanı tabloları
│   ├── schemas.py    # Veri modelleri
│   ├── main.py       # Uygulamanın başladığı yer
│   └── database.py   # DB bağlantısı
├── tests/            # Testler burada
├── requirements.txt  # Kütüphaneler
└── run.bat           # Çalıştırma betiği
```
