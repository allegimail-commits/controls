"""
Модуль для создания эмбеддингов из текста контролей.
"""

from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """
    Генератор эмбеддингов для контролей.
    Использует модель paraphrase-multilingual-MiniLM-L12-v2 для поддержки русского языка.
    """
    
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Инициализирует генератор эмбеддингов.
        
        Args:
            model_name: Название модели для создания эмбеддингов
        """
        self.model_name = model_name
        self.model = None
    
    def load_model(self):
        """Загружает модель эмбеддингов."""
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Генерирует эмбеддинг для одного текста.
        
        Args:
            text: Текст для векторизации
            
        Returns:
            Список чисел (вектор эмбеддинга)
        """
        if self.model is None:
            self.load_model()
        
        if not text:
            # Возвращаем нулевой вектор той же размерности
            embedding = self.model.encode(" ")
            return embedding.tolist()
        
        embedding = self.model.encode(text, show_progress_bar=False)
        return embedding.tolist()
    
    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Генерирует эмбеддинги для списка текстов.
        
        Args:
            texts: Список текстов для векторизации
            batch_size: Размер батча для обработки
            
        Returns:
            Список векторов эмбеддингов
        """
        if self.model is None:
            self.load_model()
        
        if not texts:
            return []
        
        # Заменяем пустые тексты на пробел
        processed_texts = [text if text else " " for text in texts]
        
        embeddings = self.model.encode(
            processed_texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        return embeddings.tolist()

