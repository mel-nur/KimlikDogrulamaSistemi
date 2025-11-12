"""
Yüz tespit modülü - Basit ve güvenilir yüz tespiti
"""
import cv2
import numpy as np
from typing import List, Optional
import os


class FaceDetector:
    """Basit yüz tespit sınıfı (Stub implementation)"""
    
    def __init__(self, scale_factor: float = 1.1, min_neighbors: int = 5):
        """
        Args:
            scale_factor: Görüntü piramidi ölçekleme faktörü  
            min_neighbors: Minimum komşu sayısı
            
        Not: Bu stub implementation, gerçek model Sprint 2'de entegre edilecek
        """
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.face_cascade = self._load_cascade()
    
    def _load_cascade(self):
        """Haar Cascade yüklemeyi dene, başarısız olursa None döndür"""
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            if os.path.exists(cascade_path):
                cascade = cv2.CascadeClassifier(cascade_path)
                if not cascade.empty():
                    return cascade
        except:
            pass
        return None
        
    def detect_faces(self, image: np.ndarray) -> List[np.ndarray]:
        """
        Görüntüden yüzleri tespit eder ve aligned crop'ları döndürür
        
        Args:
            image: BGR formatında numpy array (OpenCV image)
            
        Returns:
            Tespit edilen yüzlerin aligned crop'ları (list of numpy arrays)
            
        Raises:
            ValueError: Eğer birden fazla yüz tespit edilirse
        """
        if self.face_cascade is None:
            # Stub: Basit merkez crop döndür (gerçek model için placeholder)
            h, w = image.shape[:2]
            # Merkezi %60'lık alanı yüz olarak kabul et
            crop_size = min(h, w) * 0.6
            x1 = int((w - crop_size) / 2)
            y1 = int((h - crop_size) / 2)
            x2 = int(x1 + crop_size)
            y2 = int(y1 + crop_size)
            
            face_crop = image[y1:y2, x1:x2]
            if face_crop.size > 0:
                face_resized = cv2.resize(face_crop, (160, 160))
                return [face_resized]
            return []
        
        # Haar Cascade ile gerçek tespit
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        faces_rect = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=(30, 30)
        )
        
        if len(faces_rect) == 0:
            return []
        
        # Çoklu yüz kontrolü
        if len(faces_rect) > 1:
            raise ValueError(
                f"Birden fazla yüz tespit edildi ({len(faces_rect)}). "
                "Lütfen tek bir yüz içeren görüntü kullanın."
            )
        
        faces = []
        for (x, y, w, h) in faces_rect:
            face_crop = image[y:y+h, x:x+w]
            if face_crop.shape[0] > 20 and face_crop.shape[1] > 20:
                face_resized = cv2.resize(face_crop, (160, 160))
                faces.append(face_resized)
        
        return faces
    
    def detect_single_face(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Tek bir yüz tespit eder
        
        Args:
            image: BGR formatında numpy array
            
        Returns:
            Aligned yüz crop'u veya None (yüz bulunamazsa)
            
        Raises:
            ValueError: Eğer birden fazla yüz tespit edilirse
        """
        faces = self.detect_faces(image)
        return faces[0] if faces else None
