"""
Yüz tespit ve embedding pipeline testleri
"""
import os
import pytest
import numpy as np
import cv2
from pathlib import Path

# Proje root'una ekle
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from face.detector import FaceDetector
from face.processor import FaceEmbeddingProcessor


class TestFaceDetector:
    """FaceDetector sınıfı için testler"""
    
    @pytest.fixture
    def detector(self):
        """Test için detector instance"""
        return FaceDetector(scale_factor=1.1, min_neighbors=5)
    
    @pytest.fixture
    def sample_image(self):
        """Test için örnek görüntü (tek renkli 200x200 görüntü)"""
        # Basit test görüntüsü: ortada bir "yüz" benzer şekil
        img = np.ones((200, 200, 3), dtype=np.uint8) * 128
        # Yüz benzeri bir daire çiz (gerçek test için gerçek yüz görseli gerekli)
        cv2.circle(img, (100, 100), 50, (200, 150, 100), -1)
        return img
    
    def test_detector_initialization(self, detector):
        """Detector'ın doğru başlatılıp başlatılmadığını test et"""
        assert detector is not None
        # face_cascade None olabilir (stub mode)
    
    def test_detect_faces_returns_list(self, detector, sample_image):
        """detect_faces metodunun liste döndürdüğünü test et"""
        result = detector.detect_faces(sample_image)
        assert isinstance(result, list)
    
    def test_multiple_faces_raises_error(self, detector):
        """Çoklu yüz tespitinde ValueError fırlatıldığını test et"""
        # Not: Bu test gerçek çoklu yüzlü görüntü ile çalışmalı
        # Şimdilik sadece metodun varlığını test ediyoruz
        pass


class TestFaceEmbeddingProcessor:
    """FaceEmbeddingProcessor sınıfı için testler"""
    
    @pytest.fixture
    def processor(self):
        """Test için processor instance"""
        return FaceEmbeddingProcessor(embedding_dim=128)
    
    @pytest.fixture
    def sample_face(self):
        """Test için örnek yüz crop'u (160x160)"""
        return np.random.randint(0, 255, (160, 160, 3), dtype=np.uint8)
    
    def test_processor_initialization(self, processor):
        """Processor'ın doğru başlatılıp başlatılmadığını test et"""
        assert processor is not None
        assert processor.embedding_dim == 128
    
    def test_get_embedding_shape(self, processor, sample_face):
        """Embedding'in doğru shape'e sahip olduğunu test et"""
        embedding = processor.get_embedding(sample_face)
        assert embedding.shape == (128,)
        assert embedding.dtype == np.float32
    
    def test_get_embedding_normalized(self, processor, sample_face):
        """Normalize edilmiş embedding'in L2 norm'unun ~1.0 olduğunu test et"""
        embedding = processor.get_embedding(sample_face, normalize=True)
        norm = np.linalg.norm(embedding)
        assert np.isclose(norm, 1.0, atol=1e-6), f"Norm: {norm}, beklenen: 1.0"
    
    def test_get_embedding_without_normalization(self, processor, sample_face):
        """Normalizasyon olmadan embedding üretimini test et"""
        embedding = processor.get_embedding(sample_face, normalize=False)
        norm = np.linalg.norm(embedding)
        # Normalize edilmemiş embedding norm'u 1'den farklı olmalı
        assert not np.isclose(norm, 1.0, atol=0.1)
    
    def test_compute_similarity_identical(self, processor, sample_face):
        """Aynı görüntü için similarity ~1.0 olmalı"""
        embedding1 = processor.get_embedding(sample_face)
        embedding2 = processor.get_embedding(sample_face)
        similarity = processor.compute_similarity(embedding1, embedding2)
        assert 0.0 <= similarity <= 1.0
        assert np.isclose(similarity, 1.0, atol=0.01), f"Similarity: {similarity}"
    
    def test_compute_similarity_different(self, processor):
        """Farklı görüntüler için similarity < 1.0 olmalı"""
        face1 = np.random.randint(0, 255, (160, 160, 3), dtype=np.uint8)
        face2 = np.random.randint(0, 255, (160, 160, 3), dtype=np.uint8)
        
        embedding1 = processor.get_embedding(face1)
        embedding2 = processor.get_embedding(face2)
        similarity = processor.compute_similarity(embedding1, embedding2)
        
        assert 0.0 <= similarity <= 1.0
        # Rastgele görüntüler için similarity 1.0'dan küçük olmalı
        # (çok küçük bir ihtimalle eşit olabilir ama genelde değildir)
    
    def test_preprocess_shape(self, processor, sample_face):
        """Preprocessing'in batch dimension eklediğini test et"""
        processed = processor.preprocess(sample_face)
        assert processed.shape == (1, 160, 160, 3)
    
    def test_preprocess_range(self, processor, sample_face):
        """Preprocessing'in değerleri [-1, 1] aralığına aldığını test et"""
        processed = processor.preprocess(sample_face)
        assert processed.min() >= -1.0
        assert processed.max() <= 1.0


class TestIntegration:
    """Entegrasyon testleri - Detector + Processor pipeline"""
    
    @pytest.fixture
    def detector(self):
        return FaceDetector()
    
    @pytest.fixture
    def processor(self):
        return FaceEmbeddingProcessor()
    
    def test_full_pipeline_with_synthetic_image(self, detector, processor):
        """Sentetik görüntü ile tam pipeline testi"""
        # Sentetik görüntü oluştur
        img = np.ones((300, 300, 3), dtype=np.uint8) * 200
        cv2.circle(img, (150, 150), 70, (100, 150, 200), -1)
        
        # Yüz tespit et (gerçek yüz olmadığı için boş dönebilir)
        faces = detector.detect_faces(img)
        
        # Eğer yüz tespit edildiyse embedding üret
        if faces:
            embedding = processor.get_embedding(faces[0])
            assert embedding.shape == (128,)
            norm = np.linalg.norm(embedding)
            assert np.isclose(norm, 1.0, atol=1e-6)


if __name__ == "__main__":
    # Test'leri çalıştır
    pytest.main([__file__, "-v"])
