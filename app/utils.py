from datetime import date, datetime

def tarih_formatla_turkce(tarih: date) -> str:
    """
    Verilen tarih objesini Türkçe formatında (Gün Ay Yıl) stringe çevirir.
    Örnek: 2023-10-29 -> 29 Ekim 2023
    """
    aylar = {
        1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
        7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
    }
    if not isinstance(tarih, (date, datetime)):
        return ""
    
    return f"{tarih.day} {aylar[tarih.month]} {tarih.year}"

def isbn_dogrula(isbn: str) -> bool:
    """
    Basit bir ISBN-13 doğrulama algoritması.
    Tireleri kaldırır ve 13 haneli olup olmadığını, checksum'ı kontrol eder.
    """
    isbn = isbn.replace("-", "").replace(" ", "")
    
    if len(isbn) != 13:
        return False
        
    if not isbn.isdigit():
        return False
        
    toplam = 0
    for i, digit in enumerate(isbn[:-1]):
        n = int(digit)
        if i % 2 == 0:
            toplam += n
        else:
            toplam += n * 3
            
    kontrol_basamagi = (10 - (toplam % 10)) % 10
    return kontrol_basamagi == int(isbn[-1])

def metin_ozeti_cikar(metin: str, uzunluk: int = 100) -> str:
    """
    Verilen metni belirtilen uzunlukta keser ve sonuna '...' ekler.
    """
    if not metin:
        return ""
        
    if len(metin) <= uzunluk:
        return metin
        
    return metin[:uzunluk] + "..."

def eposta_gizle(email: str) -> str:
    """
    E-posta adresinin bir kısmını yıldızlayarak gizler.
    ornek@email.com -> o****@email.com
    """
    if "@" not in email:
        return email
        
    kullanici, domain = email.split("@")
    if len(kullanici) <= 2:
        return email
        
    gizli_kullanici = kullanici[0] + "*" * (len(kullanici) - 2) + kullanici[-1]
    return f"{gizli_kullanici}@{domain}"

def sifre_gucluluk_kontrolu(sifre: str) -> str:
    """
    Şifrenin gücünü kontrol eder.
    """
    if len(sifre) < 8:
        return "Zayıf: En az 8 karakter olmalı."
    
    has_upper = any(c.isupper() for c in sifre)
    has_lower = any(c.islower() for c in sifre)
    has_digit = any(c.isdigit() for c in sifre)
    
    if has_upper and has_lower and has_digit:
        return "Güçlü"
    elif (has_upper and has_lower) or (has_upper and has_digit) or (has_lower and has_digit):
        return "Orta"
    else:
        return "Zayıf"

def dosya_boyutu_formatla(boyut_bytes: int) -> str:
    """
    Byte cinsinden dosya boyutunu okunabilir formata çevirir.
    """
    for birim in ['B', 'KB', 'MB', 'GB', 'TB']:
        if boyut_bytes < 1024.0:
            return f"{boyut_bytes:.2f} {birim}"
        boyut_bytes /= 1024.0
    return f"{boyut_bytes:.2f} PB"
