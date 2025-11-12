@echo off
chcp 65001 >nul
title FaceSecure - Başlatılıyor...
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              🚀 FACESECURE BAŞLATILIYOR 🚀                ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

set PYTHON_PATH=.venv\Scripts\python.exe

echo [1/3] 📦 Virtual Environment kontrol ediliyor...
if not exist "%PYTHON_PATH%" (
    echo ❌ HATA: Virtual environment bulunamadı!
    echo Beklenen konum: .venv\Scripts\python.exe
    echo.
    echo 💡 Çözüm: Önce virtual environment oluşturun:
    echo    python -m venv .venv
    echo    .venv\Scripts\pip.exe install -r requirements.txt
    pause
    exit /b 1
)
echo ✅ Virtual environment bulundu
echo.

echo [2/3] 🌐 Flask API başlatılıyor (Port 8000)...
start "FaceSecure API" /MIN cmd /k "title FaceSecure API (Port 8000) && color 0B && echo ╔════════════════════════════════════════════╗ && echo ║  FACESECURE API - FLASK SERVER            ║ && echo ║  Port: 8000                               ║ && echo ╚════════════════════════════════════════════╝ && echo. && echo 🔄 FaceNet modeli yükleniyor... && echo. && .venv\Scripts\python.exe api/app.py"
timeout /t 8 /nobreak >nul
echo ✅ API başlatıldı
echo.

echo [3/3] 🎨 Streamlit Admin Panel başlatılıyor (Port 8501)...
start "FaceSecure Admin" /MIN cmd /k "title FaceSecure Admin Panel (Port 8501) && color 0E && echo ╔════════════════════════════════════════════╗ && echo ║  FACESECURE ADMIN PANEL - STREAMLIT       ║ && echo ║  Port: 8501                               ║ && echo ╚════════════════════════════════════════════╝ && echo. && echo 🔄 Admin paneli başlatılıyor... && echo. && .venv\Scripts\python.exe -m streamlit run admin/streamlit_app.py --server.port 8501"
timeout /t 3 /nobreak >nul
echo ✅ Admin panel başlatıldı
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║                 ✅ FACESECURE HAZIR! ✅                   ║
echo ║                                                            ║
echo ║  🌐 API:          http://localhost:8000                   ║
echo ║  🎨 Admin Panel:  http://localhost:8501                   ║
echo ║                                                            ║
echo ║  👤 Giriş:  admin / admin123                              ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 💡 İpucu: API ve Admin Panel ayrı pencererde çalışıyor.
echo 🛑 Kapatmak için: Her iki pencereyi kapatın veya Ctrl+C
echo.

timeout /t 5 >nul
start http://localhost:8501

echo 🌐 Tarayıcı açıldı...
echo.
echo Bu pencereyi kapatabilirsiniz.
timeout /t 3 >nul
