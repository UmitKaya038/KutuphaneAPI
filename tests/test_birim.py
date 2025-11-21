import pytest
from datetime import date, timedelta
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app import schemas, models, utils
from app.routers import kitaplar, yazarlar, kategoriler, kullanicilar, odunc
from fastapi import HTTPException


def test_kullanici_email_valid():
    # email kontrolü
    user = schemas.KullaniciCreate(ad="Test", soyad="User", email="test@example.com")
    assert user.email == "test@example.com"

def test_odunc_tarih_valid():
    # tarih mantıklı mı bakıyoruz
    today = date.today()
    tomorrow = today + timedelta(days=1)
    odunc = schemas.OduncCreate(
        kullanici_id=1, kitap_id=1, alis_tarihi=today, teslim_tarihi=tomorrow
    )
    assert odunc.teslim_tarihi == tomorrow

def test_odunc_tarih_invalid():
    # geçmişe teslim tarihi verilemez
    today = date.today()
    yesterday = today - timedelta(days=1)
    with pytest.raises(ValueError) as excinfo:
        schemas.OduncCreate(
            kullanici_id=1, kitap_id=1, alis_tarihi=today, teslim_tarihi=yesterday
        )
    assert "Teslim tarihi alış tarihinden önce olamaz" in str(excinfo.value)

def test_kitap_zorunlu_alanlar():
    """Zorunlu alanlar eksikse hata fırlatmalı"""
    with pytest.raises(ValueError):
        schemas.KitapCreate(baslik="Eksik", isbn="123") # yazar_id eksik

def test_yazar_create_schema():
    """Yazar oluşturma şeması doğru çalışmalı"""
    yazar = schemas.YazarCreate(ad="Orhan", soyad="Pamuk")
    assert yazar.ad == "Orhan"
    assert yazar.biyografi is None


def test_yazar_model_init():
    """Yazar modeli doğru başlatılmalı"""
    yazar = models.Yazar(ad="Ahmet", soyad="Hamdi", biyografi="Yazar")
    assert yazar.ad == "Ahmet"
    assert yazar.soyad == "Hamdi"

def test_kitap_model_init():
    """Kitap modeli doğru başlatılmalı"""
    kitap = models.Kitap(baslik="Kitap", isbn="12345", yayin_yili=2020)
    assert kitap.baslik == "Kitap"
    assert kitap.isbn == "12345"

def test_kullanici_create_default():
    """Kullanıcı oluşturma şemasında aktif_mi varsayılan olarak True olmalı"""
    user = schemas.KullaniciCreate(ad="Ali", soyad="Veli", email="ali@veli.com")
    assert user.aktif_mi is True


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_kitap_listele_bos(mock_db):
    """Veritabanı boşken boş liste dönmeli"""
    mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = []
    result = kitaplar.get_kitaplar(db=mock_db)
    assert result == []

def test_kitap_ekle_basarili(mock_db):
    """Kitap başarıyla eklenmeli"""
    kitap_in = schemas.KitapCreate(baslik="Test", isbn="111", yazar_id=1)
    
    # Mock davranışları
    result = kitaplar.create_kitap(kitap=kitap_in, db=mock_db)
    
    # DB çağrılarını doğrula
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert result.baslik == "Test"

def test_kitap_getir_bulunamadi(mock_db):
    """Olmayan kitap istendiğinde 404 dönmeli"""
    mock_db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        kitaplar.get_kitap(id=999, db=mock_db)
    assert exc.value.status_code == 404

def test_yazar_ekle_basarili(mock_db):
    """Yazar başarıyla eklenmeli"""
    yazar_in = schemas.YazarCreate(ad="Test", soyad="Yazar")
    result = yazarlar.create_yazar(yazar=yazar_in, db=mock_db)
    mock_db.add.assert_called_once()
    assert result.ad == "Test"

def test_kategori_ekle_basarili(mock_db):
    """Kategori başarıyla eklenmeli"""
    kat_in = schemas.KategoriCreate(ad="Bilim")
    result = kategoriler.create_kategori(kategori=kat_in, db=mock_db)
    mock_db.add.assert_called_once()
    assert result.ad == "Bilim"

