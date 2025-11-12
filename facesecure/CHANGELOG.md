# 📋 Changelog

Tüm önemli değişiklikler bu dosyada belgelenir.

## [1.0.0] - 2025-11-12

### ✨ Yeni Özellikler
- 🎉 **FaceNet modeli entegrasyonu** - Gerçek 512d embeddings
- 📸 **Karma fotoğraf ekleme** - Dosya + kamera aynı anda
- 🎨 **Streamlit admin panel** - Full-featured UI
- 🔐 **AES-256-GCM encryption** - Güvenli embedding storage
- 🔑 **HMAC-SHA256 integrity** - Data corruption prevention
- 📊 **Dashboard** - Real-time statistics
- 🧪 **Live testing** - Camera/file verification
- 📝 **Log viewer** - Failed attempts tracking
- ⚙️ **Settings panel** - Threshold configuration
- 👥 **User management** - Add/delete/list users
- 🔒 **Admin authentication** - SHA256 password hashing
- 🚀 **Auto-start scripts** - START_FACESECURE.bat
- 🛑 **Auto-stop scripts** - STOP_FACESECURE.bat

### 🔧 İyileştirmeler
- ✅ Çoklu yüz algılama koruması
- ✅ IP tracking (failed attempts)
- ✅ Timestamp logging
- ✅ Cosine similarity matching
- ✅ L2 normalization
- ✅ 10+ foto gerekliliği
- ✅ Real-time camera integration
- ✅ Multi-pose support

### 🐛 Düzeltilen Hatalar
- ✅ keras_facenet import hatası (dependency çakışmaları)
- ✅ numpy version uyumsuzluğu
- ✅ TensorFlow 2.20.0 compatibility
- ✅ File upload 16MB limiti → 100MB
- ✅ API endpoint path (/enroll → /api/enroll)
- ✅ Session state photo persistence

### 🧪 Testler
- ✅ 17/17 unit test passing
- ✅ Crypto encryption/decryption
- ✅ Embedding generation/similarity
- ✅ API endpoint validation
- ✅ Admin authentication

### 📚 Dokümantasyon
- ✅ README.md (comprehensive)
- ✅ HIZLI_BASLANGIC.md (quick start)
- ✅ LICENSE (MIT)
- ✅ Code comments (Turkish)
- ✅ API documentation
- ✅ Admin panel help texts

---

## [0.3.0] - Sprint 3: Admin Panel

### ✨ Eklenenler
- Streamlit admin panel
- Login sistemi
- Dashboard sayfası
- Kullanıcı yönetimi
- Kamera entegrasyonu
- Canlı test özelliği
- Threshold ayarlama
- Log görüntüleme

---

## [0.2.0] - Sprint 2: API Development

### ✨ Eklenenler
- Flask REST API
- POST /api/enroll endpoint
- POST /api/verify endpoint
- GET /health endpoint
- AES-GCM encryption
- HMAC integrity check
- JSON file database
- Failed attempt logging

---

## [0.1.0] - Sprint 1: Face Detection

### ✨ Eklenenler
- OpenCV Haar Cascade face detection
- FaceNet stub embeddings (128d)
- L2 normalization
- Cosine similarity
- Basic unit tests

---

## [0.0.1] - Sprint 0: Setup

### ✨ Eklenenler
- Proje yapısı
- Virtual environment
- Requirements.txt
- .env configuration
- Crypto key generation

---

**Notasyon:**
- ✨ Yeni özellik
- 🔧 İyileştirme
- 🐛 Bug fix
- 🧪 Test
- 📚 Dokümantasyon
- ⚠️ Deprecation
- 🔒 Güvenlik
