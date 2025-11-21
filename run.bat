@echo off
echo Kutuphane API Baslatiliyor...

if not exist "venv" (
    echo Sanal ortam bulunamadi. Olusturuluyor...
    python -m venv venv
    echo Sanal ortam olusturuldu.
    echo Bagimliliklar yukleniyor...
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

echo Uygulama baslatiliyor...
uvicorn app.main:app --reload
pause
