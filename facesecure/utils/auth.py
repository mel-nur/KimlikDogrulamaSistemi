"""
Admin kullanıcı yönetimi ve authentication
"""
import hashlib
import json
import os
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime


class AdminAuthManager:
    """Admin kullanıcıları için authentication yöneticisi"""
    
    def __init__(self, auth_file: str = "admin_users.json"):
        """
        Args:
            auth_file: Admin kullanıcılarının saklandığı JSON dosyası
        """
        self.auth_file = Path(auth_file)
        self._init_file()
    
    def _init_file(self):
        """Dosya yoksa oluştur ve default admin ekle"""
        if not self.auth_file.exists():
            default_admin = {
                "admin": {
                    "username": "admin",
                    "password_hash": self._hash_password("admin123"),
                    "role": "admin",
                    "created_at": datetime.utcnow().isoformat()
                }
            }
            self._save_data(default_admin)
    
    def _load_data(self) -> Dict:
        """JSON dosyasından veriyi yükle"""
        with open(self.auth_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data: Dict):
        """Veriyi JSON dosyasına kaydet"""
        with open(self.auth_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _hash_password(self, password: str) -> str:
        """Şifreyi SHA256 ile hashle"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Kullanıcı doğrulama
        
        Args:
            username: Kullanıcı adı
            password: Şifre (düz metin)
        
        Returns:
            True if authenticated, False otherwise
        """
        data = self._load_data()
        
        if username not in data:
            return False
        
        user = data[username]
        password_hash = self._hash_password(password)
        
        return user['password_hash'] == password_hash
    
    def create_admin_user(self, username: str, password: str, role: str = "admin") -> bool:
        """
        Yeni admin kullanıcısı oluştur
        
        Args:
            username: Kullanıcı adı
            password: Şifre (düz metin - hashlenecek)
            role: Kullanıcı rolü (admin, viewer)
        
        Returns:
            True if successful, False if user exists
        """
        data = self._load_data()
        
        if username in data:
            return False
        
        data[username] = {
            "username": username,
            "password_hash": self._hash_password(password),
            "role": role,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self._save_data(data)
        return True
    
    def delete_admin_user(self, username: str) -> bool:
        """
        Admin kullanıcısını sil
        
        Args:
            username: Silinecek kullanıcı adı
        
        Returns:
            True if deleted, False if not found
        """
        data = self._load_data()
        
        if username not in data:
            return False
        
        # Default admin silinemez
        if username == "admin":
            return False
        
        del data[username]
        self._save_data(data)
        return True
    
    def get_all_users(self) -> Dict:
        """Tüm admin kullanıcılarını getir (şifreler hariç)"""
        data = self._load_data()
        
        users = {}
        for username, user_data in data.items():
            users[username] = {
                "username": user_data["username"],
                "role": user_data["role"],
                "created_at": user_data["created_at"]
            }
        
        return users
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """
        Şifre değiştir
        
        Args:
            username: Kullanıcı adı
            old_password: Eski şifre
            new_password: Yeni şifre
        
        Returns:
            True if successful, False otherwise
        """
        # Önce mevcut şifreyi doğrula
        if not self.authenticate(username, old_password):
            return False
        
        data = self._load_data()
        data[username]['password_hash'] = self._hash_password(new_password)
        self._save_data(data)
        
        return True
