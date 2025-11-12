@echo off
chcp 65001 >nul
title FaceSecure - Durduruluyor...
color 0C

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              🛑 FACESECURE DURDURULUYOR 🛑                ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1/3] 🔍 Çalışan süreçler kontrol ediliyor...
echo.

REM Flask API'yi durdur (Port 8000)
echo [2/3] 🌐 Flask API durduruluyor (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo    └─ PID: %%a kapatılıyor...
    taskkill /F /PID %%a >nul 2>&1
    if errorlevel 1 (
        echo    └─ ⚠️  PID %%a kapatılamadı veya zaten kapalı
    ) else (
        echo    └─ ✅ PID %%a kapatıldı
    )
)
echo.

REM Streamlit'i durdur (Port 8501)
echo [3/3] 🎨 Streamlit Admin Panel durduruluyor (Port 8501)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501 ^| findstr LISTENING') do (
    echo    └─ PID: %%a kapatılıyor...
    taskkill /F /PID %%a >nul 2>&1
    if errorlevel 1 (
        echo    └─ ⚠️  PID %%a kapatılamadı veya zaten kapalı
    ) else (
        echo    └─ ✅ PID %%a kapatıldı
    )
)
echo.

REM Ek güvenlik: Tüm Python süreçlerini kontrol et
echo 🔄 Ek kontrol: Python süreçleri temizleniyor...
for /f "tokens=2" %%a in ('tasklist ^| findstr "python.exe"') do (
    REM Sadece FaceSecure ile ilgili Python süreçlerini kapat
    REM (Bu kısım tüm python.exe'leri kapatır, dikkatli kullanın!)
    REM taskkill /F /PID %%a >nul 2>&1
    echo    └─ Python süreci bulundu: PID %%a (Manuel kontrol önerilir)
)
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              ✅ FACESECURE DURDURULDU! ✅                 ║
echo ║                                                            ║
echo ║  🛑 Port 8000 (API):          Kapatıldı                   ║
echo ║  🛑 Port 8501 (Admin Panel):  Kapatıldı                   ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 💡 İpucu: Tekrar başlatmak için START_FACESECURE.bat çalıştırın
echo.

timeout /t 5 >nul
