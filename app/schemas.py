from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional
from datetime import date

# --- Yazar Şemaları ---
class YazarBase(BaseModel):
    ad: str = Field(..., description="Yazarın adı", json_schema_extra={"example": "Orhan"})
    soyad: str = Field(..., description="Yazarın soyadı", json_schema_extra={"example": "Pamuk"})
    biyografi: Optional[str] = Field(None, description="Yazar hakkında kısa bilgi", json_schema_extra={"example": "Nobel ödüllü Türk yazar."})

class YazarCreate(YazarBase):
    pass

class YazarUpdate(BaseModel):
    ad: Optional[str] = Field(None, description="Yazarın adı")
    soyad: Optional[str] = Field(None, description="Yazarın soyadı")
    biyografi: Optional[str] = Field(None, description="Yazar hakkında kısa bilgi")

class YazarResponse(YazarBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Kategori Şemaları ---
class KategoriBase(BaseModel):
    ad: str = Field(..., description="Kategori adı", json_schema_extra={"example": "Bilim Kurgu"})

class KategoriCreate(KategoriBase):
    pass

class KategoriUpdate(BaseModel):
    ad: Optional[str] = Field(None, description="Kategori adı")

class KategoriResponse(KategoriBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Kitap Şemaları ---
class KitapBase(BaseModel):
    baslik: str = Field(..., description="Kitabın başlığı", json_schema_extra={"example": "Masumiyet Müzesi"})
    isbn: str = Field(..., description="Kitabın ISBN numarası", json_schema_extra={"example": "9789750506093"})
    yayin_yili: Optional[int] = Field(None, description="Kitabın yayınlandığı yıl", json_schema_extra={"example": 2008})
    yazar_id: int = Field(..., description="Kitabın yazarının ID'si", json_schema_extra={"example": 1})
    kategori_id: Optional[int] = Field(None, description="Kitabın kategorisinin ID'si", json_schema_extra={"example": 1})

class KitapCreate(KitapBase):
    pass

class KitapUpdate(BaseModel):
    baslik: Optional[str] = Field(None, description="Kitabın başlığı")
    isbn: Optional[str] = Field(None, description="Kitabın ISBN numarası")
    yayin_yili: Optional[int] = Field(None, description="Kitabın yayınlandığı yıl")
    yazar_id: Optional[int] = Field(None, description="Kitabın yazarının ID'si")
    kategori_id: Optional[int] = Field(None, description="Kitabın kategorisinin ID'si")

class KitapResponse(KitapBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Kullanıcı Şemaları ---
class KullaniciBase(BaseModel):
    ad: str = Field(..., description="Kullanıcının adı", json_schema_extra={"example": "Ahmet"})
    soyad: str = Field(..., description="Kullanıcının soyadı", json_schema_extra={"example": "Yılmaz"})
    email: str = Field(..., description="Kullanıcının e-posta adresi", json_schema_extra={"example": "ahmet.yilmaz@example.com"})
    aktif_mi: bool = Field(True, description="Kullanıcının aktiflik durumu")

class KullaniciCreate(KullaniciBase):
    pass

class KullaniciUpdate(BaseModel):
    ad: Optional[str] = Field(None, description="Kullanıcının adı")
    soyad: Optional[str] = Field(None, description="Kullanıcının soyadı")
    email: Optional[str] = Field(None, description="Kullanıcının e-posta adresi")
    aktif_mi: Optional[bool] = Field(None, description="Kullanıcının aktiflik durumu")

class KullaniciResponse(KullaniciBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Ödünç Kaydı Şemaları ---
class OduncBase(BaseModel):
    kullanici_id: int = Field(..., description="Kitabı alan kullanıcının ID'si")
    kitap_id: int = Field(..., description="Ödünç alınan kitabın ID'si")
    alis_tarihi: date = Field(..., description="Kitabın alındığı tarih")
    teslim_tarihi: Optional[date] = Field(None, description="Kitabın teslim edildiği tarih (Henüz teslim edilmediyse boş bırakın)")

    @field_validator('teslim_tarihi')
    @classmethod
    def teslim_tarihi_kontrol(cls, v, info):
        if v and 'alis_tarihi' in info.data:
            if v < info.data['alis_tarihi']:
                raise ValueError('Teslim tarihi alış tarihinden önce olamaz')
        return v

class OduncCreate(OduncBase):
    pass

class OduncUpdate(BaseModel):
    kullanici_id: Optional[int] = Field(None, description="Kullanıcının ID'si")
    kitap_id: Optional[int] = Field(None, description="Kitabın ID'si")
    alis_tarihi: Optional[date] = Field(None, description="Alış tarihi")
    teslim_tarihi: Optional[date] = Field(None, description="Teslim tarihi")

class OduncResponse(OduncBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# İlişkileri göstermek için genişletilmiş şemalar
class YazarDetayResponse(YazarResponse):
    kitaplar: List[KitapResponse] = []