def test_odunc_sil_bulunamadi(mock_db):
    """Olmayan ödünç kaydı silinirken 404 dönmeli"""
    mock_db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        odunc.delete_odunc(id=999, db=mock_db)
    assert exc.value.status_code == 404

def test_kategori_sil_basarili(mock_db):
    """Kategori başarıyla silinmeli"""
    mock_kategori = models.Kategori(id=1, ad="Silinecek")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_kategori
    
    kategoriler.delete_kategori(id=1, db=mock_db)
    
    mock_db.delete.assert_called_once_with(mock_kategori)
    mock_db.commit.assert_called_once()

def test_kategori_sil_bulunamadi(mock_db):
    """Olmayan kategori silinirken 404 dönmeli"""
    mock_db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        kategoriler.delete_kategori(id=999, db=mock_db)
    assert exc.value.status_code == 404

def test_yazar_sil_basarili(mock_db):
    """Yazar başarıyla silinmeli"""
    mock_yazar = models.Yazar(id=1, ad="Sil", soyad="Yazar")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_yazar
    
    yazarlar.delete_yazar(id=1, db=mock_db)
    
    mock_db.delete.assert_called_once_with(mock_yazar)
    mock_db.commit.assert_called_once()

def test_kullanici_sil_basarili(mock_db):
    """Kullanıcı başarıyla silinmeli"""
    mock_user = models.Kullanici(id=1, ad="Sil", email="s@s.com")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    kullanicilar.delete_kullanici(id=1, db=mock_db)
    
    mock_db.delete.assert_called_once_with(mock_user)
    mock_db.commit.assert_called_once()

# --- YARDIMCI FONKSİYON TESTLERİ (UTILITIES) ---

def test_tarih_formatla():
    # Normal tarih
    d = date(2023, 10, 29)
    assert utils.tarih_formatla_turkce(d) == "29 Ekim 2023"
    
    # Geçersiz tip
    assert utils.tarih_formatla_turkce("invalid") == ""

def test_isbn_dogrula():
    # Geçerli ISBN-13 (Örnek: 978-3-16-148410-0)
    assert utils.isbn_dogrula("978-3-16-148410-0") is True
    # Tiresiz
    assert utils.isbn_dogrula("9783161484100") is True
    # Geçersiz uzunluk
    assert utils.isbn_dogrula("123") is False
    # Checksum hatası
    assert utils.isbn_dogrula("978-975-08-0714-0") is False

def test_metin_ozeti():
    # Kısa metin
    assert utils.metin_ozeti_cikar("kısa", 10) == "kısa"
    # Uzun metin
    text = "Bu çok uzun bir metindir ve kesilmesi gerekmektedir."
    assert utils.metin_ozeti_cikar(text, 10) == "Bu çok uzu..."
    # Boş
    assert utils.metin_ozeti_cikar("") == ""

def test_eposta_gizle():
    # Normal
    assert utils.eposta_gizle("ahmet@mail.com") == "a***t@mail.com"
    # Kısa isim
    assert utils.eposta_gizle("ab@mail.com") == "ab@mail.com"
    # @ yok
    assert utils.eposta_gizle("invalid") == "invalid"

def test_sifre_gucluluk():
    assert utils.sifre_gucluluk_kontrolu("12345") == "Zayıf: En az 8 karakter olmalı."
    assert utils.sifre_gucluluk_kontrolu("sifre123") == "Orta" # Sadece harf ve sayı
    assert utils.sifre_gucluluk_kontrolu("Guclu123") == "Güçlü" # Büyük, küçük, sayı

def test_dosya_boyutu():
    assert utils.dosya_boyutu_formatla(500) == "500.00 B"
    assert utils.dosya_boyutu_formatla(1024) == "1.00 KB"
    assert utils.dosya_boyutu_formatla(1024 * 1024 * 2.5) == "2.50 MB"
