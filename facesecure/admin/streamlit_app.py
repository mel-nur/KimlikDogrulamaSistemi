"""
FaceSecure Admin Panel - Streamlit Arayüzü
"""
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json
from pathlib import Path
import sys
import os
import time

# Proje root'unu path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.db import DBManager
from utils.auth import AdminAuthManager
from dotenv import load_dotenv

load_dotenv()

# Sayfa yapılandırması
st.set_page_config(
    page_title="FaceSecure Admin Panel",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API URL
API_URL = "http://127.0.0.1:8000"

# Veritabanı ve auth yöneticisi
@st.cache_resource
def get_db_manager():
    return DBManager(os.getenv('MONGO_URI'))

@st.cache_resource
def get_auth_manager():
    return AdminAuthManager("admin_users.json")

db = get_db_manager()
auth = get_auth_manager()


# Session state başlatma
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None


def check_api_health():
    """API'nin çalışıp çalışmadığını kontrol et"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def get_statistics():
    """Sistem istatistiklerini getir"""
    users = db.get_all_users()
    
    total_users = len(users)
    total_embeddings = sum(len(user.get('embeddings', [])) for user in users)
    
    # Failed attempts
    data = json.load(open(db.json_path, 'r', encoding='utf-8'))
    failed_attempts = len(data.get('failed_attempts', []))
    
    return {
        'total_users': total_users,
        'total_embeddings': total_embeddings,
        'failed_attempts': failed_attempts
    }


def main():
    # Login kontrolü
    if not st.session_state.logged_in:
        show_login()
        return
    
    # Header
    st.title("🔐 FaceSecure Admin Panel")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Menü")
        
        # Kullanıcı bilgisi
        st.success(f"👤 {st.session_state.username}")
        
        page = st.radio(
            "Sayfa Seçin",
            ["📊 Dashboard", "👥 Kullanıcı Yönetimi", "➕ Kullanıcı Ekle", "🎚️ Ayarlar", "📈 Loglar", "🧪 Canlı Test", "🔐 Admin Yönetimi"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Logout butonu
        if st.button("🚪 Çıkış Yap", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        
        st.markdown("---")
        
        # API Durumu
        api_status = check_api_health()
        if api_status:
            st.success("✅ API Çalışıyor")
        else:
            st.error("❌ API Çalışmıyor")
        
        st.markdown("---")
        st.caption("FaceSecure v1.0.0")
    
    # Ana içerik
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "👥 Kullanıcı Yönetimi":
        show_user_management()
    elif page == "➕ Kullanıcı Ekle":
        show_add_user()
    elif page == "🎚️ Ayarlar":
        show_settings()
    elif page == "📈 Loglar":
        show_logs()
    elif page == "🧪 Canlı Test":
        show_live_test()
    elif page == "🔐 Admin Yönetimi":
        show_admin_management()


def show_login():
    """Login sayfası"""
    st.title("🔐 FaceSecure Admin Panel")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.header("🔑 Giriş Yap")
        
        with st.form("login_form"):
            username = st.text_input("👤 Kullanıcı Adı")
            password = st.text_input("🔒 Şifre", type="password")
            
            submit = st.form_submit_button("🚀 Giriş Yap", type="primary", use_container_width=True)
            
            if submit:
                if username and password:
                    if auth.authenticate(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("✅ Giriş başarılı!")
                        st.rerun()
                    else:
                        st.error("❌ Kullanıcı adı veya şifre hatalı!")
                else:
                    st.warning("⚠️ Tüm alanları doldurun!")
        
        st.info("ℹ️ Default: `admin` / `admin123`")


def show_dashboard():
    """Dashboard sayfası"""
    st.header("📊 Sistem Özeti")
    
    # İstatistikler
    stats = get_statistics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👥 Toplam Kullanıcı", stats['total_users'])
    
    with col2:
        st.metric("🧬 Toplam Embedding", stats['total_embeddings'])
    
    with col3:
        st.metric("❌ Başarısız Deneme", stats['failed_attempts'])
    
    st.markdown("---")
    
    # Kullanıcı listesi
    st.subheader("📋 Kayıtlı Kullanıcılar")
    users = db.get_all_users()
    
    if users:
        user_data = []
        for user in users:
            user_data.append({
                'Kullanıcı Adı': user['username'],
                'Embedding Sayısı': len(user.get('embeddings', [])),
                'Kayıt Tarihi': user.get('created_at', 'N/A')[:19],
                'Son Güncelleme': user.get('updated_at', 'N/A')[:19]
            })
        
        df = pd.DataFrame(user_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Henüz kayıtlı kullanıcı yok")


def show_user_management():
    """Kullanıcı yönetimi sayfası"""
    st.header("👥 Kullanıcı Yönetimi")
    
    # Yenile butonu
    if st.button("🔄 Yenile", type="secondary"):
        st.cache_resource.clear()
        st.rerun()
    
    users = db.get_all_users()
    
    if not users:
        st.info("Henüz kayıtlı kullanıcı yok")
        return
    
    # Her kullanıcı için kart
    for user in users:
        with st.expander(f"👤 {user['username']}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**User ID:** {user.get('_id', 'N/A')}")
                st.write(f"**Embedding Sayısı:** {len(user.get('embeddings', []))}")
                st.write(f"**Kayıt Tarihi:** {user.get('created_at', 'N/A')[:19]}")
                st.write(f"**Son Güncelleme:** {user.get('updated_at', 'N/A')[:19]}")
            
            with col2:
                if st.button(f"🗑️ Sil", key=f"delete_{user['username']}", type="primary"):
                    if st.session_state.get(f"confirm_delete_{user['username']}", False):
                        # Silme onaylandı
                        success = db.delete_user(user['username'])
                        if success:
                            st.success(f"✅ {user['username']} silindi!")
                            st.cache_resource.clear()
                            st.rerun()
                        else:
                            st.error("❌ Silme başarısız!")
                    else:
                        # Onay iste
                        st.session_state[f"confirm_delete_{user['username']}"] = True
                        st.warning("⚠️ Tekrar tıklayarak onaylayın")


def show_add_user():
    """Yeni yüz tanıma kullanıcısı ekleme sayfası"""
    st.header("➕ Yeni Kullanıcı Ekle")
    st.write("Yüz tanıma sistemi için yeni kullanıcı kaydedin")
    
    # API kontrolü
    if not check_api_health():
        st.error("❌ API çalışmıyor! Lütfen önce API'yi başlatın.")
        st.code("cd facesecure\n.\\start_api.bat", language="bash")
        return
    
    # Session state'de fotoğraf listesi (TÜM FOTOĞRAFLAR BURADA)
    if 'all_photos' not in st.session_state:
        st.session_state.all_photos = []
    if 'photo_sources' not in st.session_state:
        st.session_state.photo_sources = []  # 'file' veya 'camera'
    
    # Kullanıcı adı (tüm bölümler için ortak)
    st.subheader("� Kullanıcı Bilgileri")
    username = st.text_input(
        "👤 Kullanıcı Adı",
        placeholder="Örn: ahmet_yilmaz",
        key="user_username",
        help="Benzersiz bir kullanıcı adı girin"
    )
    
    st.markdown("---")
    
    # Fotoğraf ekleme bölümü
    st.subheader("📷 Fotoğraf Ekleme")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📁 Dosyadan Yükle**")
        uploaded_files = st.file_uploader(
            "Fotoğraf seç",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            key="file_uploader",
            help="Birden fazla fotoğraf seçebilirsiniz"
        )
        
        if st.button("➕ Dosyaları Ekle", disabled=not uploaded_files):
            for uploaded_file in uploaded_files:
                uploaded_file.seek(0)
                photo_bytes = uploaded_file.getvalue()
                # Aynı fotoğrafı iki kez eklemeyi önle
                if photo_bytes not in st.session_state.all_photos:
                    st.session_state.all_photos.append(photo_bytes)
                    st.session_state.photo_sources.append('file')
            st.success(f"✅ {len(uploaded_files)} fotoğraf eklendi!")
            st.rerun()
    
    with col2:
        st.markdown("**📸 Kameradan Çek**")
        camera_photo = st.camera_input("Fotoğraf çek", key="camera_input")
        
        if st.button("➕ Fotoğrafı Ekle", disabled=(camera_photo is None)):
            if camera_photo:
                photo_bytes = camera_photo.getvalue()
                # Aynı fotoğrafı iki kez eklemeyi önle
                if photo_bytes not in st.session_state.all_photos:
                    st.session_state.all_photos.append(photo_bytes)
                    st.session_state.photo_sources.append('camera')
                    st.success("✅ Fotoğraf eklendi!")
                    st.rerun()
    
    st.markdown("---")
    
    # Tüm fotoğrafları göster
    show_all_photos_gallery(username)


def show_all_photos_gallery(username):
    """Tüm fotoğrafları galeri olarak göster ve kayıt işlemini yap"""
    st.subheader("🖼️ Toplanan Fotoğraflar")
    
    total_photos = len(st.session_state.all_photos)
    
    if total_photos == 0:
        st.info("ℹ️ Henüz fotoğraf eklenmedi. Yukarıdaki yöntemlerden birini kullanarak fotoğraf ekleyin.")
        return
    
    # İlerleme göster
    progress_color = "🟢" if total_photos >= 10 else "🟡" if total_photos >= 5 else "🔴"
    st.markdown(f"{progress_color} **{total_photos}/10 fotoğraf toplandi** (minimum 10 gerekli)")
    st.progress(min(total_photos / 10, 1.0))
    
    # Fotoğrafları göster
    cols_per_row = 5
    for i in range(0, total_photos, cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            photo_idx = i + j
            if photo_idx < total_photos:
                with col:
                    # Fotoğrafı göster
                    st.image(st.session_state.all_photos[photo_idx], width=100)
                    
                    # Kaynak göster
                    source = st.session_state.photo_sources[photo_idx]
                    source_emoji = "📁" if source == 'file' else "📸"
                    st.caption(f"{source_emoji} #{photo_idx + 1}")
                    
                    # Silme butonu
                    if st.button("🗑️", key=f"delete_{photo_idx}"):
                        st.session_state.all_photos.pop(photo_idx)
                        st.session_state.photo_sources.pop(photo_idx)
                        st.rerun()
    
    st.markdown("---")
    
    # Kaydetme bölümü
    if not username:
        st.warning("⚠️ Lütfen önce kullanıcı adı girin")
        return
    
    if total_photos < 10:
        st.warning(f"⚠️ Minimum 10 fotoğraf gerekli. Şu an {total_photos} fotoğraf var.")
        return
    
    # Kaydet butonu
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Kullanıcıyı Kaydet", type="primary", use_container_width=True):
            with st.spinner("Yüz tanıma modeli eğitiliyor..."):
                try:
                    # API'ye gönder
                    files = []
                    for idx, photo_bytes in enumerate(st.session_state.all_photos):
                        files.append(
                            ('images', (f'photo_{idx}.jpg', photo_bytes, 'image/jpeg'))
                        )
                    
                    response = requests.post(
                        f"{API_URL}/api/enroll",
                        data={'username': username},
                        files=files,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ Kullanıcı başarıyla kaydedildi!")
                        st.json(result)
                        
                        # Session state temizle
                        st.session_state.all_photos = []
                        st.session_state.photo_sources = []
                        st.balloons()
                        
                        time.sleep(2)
                        st.rerun()
                    else:
                        error_detail = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                        st.error(f"❌ Hata: {error_detail}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ API'ye bağlanılamadı! API'nin çalıştığından emin olun.")
                except Exception as e:
                    st.error(f"❌ Beklenmeyen hata: {str(e)}")

def show_add_user_file_upload():
    """Dosyadan kullanıcı ekleme"""
    with st.form("add_user_form"):
        st.subheader("📝 Kullanıcı Bilgileri")
        
        username = st.text_input(
            "👤 Kullanıcı Adı",
            placeholder="Örn: ahmet_yilmaz",
            help="Benzersiz bir kullanıcı adı girin"
        )
        
        st.subheader("📷 Fotoğraflar (En az 10 adet)")
        st.info("💡 **İpucu:** Farklı açılardan, farklı ışıklarda fotoğraflar çekin:\n"
                "- Yüzünüzü sola çevirin\n"
                "- Yüzünüzü sağa çevirin\n"
                "- Yukarı bakın\n"
                "- Aşağı bakın\n"
                "- Farklı ışık koşullarında\n"
                "- Gözlüklü/gözlüksüz (kullanıyorsanız)")
        
        uploaded_files = st.file_uploader(
            "Fotoğraf Yükle",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            help="En az 10 farklı fotoğraf yükleyin"
        )
        
        # Yüklenen fotoğrafları göster
        if uploaded_files:
            st.write(f"📸 **Yüklenen fotoğraf sayısı:** {len(uploaded_files)}")
            
            if len(uploaded_files) >= 3:
                cols = st.columns(min(len(uploaded_files), 5))
                for idx, uploaded_file in enumerate(uploaded_files[:5]):
                    with cols[idx % 5]:
                        st.image(uploaded_file, use_container_width=True, caption=f"#{idx+1}")
                
                if len(uploaded_files) > 5:
                    st.caption(f"... ve {len(uploaded_files) - 5} fotoğraf daha")
        
        submit = st.form_submit_button("💾 Kullanıcı Kaydet", type="primary", use_container_width=True)
        
        if submit:
            if not username:
                st.error("❌ Kullanıcı adı gerekli!")
            elif not uploaded_files:
                st.error("❌ En az 10 fotoğraf yüklemelisiniz!")
            elif len(uploaded_files) < 10:
                st.error(f"❌ En az 10 fotoğraf gerekli! (Şu an: {len(uploaded_files)})")
            else:
                # Enrollment API'ye gönder
                with st.spinner(f"👤 {username} kaydediliyor..."):
                    try:
                        files = []
                        for uploaded_file in uploaded_files:
                            uploaded_file.seek(0)  # Dosya pointerını başa al
                            files.append(('images', (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)))
                        
                        data = {'username': username}
                        
                        response = requests.post(
                            f"{API_URL}/api/enroll",
                            data=data,
                            files=files,
                            timeout=30
                        )
                        
                        if response.status_code == 201:
                            result = response.json()
                            st.success(f"✅ {username} başarıyla kaydedildi!")
                            st.json({
                                'User ID': result.get('user_id'),
                                'Embedding Sayısı': result.get('embeddings_count'),
                                'Mesaj': result.get('message')
                            })
                            st.balloons()
                            
                            # Veritabanını yenile
                            st.cache_resource.clear()
                            
                        elif response.status_code == 409:
                            st.error(f"❌ Kullanıcı '{username}' zaten kayıtlı!")
                        else:
                            error_msg = response.json().get('error', 'Bilinmeyen hata')
                            st.error(f"❌ Kayıt başarısız: {error_msg}")
                    
                    except Exception as e:
                        st.error(f"❌ Bağlantı hatası: {str(e)}")


def show_add_user_camera():
    """Kameradan kullanıcı ekleme"""
    st.subheader("📝 Kullanıcı Bilgileri")
    
    username = st.text_input(
        "👤 Kullanıcı Adı",
        placeholder="Örn: ahmet_yilmaz",
        key="camera_username",
        help="Benzersiz bir kullanıcı adı girin"
    )
    
    st.markdown("---")
    st.subheader("📸 Kamera ile Fotoğraf Çekimi")
    
    st.info("💡 **Adımlar:**\n"
            "1. Aşağıdaki kameradan fotoğraf çekin\n"
            "2. Her çekimde farklı bir açı/pozisyon kullanın\n"
            "3. En az 10 fotoğraf çekin\n"
            "4. 'Kullanıcı Kaydet' butonuna tıklayın")
    
    # Kamera
    camera_photo = st.camera_input("📷 Fotoğraf Çek")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Fotoğrafı Ekle", type="primary", disabled=(camera_photo is None)):
            if camera_photo:
                st.session_state.camera_photos.append(camera_photo.getvalue())
                st.success(f"✅ Fotoğraf eklendi! Toplam: {len(st.session_state.camera_photos)}")
                st.rerun()
    
    with col2:
        if st.button("🗑️ Son Fotoğrafı Sil", disabled=(len(st.session_state.camera_photos) == 0)):
            if st.session_state.camera_photos:
                st.session_state.camera_photos.pop()
                st.success("✅ Son fotoğraf silindi!")
                st.rerun()
    
    with col3:
        if st.button("🔄 Tümünü Temizle", disabled=(len(st.session_state.camera_photos) == 0)):
            st.session_state.camera_photos = []
            st.success("✅ Tüm fotoğraflar temizlendi!")
            st.rerun()
    
    # Çekilen fotoğrafları göster
    st.markdown("---")
    st.write(f"### 📸 Çekilen Fotoğraflar: {len(st.session_state.camera_photos)}/10")
    
    if st.session_state.camera_photos:
        # Progress bar
        progress = min(len(st.session_state.camera_photos) / 10, 1.0)
        st.progress(progress)
        
        # Fotoğraf galerisi
        cols = st.columns(5)
        for idx, photo_bytes in enumerate(st.session_state.camera_photos):
            with cols[idx % 5]:
                st.image(photo_bytes, caption=f"#{idx+1}", use_container_width=True)
        
        st.markdown("---")
        
        # Kaydet butonu
        if st.button("💾 Kullanıcı Kaydet", type="primary", use_container_width=True, 
                     disabled=(len(st.session_state.camera_photos) < 10 or not username)):
            
            if not username:
                st.error("❌ Kullanıcı adı gerekli!")
            elif len(st.session_state.camera_photos) < 10:
                st.error(f"❌ En az 10 fotoğraf gerekli! (Şu an: {len(st.session_state.camera_photos)})")
            else:
                # Enrollment API'ye gönder
                with st.spinner(f"👤 {username} kaydediliyor..."):
                    try:
                        files = []
                        for idx, photo_bytes in enumerate(st.session_state.camera_photos):
                            files.append(('images', (f'camera_{idx}.jpg', photo_bytes, 'image/jpeg')))
                        
                        data = {'username': username}
                        
                        response = requests.post(
                            f"{API_URL}/api/enroll",
                            data=data,
                            files=files,
                            timeout=30
                        )
                        
                        if response.status_code == 201:
                            result = response.json()
                            st.success(f"✅ {username} başarıyla kaydedildi!")
                            st.json({
                                'User ID': result.get('user_id'),
                                'Embedding Sayısı': result.get('embeddings_count'),
                                'Mesaj': result.get('message')
                            })
                            st.balloons()
                            
                            # Fotoğrafları temizle
                            st.session_state.camera_photos = []
                            
                            # Veritabanını yenile
                            st.cache_resource.clear()
                            
                        elif response.status_code == 409:
                            st.error(f"❌ Kullanıcı '{username}' zaten kayıtlı!")
                        else:
                            error_msg = response.json().get('error', 'Bilinmeyen hata')
                            st.error(f"❌ Kayıt başarısız: {error_msg}")
                    
                    except Exception as e:
                        st.error(f"❌ Bağlantı hatası: {str(e)}")
    else:
        st.info("Henüz fotoğraf çekmediniz. Yukarıdaki kameradan fotoğraf çekip '➕ Fotoğrafı Ekle' butonuna tıklayın.")


def show_settings():
    """Ayarlar sayfası"""
    st.header("🎚️ Sistem Ayarları")
    
    # Threshold ayarı
    st.subheader("🎯 Similarity Threshold")
    st.write("Yüz doğrulama için minimum benzerlik eşiği")
    
    # Mevcut threshold değerini al
    current_threshold = float(os.getenv('FS_THRESHOLD', '0.70'))
    
    threshold = st.slider(
        "Threshold Değeri",
        min_value=0.0,
        max_value=1.0,
        value=current_threshold,
        step=0.05,
        help="Düşük değer: Daha gevşek (daha fazla false positive)\nYüksek değer: Daha sıkı (daha fazla false negative)"
    )
    
    st.info(f"**Mevcut Değer:** {current_threshold}")
    st.info(f"**Yeni Değer:** {threshold}")
    
    if threshold != current_threshold:
        if st.button("💾 Threshold Kaydet", type="primary"):
            # .env dosyasını güncelle
            env_path = project_root / '.env'
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            with open(env_path, 'w') as f:
                for line in lines:
                    if line.startswith('FS_THRESHOLD='):
                        f.write(f'FS_THRESHOLD={threshold}\n')
                    else:
                        f.write(line)
            
            st.success(f"✅ Threshold {threshold} olarak kaydedildi!")
            st.info("⚠️ API'yi yeniden başlatın!")
    
    st.markdown("---")
    
    # Veritabanı bilgileri
    st.subheader("💾 Veritabanı")
    st.write(f"**Dosya:** {db.json_path}")
    st.write(f"**Boyut:** {os.path.getsize(db.json_path) / 1024:.2f} KB")
    
    if st.button("📥 Veritabanını İndir", type="secondary"):
        with open(db.json_path, 'r', encoding='utf-8') as f:
            data = f.read()
        st.download_button(
            label="💾 JSON Dosyasını İndir",
            data=data,
            file_name="facesecure_backup.json",
            mime="application/json"
        )


def show_logs():
    """Log görüntüleme sayfası"""
    st.header("📈 Başarısız Doğrulama Denemeleri")
    
    # Logları yükle
    data = json.load(open(db.json_path, 'r', encoding='utf-8'))
    failed_attempts = data.get('failed_attempts', [])
    
    if not failed_attempts:
        st.info("Henüz başarısız deneme yok")
        return
    
    # DataFrame oluştur
    log_data = []
    for attempt in failed_attempts:
        log_data.append({
            'Kullanıcı': attempt.get('username', 'N/A'),
            'IP Adresi': attempt.get('ip_address', 'N/A'),
            'Benzerlik': f"{attempt.get('similarity_score', 0):.3f}",
            'Neden': attempt.get('reason', 'N/A'),
            'Tarih': attempt.get('timestamp', 'N/A')[:19]
        })
    
    df = pd.DataFrame(log_data)
    
    # Filtreler
    col1, col2 = st.columns(2)
    
    with col1:
        username_filter = st.selectbox(
            "Kullanıcıya Göre Filtrele",
            ['Tümü'] + list(df['Kullanıcı'].unique())
        )
    
    with col2:
        reason_filter = st.selectbox(
            "Nedene Göre Filtrele",
            ['Tümü'] + list(df['Neden'].unique())
        )
    
    # Filtreleme uygula
    filtered_df = df.copy()
    if username_filter != 'Tümü':
        filtered_df = filtered_df[filtered_df['Kullanıcı'] == username_filter]
    if reason_filter != 'Tümü':
        filtered_df = filtered_df[filtered_df['Neden'] == reason_filter]
    
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    
    # İstatistikler
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Toplam Deneme", len(failed_attempts))
    with col2:
        st.metric("Filtrelenmiş", len(filtered_df))
    with col3:
        avg_similarity = filtered_df['Benzerlik'].astype(float).mean()
        st.metric("Ort. Benzerlik", f"{avg_similarity:.3f}")


def show_live_test():
    """Canlı test sayfası"""
    st.header("🧪 Canlı Yüz Doğrulama Testi")
    
    # API kontrolü
    if not check_api_health():
        st.error("❌ API çalışmıyor! Lütfen önce API'yi başlatın.")
        st.code("cd facesecure\n.\\start_api.bat", language="bash")
        return
    
    # Kullanıcı seçimi
    users = db.get_all_users()
    if not users:
        st.warning("⚠️ Henüz kayıtlı kullanıcı yok!")
        return
    
    usernames = [user['username'] for user in users]
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_username = st.selectbox("🎯 Test Edilecek Kullanıcı", usernames)
    
    with col2:
        test_mode = st.radio("Test Modu", ["Dosyadan Yükle", "Tüm Kullanıcılara Karşı"])
    
    st.markdown("---")
    
    # Fotoğraf kaynağı seçimi
    photo_source = st.radio(
        "📷 Fotoğraf Kaynağı",
        ["📁 Dosyadan Yükle", "📸 Kameradan Çek"],
        horizontal=True
    )
    
    uploaded_file = None
    camera_photo = None
    
    if photo_source == "📁 Dosyadan Yükle":
        # Dosya yükleme
        uploaded_file = st.file_uploader("📷 Fotoğraf Yükle", type=['jpg', 'jpeg', 'png'])
    else:
        # Kamera
        st.info("📸 Kameranızı kullanarak fotoğraf çekin")
        camera_photo = st.camera_input("Fotoğraf Çek")
    
    # Fotoğraf varsa işle
    test_photo = uploaded_file or camera_photo
    
    if test_photo is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(test_photo, caption="Test Fotoğrafı", use_container_width=True)
        
        with col2:
            if st.button("🔍 Doğrulama Yap", type="primary", use_container_width=True):
                with st.spinner("Doğrulama yapılıyor..."):
                    # API'ye istek gönder
                    files = {'image': test_photo.getvalue()}
                    
                    if test_mode == "Dosyadan Yükle":
                        data = {'username': target_username}
                    else:
                        data = {}  # Tüm kullanıcılara karşı test
                    
                    try:
                        response = requests.post(
                            f"{API_URL}/api/verify",
                            data=data,
                            files=files,
                            timeout=10
                        )
                        
                        result = response.json()
                        
                        # Sonuçları göster
                        if response.status_code == 200:
                            if result.get('verified'):
                                st.success("✅ DOĞRULAMA BAŞARILI!")
                                st.write(f"**Eşleşen Kullanıcı:** {result.get('username')}")
                                st.write(f"**Benzerlik:** {result.get('similarity'):.3f}")
                                st.write(f"**Threshold:** {result.get('threshold')}")
                                
                                # Progress bar
                                similarity = result.get('similarity', 0)
                                st.progress(similarity)
                            else:
                                st.error("❌ DOĞRULAMA BAŞARISIZ!")
                                st.write(f"**Neden:** {result.get('reason', 'Bilinmiyor')}")
                                if 'similarity' in result:
                                    st.write(f"**Benzerlik:** {result.get('similarity'):.3f}")
                                    st.write(f"**Threshold:** {result.get('threshold')}")
                                    st.progress(result.get('similarity', 0))
                        else:
                            st.error(f"❌ Hata: {result.get('error', 'Bilinmeyen hata')}")
                    
                    except Exception as e:
                        st.error(f"❌ Bağlantı hatası: {str(e)}")


def show_admin_management():
    """Admin kullanıcı yönetimi sayfası"""
    st.header("🔐 Admin Kullanıcı Yönetimi")
    
    tab1, tab2, tab3 = st.tabs(["👥 Admin Listesi", "➕ Yeni Admin Ekle", "🔑 Şifre Değiştir"])
    
    # Tab 1: Admin Listesi
    with tab1:
        st.subheader("📋 Kayıtlı Admin Kullanıcıları")
        
        admin_users = auth.get_all_users()
        
        if admin_users:
            for username, user_data in admin_users.items():
                with st.expander(f"👤 {username}", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Kullanıcı Adı:** {user_data['username']}")
                        st.write(f"**Rol:** {user_data['role']}")
                        st.write(f"**Oluşturulma:** {user_data.get('created_at', 'N/A')[:19]}")
                    
                    with col2:
                        if username != "admin":  # Default admin silinemez
                            if st.button(f"🗑️ Sil", key=f"delete_admin_{username}", type="primary"):
                                if st.session_state.get(f"confirm_delete_admin_{username}", False):
                                    success = auth.delete_admin_user(username)
                                    if success:
                                        st.success(f"✅ {username} silindi!")
                                        st.rerun()
                                    else:
                                        st.error("❌ Silme başarısız!")
                                else:
                                    st.session_state[f"confirm_delete_admin_{username}"] = True
                                    st.warning("⚠️ Tekrar tıklayarak onaylayın")
                        else:
                            st.caption("🔒 Default admin")
        else:
            st.info("Henüz admin kullanıcı yok")
    
    # Tab 2: Yeni Admin Ekle
    with tab2:
        st.subheader("➕ Yeni Admin Kullanıcısı Ekle")
        
        with st.form("add_admin_form"):
            new_username = st.text_input(
                "👤 Kullanıcı Adı",
                placeholder="Örn: admin2",
                help="Benzersiz bir admin kullanıcı adı"
            )
            
            new_password = st.text_input(
                "🔒 Şifre",
                type="password",
                placeholder="Güçlü bir şifre girin",
                help="En az 8 karakter önerilir"
            )
            
            confirm_password = st.text_input(
                "🔒 Şifre Tekrar",
                type="password",
                placeholder="Şifreyi tekrar girin"
            )
            
            role = st.selectbox(
                "🎭 Rol",
                ["admin", "viewer"],
                help="admin: Tam yetki, viewer: Sadece görüntüleme"
            )
            
            submit_add = st.form_submit_button("💾 Admin Ekle", type="primary", use_container_width=True)
            
            if submit_add:
                if not new_username or not new_password:
                    st.error("❌ Tüm alanları doldurun!")
                elif new_password != confirm_password:
                    st.error("❌ Şifreler eşleşmiyor!")
                elif len(new_password) < 6:
                    st.error("❌ Şifre en az 6 karakter olmalı!")
                else:
                    success = auth.create_admin_user(new_username, new_password, role)
                    if success:
                        st.success(f"✅ Admin kullanıcısı '{new_username}' oluşturuldu!")
                        st.balloons()
                    else:
                        st.error(f"❌ Kullanıcı '{new_username}' zaten mevcut!")
    
    # Tab 3: Şifre Değiştir
    with tab3:
        st.subheader("🔑 Şifre Değiştir")
        
        with st.form("change_password_form"):
            st.write(f"**Kullanıcı:** {st.session_state.username}")
            
            old_password = st.text_input(
                "🔒 Mevcut Şifre",
                type="password",
                placeholder="Mevcut şifrenizi girin"
            )
            
            new_password = st.text_input(
                "🔐 Yeni Şifre",
                type="password",
                placeholder="Yeni şifrenizi girin"
            )
            
            confirm_new_password = st.text_input(
                "🔐 Yeni Şifre Tekrar",
                type="password",
                placeholder="Yeni şifrenizi tekrar girin"
            )
            
            submit_change = st.form_submit_button("💾 Şifre Değiştir", type="primary", use_container_width=True)
            
            if submit_change:
                if not old_password or not new_password:
                    st.error("❌ Tüm alanları doldurun!")
                elif new_password != confirm_new_password:
                    st.error("❌ Yeni şifreler eşleşmiyor!")
                elif len(new_password) < 6:
                    st.error("❌ Yeni şifre en az 6 karakter olmalı!")
                else:
                    success = auth.change_password(st.session_state.username, old_password, new_password)
                    if success:
                        st.success("✅ Şifre başarıyla değiştirildi!")
                        st.balloons()
                    else:
                        st.error("❌ Mevcut şifre hatalı!")


if __name__ == "__main__":
    main()
