"""
Kullanıcı kayıt (enrollment) endpoint'i
"""
from flask import Blueprint, request, jsonify
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import os
import sys
from pathlib import Path

# Proje root'u path'e ekle
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from face.detector import FaceDetector
from face.processor import FaceEmbeddingProcessor
from utils.crypto import CryptoManager
from utils.db import DBManager
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('enroll', __name__, url_prefix='/api')

# Global instances (production'da singleton pattern kullan)
detector = FaceDetector()
processor = FaceEmbeddingProcessor()
crypto_manager = CryptoManager(
    os.getenv('FS_AES_KEY_B64'),
    os.getenv('FS_HMAC_KEY_B64')
)
db_manager = DBManager(os.getenv('MONGO_URI'))


@bp.route('/enroll', methods=['POST'])
def enroll_user():
    """
    Yeni kullanıcı kaydı (enrollment)
    
    Request:
        - username: str
        - images: List[file] (en az 10 görüntü)
    
    Response:
        - user_id: str
        - embeddings_count: int
        - message: str
    """
    # Form verilerini al
    username = request.form.get('username')
    
    if not username:
        return jsonify({'error': 'username gerekli'}), 400
    
    # Kullanıcı zaten var mı kontrol et
    existing_user = db_manager.get_user_by_username(username)
    if existing_user:
        return jsonify({'error': f'Kullanıcı "{username}" zaten mevcut'}), 409
    
    # Görüntüleri al
    images = request.files.getlist('images')
    
    if len(images) < 10:
        return jsonify({
            'error': f'En az 10 görüntü gerekli, {len(images)} tane gönderildi'
        }), 400
    
    embeddings = []
    processed_count = 0
    
    try:
        for idx, image_file in enumerate(images):
            # Dosyayı oku
            file_bytes = np.frombuffer(image_file.read(), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            if image is None:
                continue
            
            # Yüz tespit et
            try:
                faces = detector.detect_faces(image)
                
                if not faces:
                    continue
                
                # Embedding üret
                embedding = processor.get_embedding(faces[0], normalize=True)
                
                # Şifrele
                encrypted_b64, hmac_b64 = crypto_manager.encrypt_embedding(embedding)
                
                embeddings.append({
                    'encrypted': encrypted_b64,
                    'hmac': hmac_b64,
                    'pose_index': idx
                })
                
                processed_count += 1
                
            except ValueError as e:
                # Çoklu yüz hatası - bu görüntüyü atla
                continue
        
        if processed_count < 10:
            return jsonify({
                'error': f'En az 10 geçerli yüz embedding\'i gerekli, {processed_count} tane işlendi'
            }), 400
        
        # Kullanıcıyı kaydet
        user_id = db_manager.create_user(username, embeddings)
        
        return jsonify({
            'user_id': user_id,
            'username': username,
            'embeddings_count': processed_count,
            'message': 'Kullanıcı başarıyla kaydedildi'
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'İşlem hatası: {str(e)}'}), 500
