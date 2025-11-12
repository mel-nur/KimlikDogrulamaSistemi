"""
Veritabanı bağlantı ve yardımcı fonksiyonları (JSON dosya tabanlı)
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import os


class DBManager:
    """JSON dosya tabanlı veritabanı yöneticisi"""
    
    def __init__(self, mongo_uri: str = None):
        """
        Args:
            mongo_uri: Kullanılmıyor (uyumluluk için)
        """
        self.json_path = "facesecure_data.json"
        self._load_data()
        print(f"✅ JSON veritabanı: {self.json_path}")
    
    def _load_data(self):
        """JSON dosyasından veri yükle"""
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.users_storage = data.get('users', {})
                    self.failed_attempts_storage = data.get('failed_attempts', [])
                    self.user_id_counter = data.get('user_id_counter', 0)
            except (json.JSONDecodeError, IOError):
                # Dosya bozuksa yeni başlat
                self.users_storage = {}
                self.failed_attempts_storage = []
                self.user_id_counter = 0
                self._save_data()
        else:
            self.users_storage = {}
            self.failed_attempts_storage = []
            self.user_id_counter = 0
            self._save_data()
    
    def _save_data(self):
        """Veriyi JSON dosyasına kaydet"""
        data = {
            'users': self.users_storage,
            'failed_attempts': self.failed_attempts_storage,
            'user_id_counter': self.user_id_counter
        }
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    def create_user(self, username: str, embeddings: List[Dict[str, str]]) -> str:
        """
        Yeni kullanıcı oluştur
        
        Args:
            username: Kullanıcı adı
            embeddings: Şifrelenmiş embedding listesi 
                        [{'encrypted': str, 'hmac': str}, ...]
        
        Returns:
            User ID
        """
        if username in self.users_storage:
            raise ValueError(f"Kullanıcı '{username}' zaten mevcut")
        
        self.user_id_counter += 1
        user_id = str(self.user_id_counter)
        
        user_doc = {
            '_id': user_id,
            'username': username,
            'embeddings': embeddings,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        self.users_storage[username] = user_doc
        self._save_data()
        return user_id
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Kullanıcıyı username ile bul"""
        return self.users_storage.get(username)
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Tüm kullanıcıları getir"""
        return list(self.users_storage.values())
    
    def delete_user(self, username: str) -> bool:
        """Kullanıcıyı sil"""
        if username in self.users_storage:
            del self.users_storage[username]
            self._save_data()
            return True
        return False
    
    def log_failed_attempt(self, username: Optional[str], ip_address: str, 
                          similarity_score: float, reason: str):
        """
        Başarısız doğrulama denemesini logla
        
        Args:
            username: Denenen kullanıcı adı (varsa)
            ip_address: İstemci IP adresi
            similarity_score: Benzerlik skoru
            reason: Başarısızlık nedeni
        """
        log_doc = {
            'username': username,
            'ip_address': ip_address,
            'similarity_score': similarity_score,
            'reason': reason,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.failed_attempts_storage.append(log_doc)
        self._save_data()
    
    def get_failed_attempts(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Son başarısız denemeleri getir"""
        # Son N kaydı getir (reversed)
        return list(reversed(self.failed_attempts_storage[-limit:]))
    
    def close(self):
        """JSON - kapatma gerekmez"""
        pass
