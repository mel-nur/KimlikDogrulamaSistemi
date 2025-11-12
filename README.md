# 🔐 FaceSecure - Gelişmiş Yüz Tanıma Kimlik Doğrulama Sistemi

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0-red.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Güvenli, Hızlı ve Kullanıcı Dostu Yüz Tanıma Sistemi**

[Özellikler](#-özellikler) • [Kurulum](#-kurulum) • [Kullanım](#-kullanım) • [API](#-api-dokümantasyonu) • [Katkıda Bulunma](#-katkıda-bulunma)

</div>

---

## 📋 İçindekiler

- [Hakkında](#-hakkında)
- [Özellikler](#-özellikler)
- [Teknolojiler](#-teknolojiler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [API Dokümantasyonu](#-api-dokümantasyonu)
- [Güvenlik](#-güvenlik)
- [Proje Yapısı](#-proje-yapısı)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

---

## 🎯 Hakkında

**FaceSecure**, modern yüz tanıma teknolojisi kullanarak güvenli kimlik doğrulama sağlayan, açık kaynaklı bir Python projesidir. FaceNet modelini kullanarak %99+ doğruluk oranı ile çalışır ve kurumsal düzeyde güvenlik standartlarını karşılar.

### ✨ Neden FaceSecure?

- 🚀 **Hızlı & Doğru**: FaceNet modeli ile saniyeler içinde yüz tanıma
- 🔒 **Güvenli**: AES-256-GCM şifreleme ve HMAC doğrulama
- 🎨 **Modern Arayüz**: Streamlit ile kullanıcı dostu admin paneli
- 🔌 **API Desteği**: Flask RESTful API ile kolay entegrasyon
- 📊 **Detaylı Raporlama**: Gerçek zamanlı istatistikler ve analizler
- 👥 **Rol Bazlı Erişim**: Admin ve kullanıcı ayrımı

---

## 🚀 Özellikler

### 🔐 Kimlik Doğrulama
- **Yüz Tanıma ile Giriş**: Kamera veya fotoğraf ile anlık kimlik doğrulama
- **Şifre ile Giriş**: Klasik şifre tabanlı giriş alternatifi
- **İkili Yetkilendirme**: Admin ve normal kullanıcı rolleri
- **Akıllı Yönlendirme**: Kullanıcı tipine göre otomatik sayfa yönlendirme

### 📸 Kullanıcı Yönetimi
- **Kolay Kayıt**: Kamera veya dosyadan fotoğraf yükleme
- **Çoklu Fotoğraf**: 10 farklı poz ile yüksek doğruluk
- **Toplu İşlemler**: Birden fazla kullanıcı ekleme/silme
- **Kullanıcı Arama**: Hızlı arama ve filtreleme

### 📊 İstatistikler & Raporlama
- Toplam kullanıcı sayısı
- Başarılı/başarısız giriş denemeleri
- Günlük aktivite grafikleri
- Sistem sağlık durumu

### 🔒 Güvenlik Özellikleri
- **AES-256-GCM Şifreleme**: Yüz verilerinin güvenli saklanması
- **HMAC-SHA256 Doğrulama**: Veri bütünlüğü koruması
- **Threshold Kontrolü**: Ayarlanabilir benzerlik eşiği (varsayılan: 0.7)
- **Güvenli Oturum Yönetimi**: Session bazlı kimlik doğrulama

### 🎨 Kullanıcı Arayüzü
- **Modern Tasarım**: Streamlit ile responsive ve kullanıcı dostu
- **Türkçe Dil Desteği**: Tam Türkçe arayüz
- **Gerçek Zamanlı Görüntüleme**: Anlık kamera önizleme
- **Karanlık/Aydınlık Tema**: Kullanıcı tercihi

---

## 🛠 Teknolojiler

### Backend
- **Python 3.11**: Ana programlama dili
- **Flask 3.1.2**: RESTful API framework
- **FaceNet (keras-facenet)**: Yüz tanıma modeli (512D embeddings)
- **OpenCV 4.10**: Görüntü işleme ve yüz tespiti

### Frontend
- **Streamlit 1.51.0**: Web arayüzü framework
- **Plotly**: İnteraktif grafikler
- **Pillow (PIL)**: Görüntü işleme

### Güvenlik & Veri
- **PyCryptodome**: AES-256-GCM şifreleme
- **HMAC**: Veri bütünlüğü doğrulama
- **JSON**: Veri depolama

### ML & Veri İşleme
- **NumPy**: Sayısal hesaplamalar
- **TensorFlow**: FaceNet model backend
- **scikit-learn**: Cosine similarity hesaplama

---

## 📦 Kurulum

### Gereksinimler

- Python 3.11 veya üzeri
- Kamera (yüz tanıma için)
- 4GB+ RAM önerilir

### Adım 1: Projeyi İndirin

```bash
git clone https://github.com/kullaniciadi/facesecure.git
cd facesecure
```

### Adım 2: Virtual Environment Oluşturun

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
cd facesecure
pip install -r requirements.txt
```

### Adım 4: Sistemin Çalıştığını Doğrulayın

```bash
# Admin panelini başlatın
streamlit run admin/streamlit_app.py

# API'yi başlatın (başka terminal)
python api/app.py
```

---

## 🎮 Kullanım

### Admin Paneli

1. **Sistemi Başlatın:**
   ```bash
   cd facesecure
   streamlit run admin/streamlit_app.py
   ```

2. **Giriş Yapın:**
   - **Varsayılan Admin:**
     - Kullanıcı adı: `admin`
     - Şifre: `admin123`
   
   veya
   
   - Yüz tanıma ile giriş yapın

3. **Kullanıcı Ekleyin:**
   - Sol menüden "👤 Kullanıcı Yönetimi" seçin
   - "➕ Yeni Kullanıcı Ekle" butonuna tıklayın
   - Kamera veya dosyadan fotoğraf yükleyin
   - 10 farklı poz çekin (otomatik)

### API Kullanımı

#### Sunucuyu Başlatın
```bash
python api/app.py
```

API varsayılan olarak `http://localhost:8000` adresinde çalışır.

#### Kullanıcı Kaydı
```python
import requests

url = "http://localhost:8000/api/enroll"
files = {
    'images': [
        open('photo1.jpg', 'rb'),
        open('photo2.jpg', 'rb'),
        # ... 10 fotoğrafa kadar
    ]
}
data = {'username': 'ahmet'}

response = requests.post(url, files=files, data=data)
print(response.json())
```

#### Kimlik Doğrulama
```python
import requests

url = "http://localhost:8000/api/verify"
files = {'image': open('test_photo.jpg', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```

---

## 📚 API Dokümantasyonu

### Endpoints

#### 1. Kullanıcı Kaydı (Enrollment)

**Endpoint:** `POST /api/enroll`

**Parametreler:**
- `username` (string, required): Kullanıcı adı
- `images` (files, required): 1-10 arası fotoğraf

**Başarılı Yanıt:**
```json
{
    "success": true,
    "message": "Kullanıcı başarıyla kaydedildi",
    "user_id": "1",
    "username": "ahmet",
    "photo_count": 10
}
```

#### 2. Kimlik Doğrulama (Verification)

**Endpoint:** `POST /api/verify`

**Parametreler:**
- `image` (file, required): Test fotoğrafı
- `threshold` (float, optional): Benzerlik eşiği (varsayılan: 0.7)

**Başarılı Yanıt:**
```json
{
    "success": true,
    "verified": true,
    "username": "ahmet",
    "similarity": 0.89,
    "is_admin": true
}
```

**Başarısız Yanıt:**
```json
{
    "success": false,
    "verified": false,
    "message": "Yüz tanımlanamadı",
    "best_similarity": 0.45
}
```

---

## 🔒 Güvenlik

### Veri Şifreleme

Tüm yüz verileri (embeddings) şu güvenlik katmanları ile korunur:

1. **AES-256-GCM Şifreleme**: Askeri düzey şifreleme
2. **HMAC-SHA256**: Veri bütünlüğü doğrulama
3. **Rastgele Nonce**: Her şifreleme için benzersiz
4. **Key Derivation**: Güvenli anahtar türetme

### Örnek Veri Yapısı

```json
{
    "encrypted": "base64_encoded_encrypted_data",
    "hmac": "base64_encoded_hmac",
    "pose_index": 0
}
```

### Güvenlik Önerileri

- ✅ Üretim ortamında güçlü şifreler kullanın
- ✅ HTTPS kullanın (SSL/TLS)
- ✅ Düzenli güvenlik güncellemeleri yapın
- ✅ Veritabanı yedeği alın
- ✅ Threshold değerini ortamınıza göre ayarlayın

---

## 📁 Proje Yapısı

```
facesecure/
├── admin/
│   └── streamlit_app.py          # Ana Streamlit uygulaması
├── api/
│   ├── app.py                     # Flask API server
│   └── routes/
│       ├── enroll.py              # Kayıt endpoint
│       └── verify.py              # Doğrulama endpoint
├── face/
│   ├── detector.py                # Yüz tespiti
│   └── processor.py               # FaceNet embedding işleme
├── utils/
│   ├── auth.py                    # Admin yetkilendirme
│   ├── crypto.py                  # Şifreleme/deşifreleme
│   └── db.py                      # Veritabanı yönetimi
├── evaluation/
│   ├── evaluate_model.py          # Model değerlendirme
│   └── dataset_manager.py         # Test dataset yönetimi
├── tests/
│   ├── test_crypto.py             # Şifreleme testleri
│   └── test_embedding.py          # Embedding testleri
├── facesecure_data.json           # Kullanıcı verileri
├── admin_users.json               # Admin kullanıcılar
├── requirements.txt               # Python bağımlılıkları
├── README.md                      # Bu dosya
├── LICENSE                        # MIT Lisansı
└── CHANGELOG.md                   # Sürüm geçmişi
```

---

## 📊 Performans

### Model Özellikleri

- **Model**: FaceNet (InceptionResNetV2)
- **Embedding Boyutu**: 512 boyutlu vektör
- **Doğruluk**: %99+ (LFW dataset)
- **Hız**: ~100ms/fotoğraf (CPU)
- **Benzerlik Metriği**: Cosine similarity

### Sistem Gereksinimleri

| Bileşen | Minimum | Önerilen |
|---------|---------|----------|
| CPU | 2 core | 4+ core |
| RAM | 2GB | 4GB+ |
| Disk | 500MB | 1GB+ |
| Python | 3.11 | 3.11+ |
| Kamera | VGA | HD+ |

---

## 🧪 Test Etme

### Unit Testler

```bash
# Tüm testleri çalıştır
python -m pytest tests/

# Sadece şifreleme testleri
python -m pytest tests/test_crypto.py

# Sadece embedding testleri
python -m pytest tests/test_embedding.py
```

### Model Değerlendirme

```bash
cd evaluation
python evaluate_model.py
```

---

## 🗺 Yol Haritası

- [x] Temel yüz tanıma sistemi
- [x] Admin paneli
- [x] RESTful API
- [x] Şifreleme & güvenlik
- [x] Rol bazlı erişim
- [ ] Liveness detection (canlılık tespiti)
- [ ] Multi-factor authentication (MFA)
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] Mobil uygulama (React Native)
- [ ] Face mask detection
- [ ] Age & emotion detection
- [ ] Cloud deployment (AWS/Azure/GCP)

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Projeye katkıda bulunmak için:

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Katkı Kuralları

- PEP 8 kod standardına uyun
- Değişiklikler için testler ekleyin
- Dokümantasyonu güncelleyin
- Commit mesajlarını açıklayıcı yazın

---

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 👨‍💻 Geliştirici

**Proje Sahibi**: [Ahmet Koç]

---

## 🙏 Teşekkürler

Bu proje aşağıdaki açık kaynak projelerden yararlanmıştır:

- [FaceNet](https://github.com/davidsandberg/facenet) - Yüz tanıma modeli
- [OpenCV](https://opencv.org/) - Görüntü işleme
- [Streamlit](https://streamlit.io/) - Web arayüzü
- [Flask](https://flask.palletsprojects.com/) - RESTful API

---

## 📞 İletişim & Destek

- 📧 Email: [email@example.com]
- 🐛 Bug Report: [GitHub Issues](https://github.com/kullaniciadi/facesecure/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/kullaniciadi/facesecure/discussions)
- 📖 Wiki: [GitHub Wiki](https://github.com/kullaniciadi/facesecure/wiki)

---

## ⭐ Yıldız Grafiği

[![Stargazers over time](https://starchart.cc/kullaniciadi/facesecure.svg)](https://starchart.cc/kullaniciadi/facesecure)

---

<div align="center">

**[⬆ Başa Dön](#-facesecure---gelişmiş-yüz-tanıma-kimlik-doğrulama-sistemi)**

Beğendiyseniz ⭐ vermeyi unutmayın!

Made with ❤️ by [Ahmet Koç]

</div>
