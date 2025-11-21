"""
Модуль для работы с ChromaDB - создание и управление векторной БД.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Optional
from pathlib import Path

from ..models.control import Control
from .embeddings import EmbeddingGenerator


class ChromaDBManager:
    """
    Менеджер для работы с ChromaDB.
    Создает и управляет векторной базой данных контролей.
    """
    
    def __init__(self, db_path: str = "chroma_db", collection_name: str = "controls"):
        """
        Инициализирует менеджер ChromaDB.
        
        Args:
            db_path: Путь к директории для хранения БД
            collection_name: Название коллекции в БД
        """
        self.db_path = Path(db_path)
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self.embedding_generator = EmbeddingGenerator()
    
    def initialize(self):
        """Инициализирует клиент ChromaDB и коллекцию."""
        if self.client is None:
            # Создаем директорию если не существует
            self.db_path.mkdir(parents=True, exist_ok=True)
            
            self.client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=Settings(anonymized_telemetry=False)
            )
        
        # Получаем или создаем коллекцию
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
        except Exception:
            # Коллекция не существует, создаем новую
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Коллекция дополнительных контролей"}
            )
    
    def create_database_from_controls(self, controls: List[Control], progress_callback=None):
        """
        Создает векторную БД из списка контролей.
        
        Args:
            controls: Список контролей для векторизации
            progress_callback: Функция обратного вызова для отображения прогресса
                               Принимает (current, total, message)
        """
        if not controls:
            raise ValueError("Список контролей пуст")
        
        self.initialize()
        self.embedding_generator.load_model()
        
        # Очищаем существующую коллекцию
        try:
            self.client.delete_collection(name=self.collection_name)
        except Exception:
            pass
        
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "Коллекция дополнительных контролей"}
        )
        
        total = len(controls)
        
        # Подготавливаем данные для батч-обработки
        texts = []
        metadatas = []
        ids = []
        
        if progress_callback:
            progress_callback(0, total, "Подготовка данных...")
        
        for idx, control in enumerate(controls):
            # Создаем текст для эмбеддинга
            text = control.get_text_for_embedding()
            texts.append(text)
            
            # Создаем метаданные
            metadata = control.to_dict()
            metadatas.append(metadata)
            
            # Создаем ID
            control_id = f"control_{idx}_{control.identifier}" if control.identifier else f"control_{idx}"
            ids.append(control_id)
        
        if progress_callback:
            progress_callback(0, total, "Генерация эмбеддингов...")
        
        # Генерируем эмбеддинги батчами
        embeddings = self.embedding_generator.generate_embeddings_batch(texts, batch_size=32)
        
        if progress_callback:
            progress_callback(0, total, "Сохранение в базу данных...")
        
        # Добавляем в ChromaDB батчами
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]
            batch_metadatas = metadatas[i:i + batch_size]
            batch_texts = texts[i:i + batch_size]
            
            self.collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,
                metadatas=batch_metadatas,
                documents=batch_texts
            )
            
            if progress_callback:
                progress_callback(min(i + batch_size, total), total, 
                                 f"Обработано {min(i + batch_size, total)} из {total} контролей...")
        
        if progress_callback:
            progress_callback(total, total, "Готово!")
    
    def search(self, query: str, n_results: int = 10) -> List[dict]:
        """
        Выполняет семантический поиск по векторной БД.
        
        Args:
            query: Текст запроса
            n_results: Количество результатов
            
        Returns:
            Список словарей с результатами поиска
        """
        if self.collection is None:
            self.initialize()
        
        if not query:
            return []
        
        # Генерируем эмбеддинг для запроса
        query_embedding = self.embedding_generator.generate_embedding(query)
        
        # Выполняем поиск
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Форматируем результаты
        formatted_results = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                result = {
                    'id': results['ids'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None,
                    'document': results['documents'][0][i] if 'documents' in results else None
                }
                formatted_results.append(result)
        
        return formatted_results
    
    def get_collection_count(self) -> int:
        """
        Возвращает количество элементов в коллекции.
        
        Returns:
            Количество элементов
        """
        if self.collection is None:
            self.initialize()
        
        return self.collection.count()

