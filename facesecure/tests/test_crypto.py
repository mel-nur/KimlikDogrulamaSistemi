"""
Sprint 2 unit testleri - Crypto ve DB testleri
"""
import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crypto import CryptoManager, generate_keys


class TestCryptoManager:
    """Şifreleme testleri"""
    
    @pytest.fixture
    def crypto_manager(self):
        """Test için CryptoManager instance"""
        aes_key_b64, hmac_key_b64 = generate_keys()
        return CryptoManager(aes_key_b64, hmac_key_b64)
    
    @pytest.fixture
    def sample_embedding(self):
        """Test için örnek embedding"""
        embedding = np.random.randn(128).astype(np.float32)
        embedding = embedding / np.linalg.norm(embedding)  # Normalize
        return embedding
    
    def test_crypto_manager_initialization(self, crypto_manager):
        """CryptoManager başlatma testi"""
        assert crypto_manager is not None
        assert crypto_manager.aes_key is not None
        assert crypto_manager.hmac_key is not None
        assert len(crypto_manager.aes_key) == 32
        assert len(crypto_manager.hmac_key) == 32
    
    def test_encrypt_embedding(self, crypto_manager, sample_embedding):
        """Embedding şifreleme testi"""
        encrypted_b64, hmac_b64 = crypto_manager.encrypt_embedding(sample_embedding)
        
        assert isinstance(encrypted_b64, str)
        assert isinstance(hmac_b64, str)
        assert len(encrypted_b64) > 0
        assert len(hmac_b64) > 0
    
    def test_decrypt_embedding(self, crypto_manager, sample_embedding):
        """Embedding deşifreleme testi"""
        # Şifrele
        encrypted_b64, hmac_b64 = crypto_manager.encrypt_embedding(sample_embedding)
        
        # Deşifre et
        decrypted = crypto_manager.decrypt_embedding(encrypted_b64, hmac_b64)
        
        assert decrypted.shape == sample_embedding.shape
        assert np.allclose(decrypted, sample_embedding, atol=1e-6)
    
    def test_hmac_integrity_check(self, crypto_manager, sample_embedding):
        """HMAC bütünlük kontrolü testi"""
        encrypted_b64, hmac_b64 = crypto_manager.encrypt_embedding(sample_embedding)
        
        # HMAC'i değiştir (tampering simulation)
        fake_hmac = hmac_b64[:-4] + "FAKE"
        
        # Deşifreleme başarısız olmalı
        with pytest.raises(ValueError, match="HMAC doğrulama başarısız"):
            crypto_manager.decrypt_embedding(encrypted_b64, fake_hmac)
    
    def test_generate_keys(self):
        """Anahtar üretme testi"""
        aes_key_b64, hmac_key_b64 = generate_keys()
        
        assert isinstance(aes_key_b64, str)
        assert isinstance(hmac_key_b64, str)
        assert len(aes_key_b64) > 0
        assert len(hmac_key_b64) > 0
        
        # İki üretim farklı anahtarlar vermeli
        aes_key_b64_2, hmac_key_b64_2 = generate_keys()
        assert aes_key_b64 != aes_key_b64_2
        assert hmac_key_b64 != hmac_key_b64_2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
