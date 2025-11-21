"""
Команды графического интерфейса, включая создание векторной БД.
"""

import streamlit as st
from pathlib import Path
from typing import Callable, Optional
from ..vector_db.chroma_manager import ChromaDBManager
from ..models.control import Control


def render_create_vector_db_command(controls: list[Control], xml_path: str) -> None:
    """
    Отображает команду создания векторной БД.
    
    Args:
        controls: Список контролей для векторизации
        xml_path: Путь к исходному XML файлу
    """
    st.header("🗄️ Создание векторной БД")
    
    st.info("Эта команда создаст векторную базу данных ChromaDB на основе макета Template.xml")
    
    # Параметры
    with st.expander("⚙️ Параметры", expanded=False):
        db_path = st.text_input(
            "Путь к директории БД",
            value="chroma_db",
            help="Директория для хранения векторной БД"
        )
        
        collection_name = st.text_input(
            "Название коллекции",
            value="controls",
            help="Название коллекции в ChromaDB"
        )
        
        model_name = st.selectbox(
            "Модель эмбеддингов",
            options=[
                "paraphrase-multilingual-MiniLM-L12-v2",
                "all-MiniLM-L6-v2",
            ],
            index=0,
            help="Модель для создания эмбеддингов (рекомендуется multilingual для русского языка)"
        )
    
    # Кнопка создания БД
    if st.button("🚀 Создать векторную БД", type="primary", use_container_width=True):
        if not controls:
            st.error("Нет контролей для обработки. Загрузите Template.xml сначала.")
            return
        
        try:
            # Инициализируем менеджер
            db_manager = ChromaDBManager(db_path=db_path, collection_name=collection_name)
            db_manager.embedding_generator.model_name = model_name
            
            # Создаем прогресс-бар
            progress_bar = st.progress(0)
            status_text = st.empty()
            log_container = st.container()
            
            def progress_callback(current: int, total: int, message: str):
                """Обратный вызов для отображения прогресса."""
                progress = current / total if total > 0 else 0
                progress_bar.progress(progress)
                status_text.text(f"{message} ({current}/{total})")
                
                # Логируем в контейнер
                with log_container:
                    st.text(f"✓ {message}")
            
            # Создаем БД
            with st.spinner("Создание векторной БД..."):
                db_manager.create_database_from_controls(controls, progress_callback=progress_callback)
            
            # Успех
            progress_bar.progress(1.0)
            status_text.text("Готово!")
            st.success(f"✅ Векторная БД успешно создана! Обработано {len(controls)} контролей.")
            
            # Показываем информацию о БД
            count = db_manager.get_collection_count()
            st.info(f"📊 В базе данных: {count} элементов")
            
        except Exception as e:
            st.error(f"❌ Ошибка при создании векторной БД: {str(e)}")
            st.exception(e)

