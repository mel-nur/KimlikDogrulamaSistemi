# 🚀 FaceSecure - Hızlı Başlangıç

## 📦 Tek Tıkla Başlatma

### ▶️ Başlatmak için:
1. **`START_FACESECURE.bat`** dosyasına çift tıklayın
2. 8-10 saniye bekleyin (FaceNet modeli yükleniyor)
3. Tarayıcı otomatik açılacak
4. Login: **admin** / **admin123**

### ⏹️ Durdurmak için:
1. **`STOP_FACESECURE.bat`** dosyasına çift tıklayın
2. Tüm servisler otomatik kapanacak

---

## 🌐 Erişim Bilgileri

| Servis | URL | Açıklama |
|--------|-----|----------|
| **API** | http://localhost:8000 | Flask REST API |
| **Admin Panel** | http://localhost:8501 | Streamlit Arayüzü |
| **API Health** | http://localhost:8000/health | Sistem durumu |

---

## 👤 Giriş Bilgileri

- **Kullanıcı Adı:** `admin`
- **Şifre:** `admin123`

---

## 🎯 Ne Yapabilirsiniz?

### 1️⃣ Kullanıcı Ekleme
- **Dosyadan:** 10+ fotoğraf yükleyin
- **Kameradan:** Canlı fotoğraf çekin (10 adet)

### 2️⃣ Canlı Test
- **Dosyadan:** Fotoğraf yükleyerek test edin
- **Kameradan:** Canlı kamera ile test edin

### 3️⃣ Kullanıcı Yönetimi
- Tüm kullanıcıları görüntüleyin
- Kullanıcı silin
- Embedding sayılarını kontrol edin

### 4️⃣ Ayarlar
- Benzerlik eşiği (threshold) ayarlayın
- Veritabanı yedekleyin

### 5️⃣ Loglar
- Başarısız doğrulama denemelerini görün
- Güvenlik takibi yapın

### 6️⃣ Admin Yönetimi
- Yeni admin kullanıcı ekleyin
- Şifre değiştirin

---

## ⚙️ Teknik Detaylar

### FaceNet Modeli
- **Embedding Boyutu:** 512 boyutlu vektörler
- **Model:** Pre-trained FaceNet (Keras)
- **Güvenlik:** AES-256-GCM + HMAC-SHA256

### Eşik Değeri
- **Varsayılan:** 0.70
- **Aynı Kişi:** 0.85 - 0.95 benzerlik
- **Farklı Kişi:** 0.30 - 0.60 benzerlik

---

## 🛠️ Sorun Giderme

### Port Meşgul Hatası
```batch
STOP_FACESECURE.bat
# 3 saniye bekleyin
START_FACESECURE.bat
```

### Model Yükleme Hatası
- İlk başlatma 10-15 saniye sürebilir (normal)
- FaceNet modeli indiriliyor

### Kamera Çalışmıyor
- Tarayıcıda kamera izni verin
- Başka uygulama kamerayı kullanıyor olabilir

---

## 📝 Notlar

⚠️ **ÖNEMLİ:**
- İlk başlatma yavaş olabilir (FaceNet modeli indiriliyor)
- Veritabanı: `facesecure_data.json` (yedekleyin!)
- Şifreler: `.env` dosyasında (yedekleyin!)

✅ **Güvenlik:**
- Tüm embedding'ler AES-256-GCM ile şifreli
- HMAC-SHA256 veri bütünlüğü kontrolü
- SHA256 şifre hashleme
- JWT token desteği (opsiyonel)

---

## 📚 Sprint Durumu

✅ **Tamamlanan:**
- Sprint 0: Ortam kurulumu
- Sprint 1: Yüz algılama + FaceNet
- Sprint 2: API + Güvenlik
- Sprint 3: Admin Panel + Kamera

⏳ **Sonraki:**
- Sprint 4: Accuracy iyileştirme + Docker
- Sprint 5: Liveness detection + Production

---

## 💡 İpuçları

1. **İlk Kullanıcı Eklerken:**
   - 10-15 farklı açıdan fotoğraf çekin
   - İyi ışık altında fotoğraf çekin
   - Yüzünüz net görünsün

2. **Test Ederken:**
   - Fotoğrafınızı kayıt sırasıyla benzer şekilde çekin
   - Gözlük varsa her iki şekilde de kaydedin

3. **Threshold Ayarı:**
   - Çok düşük (0.5): Güvensiz, yanlış pozitifler
   - Çok yüksek (0.9): Çok katı, gerçek kullanıcılar reddedilebilir
   - Önerilen: **0.70 - 0.75**

---

## 🎉 Başarılar!

FaceSecure ile güvenli yüz tanıma sistemine hoş geldiniz! 🚀
