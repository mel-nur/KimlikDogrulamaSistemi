"""
Yüz doğrulama (verification) endpoint'i
"""
from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from face.detector import FaceDetector
from face.processor import FaceEmbeddingProcessor
from utils.crypto import CryptoManager
from utils.db import DBManager
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('verify', __name__, url_prefix='/api')

# Global instances
detector = FaceDetector()
processor = FaceEmbeddingProcessor()
crypto_manager = CryptoManager(
    os.getenv('FS_AES_KEY_B64'),
    os.getenv('FS_HMAC_KEY_B64')
)
db_manager = DBManager(os.getenv('MONGO_URI'))

# Threshold
SIMILARITY_THRESHOLD = float(os.getenv('FS_THRESHOLD', '0.70'))


@bp.route('/verify', methods=['POST'])
def verify_face():
    """
    Yüz doğrulama
    
    Request:
        - username: str (opsiyonel, belirtilmezse tüm kullanıcılara karşı)
        - image: file (tek bir yüz görüntüsü)
    
    Response:
        - verified: bool
        - username: str (eşleşme varsa)
        - similarity: float
        - threshold: float
    """
    # Her request'te DBManager'ı yeniden yükle (fresh data)
    db = DBManager(os.getenv('MONGO_URI'))
    
    # İstemci IP'sini al
    client_ip = request.remote_addr
    
    # Görüntüyü al
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({'error': 'image gerekli'}), 400
    
    # Username (opsiyonel)
    target_username = request.form.get('username')
    
    try:
        # Görüntüyü oku
        file_bytes = np.frombuffer(image_file.read(), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Geçersiz görüntü'}), 400
        
        # Yüz tespit et
        faces = detector.detect_faces(image)
        
        if not faces:
            db.log_failed_attempt(
                target_username,
                client_ip,
                0.0,
                'Yüz tespit edilemedi'
            )
            return jsonify({
                'verified': False,
                'reason': 'Yüz tespit edilemedi'
            }), 200
        
        # Embedding üret
        query_embedding = processor.get_embedding(faces[0], normalize=True)
        
        # Kullanıcıları al
        if target_username:
            users = [db.get_user_by_username(target_username)]
            if users[0] is None:
                return jsonify({'error': 'Kullanıcı bulunamadı'}), 404
        else:
            users = db.get_all_users()
        
        if not users:
            return jsonify({'error': 'Kayıtlı kullanıcı yok'}), 404
        
        # En yüksek benzerliği bul
        best_match = None
        best_similarity = 0.0
        
        for user in users:
            for emb_doc in user['embeddings']:
                # Embedding'i deşifre et
                stored_embedding = crypto_manager.decrypt_embedding(
                    emb_doc['encrypted'],
                    emb_doc['hmac']
                )
                
                # Benzerlik hesapla
                similarity = processor.compute_similarity(
                    query_embedding,
                    stored_embedding
                )
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = user['username']
        
        # Threshold kontrolü
        if best_similarity >= SIMILARITY_THRESHOLD:
            return jsonify({
                'verified': True,
                'username': best_match,
                'similarity': float(best_similarity),
                'threshold': SIMILARITY_THRESHOLD
            }), 200
        else:
            # Başarısız denemeyi logla
            db.log_failed_attempt(
                best_match,
                client_ip,
                best_similarity,
                f'Benzerlik threshold\'un altında ({best_similarity:.3f} < {SIMILARITY_THRESHOLD})'
            )
            
            return jsonify({
                'verified': False,
                'similarity': float(best_similarity),
                'threshold': SIMILARITY_THRESHOLD,
                'reason': 'Benzerlik threshold\'un altında'
            }), 200
        
    except ValueError as e:
        # Çoklu yüz hatası
        db.log_failed_attempt(
            target_username,
            client_ip,
            0.0,
            str(e)
        )
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        return jsonify({'error': f'İşlem hatası: {str(e)}'}), 500
