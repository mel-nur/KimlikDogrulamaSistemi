"""
Flask API ana dosyası
"""
from flask import Flask
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Proje root'unu path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# .env dosyasını yükle
load_dotenv()

# Flask app oluştur
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max upload (10+ fotoğraf için)

# Route'ları import et (api. prefix olmadan)
from routes import enroll, verify

# Blueprint'leri kaydet
app.register_blueprint(enroll.bp)
app.register_blueprint(verify.bp)


@app.route('/')
def index():
    """API ana sayfası"""
    return {
        'service': 'FaceSecure API',
        'version': '1.0.0',
        'endpoints': {
            'enroll': '/api/enroll',
            'verify': '/api/verify'
        }
    }


@app.route('/health')
def health():
    """Sağlık kontrolü"""
    return {'status': 'healthy'}

if __name__ == '__main__':
    print("🚀 FaceSecure API başlatılıyor...")
    print("📡 API: http://127.0.0.1:8000")
    app.run(debug=False, host='0.0.0.0', port=8000, use_reloader=False)

