"""
Embedding işleme modülü - Yüz embedding'lerini üretir ve normalize eder
"""
import numpy as np
import cv2
from typing import Optional
from keras_facenet import FaceNet


class FaceEmbeddingProcessor:
    """
    Yüz embedding üretimi için işlemci sınıfı
    
    FaceNet modelini kullanarak 512 boyutlu embedding vektörleri üretir.
    """
    
    def __init__(self, model_path: Optional[str] = None, embedding_dim: int = 512):
        """
        Args:
            model_path: Model dosyasının yolu (kullanılmıyor, keras-facenet otomatik indirir)
            embedding_dim: Embedding vektör boyutu (FaceNet için 512)
        """
        self.model_path = model_path
        self.embedding_dim = embedding_dim
        
        # Gerçek FaceNet modelini yükle
        print("🔄 FaceNet modeli yükleniyor...")
        try:
            self.model = FaceNet()
            print("✅ FaceNet modeli başarıyla yüklendi!")
        except Exception as e:
            print(f"❌ FaceNet modeli yüklenemedi: {e}")
            print("⚠️  Stub embedding'e geri dönülüyor...")
            self.model = None
            self.embedding_dim = 128
    
    def get_embedding(self, face_image: np.ndarray, normalize: bool = True) -> np.ndarray:
        """
        Yüz görüntüsünden embedding üretir
        
        Args:
            face_image: Aligned yüz crop'u (BGR formatında)
            normalize: L2 normalizasyonu uygulansın mı?
            
        Returns:
            Embedding vektörü (512,) shape'inde numpy array (FaceNet)
            veya (128,) shape (stub mode)
        """
        if self.model is not None:
            # Gerçek FaceNet inference
            try:
                # FaceNet için preprocessing
                # 1. BGR -> RGB dönüşümü
                face_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
                
                # 2. 160x160 resize (FaceNet input size)
                face_resized = cv2.resize(face_rgb, (160, 160))
                
                # 3. Expand dimensions (batch dimension)
                face_batch = np.expand_dims(face_resized, axis=0)
                
                # 4. Embedding üret
                embedding = self.model.embeddings(face_batch)[0]
                
                # 5. Normalize
                if normalize:
                    embedding = self._normalize(embedding)
                
                return embedding
            except Exception as e:
                print(f"❌ FaceNet inference hatası: {e}")
                print("⚠️  Stub embedding'e geri dönülüyor...")
                # Hata durumunda stub'a düş
                pass
        
        # Stub implementation: Deterministik rastgele embedding
        seed = int(np.mean(face_image) * 1000) % 10000
        np.random.seed(seed)
        embedding = np.random.randn(self.embedding_dim).astype(np.float32)
        
        if normalize:
            embedding = self._normalize(embedding)
        
        return embedding
    
    def _normalize(self, embedding: np.ndarray) -> np.ndarray:
        """
        L2 normalizasyonu uygular
        
        Args:
            embedding: Ham embedding vektörü
            
        Returns:
            Normalize edilmiş embedding (norm ≈ 1.0)
        """
        norm = np.linalg.norm(embedding)
        if norm > 0:
            return embedding / norm
        return embedding
    
    def preprocess(self, face_image: np.ndarray) -> np.ndarray:
        """
        Model için görüntü ön işleme
        
        Args:
            face_image: Ham yüz görüntüsü
            
        Returns:
            Ön işlenmiş görüntü
        """
        # FaceNet preprocessing
        # 1. [0, 255] -> [-1, 1] normalize
        processed = (face_image.astype(np.float32) - 127.5) / 127.5
        
        # 2. Batch dimension ekle
        processed = np.expand_dims(processed, axis=0)
        
        return processed
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        İki embedding arasında cosine similarity hesaplar
        
        Args:
            embedding1: İlk embedding vektörü
            embedding2: İkinci embedding vektörü
            
        Returns:
            Cosine similarity skoru (0-1 arası, 1 = tamamen aynı)
        """
        # Cosine similarity = dot product (normalize edilmişse)
        similarity = np.dot(embedding1, embedding2)
        
        # [-1, 1] -> [0, 1] skalaya dönüştür
        similarity = (similarity + 1) / 2
        
        return float(similarity)
