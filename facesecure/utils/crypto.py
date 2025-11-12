"""
Şifreleme ve güvenlik yardımcı fonksiyonları
"""
import os
import base64
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from typing import Tuple
import numpy as np


class CryptoManager:
    """AES-GCM şifreleme ve HMAC doğrulama yöneticisi"""
    
    def __init__(self, aes_key_b64: str, hmac_key_b64: str):
        """
        Args:
            aes_key_b64: Base64 encoded AES-256 key (32 bytes)
            hmac_key_b64: Base64 encoded HMAC key (32 bytes)
        """
        self.aes_key = base64.b64decode(aes_key_b64)
        self.hmac_key = base64.b64decode(hmac_key_b64)
        
        if len(self.aes_key) != 32:
            raise ValueError("AES key 32 byte olmalı")
        if len(self.hmac_key) != 32:
            raise ValueError("HMAC key 32 byte olmalı")
        
        self.aesgcm = AESGCM(self.aes_key)
    
    def encrypt_embedding(self, embedding: np.ndarray) -> Tuple[str, str]:
        """
        Embedding'i AES-GCM ile şifreler
        
        Args:
            embedding: 512-boyutlu numpy array (FaceNet)
            
        Returns:
            (encrypted_b64, hmac_b64) tuple
        """
        # Numpy array'i bytes'a çevir
        embedding_bytes = embedding.tobytes()
        
        # 96-bit nonce (GCM standardı)
        nonce = os.urandom(12)
        
        # AES-GCM şifreleme (authenticated encryption)
        ciphertext = self.aesgcm.encrypt(nonce, embedding_bytes, None)
        
        # Nonce + ciphertext birleştir
        encrypted = nonce + ciphertext
        encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
        
        # HMAC hesapla (additional integrity check)
        hmac_digest = hmac.new(
            self.hmac_key,
            encrypted,
            hashlib.sha256
        ).digest()
        hmac_b64 = base64.b64encode(hmac_digest).decode('utf-8')
        
        return encrypted_b64, hmac_b64
    
    def decrypt_embedding(self, encrypted_b64: str, hmac_b64: str, 
                         embedding_dim: int = 512) -> np.ndarray:
        """
        Şifrelenmiş embedding'i çözer
        
        Args:
            encrypted_b64: Base64 encoded encrypted data
            hmac_b64: Base64 encoded HMAC
            embedding_dim: Embedding boyutu (FaceNet: 512)
            
        Returns:
            Decrypted embedding (numpy array)
            
        Raises:
            ValueError: HMAC doğrulama başarısız
        """
        encrypted = base64.b64decode(encrypted_b64)
        stored_hmac = base64.b64decode(hmac_b64)
        
        # HMAC doğrulama
        computed_hmac = hmac.new(
            self.hmac_key,
            encrypted,
            hashlib.sha256
        ).digest()
        
        if not hmac.compare_digest(stored_hmac, computed_hmac):
            raise ValueError("HMAC doğrulama başarısız - veri bütünlüğü ihlali!")
        
        # Nonce ve ciphertext ayır
        nonce = encrypted[:12]
        ciphertext = encrypted[12:]
        
        # Deşifreleme
        plaintext = self.aesgcm.decrypt(nonce, ciphertext, None)
        
        # Bytes'ı numpy array'e çevir
        embedding = np.frombuffer(plaintext, dtype=np.float32)
        
        if len(embedding) != embedding_dim:
            raise ValueError(f"Embedding boyutu uyuşmuyor: {len(embedding)} != {embedding_dim}")
        
        return embedding


def generate_keys() -> Tuple[str, str]:
    """
    Yeni AES ve HMAC anahtarları üretir
    
    Returns:
        (aes_key_b64, hmac_key_b64) tuple
    """
    aes_key = os.urandom(32)
    hmac_key = os.urandom(32)
    
    return (
        base64.b64encode(aes_key).decode('utf-8'),
        base64.b64encode(hmac_key).decode('utf-8')
    )
