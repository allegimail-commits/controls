"""
Скрипт для создания векторной БД на основе макета Template.xml.
Запускайте этот скрипт из корневой директории проекта.
"""

import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь для импортов
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.parser.xml_parser import load_controls
from src.vector_db.chroma_manager import ChromaDBManager


def create_vector_database():
    """Создает векторную БД из Template.xml"""
    
    # Путь к XML файлу
    xml_path = project_root / "Template.xml"
    
    if not xml_path.exists():
        print(f"[ERROR] Файл Template.xml не найден по пути: {xml_path}")
        return False
    
    print("[INFO] Загрузка контролей из Template.xml...")
    try:
        controls = load_controls(str(xml_path))
        print(f"[OK] Загружено {len(controls)} контролей")
    except Exception as e:
        print(f"[ERROR] Ошибка при загрузке XML: {e}")
        return False
    
    if not controls:
        print("[ERROR] Не найдено контролей для обработки")
        return False
    
    # Параметры БД
    db_path = "chroma_db"
    collection_name = "controls"
    model_name = "paraphrase-multilingual-MiniLM-L12-v2"
    
    print(f"\n[INFO] Создание векторной БД...")
    print(f"   Путь к БД: {db_path}")
    print(f"   Коллекция: {collection_name}")
    print(f"   Модель: {model_name}")
    print()
    
    try:
        # Инициализируем менеджер
        db_manager = ChromaDBManager(db_path=db_path, collection_name=collection_name)
        db_manager.embedding_generator.model_name = model_name
        
        # Callback для отображения прогресса
        def progress_callback(current: int, total: int, message: str):
            percentage = (current / total * 100) if total > 0 else 0
            print(f"   [{percentage:5.1f}%] {message}")
        
        # Создаем БД
        db_manager.create_database_from_controls(controls, progress_callback=progress_callback)
        
        # Проверяем результат
        count = db_manager.get_collection_count()
        print(f"\n[OK] Векторная БД успешно создана!")
        print(f"   Обработано контролей: {len(controls)}")
        print(f"   Элементов в БД: {count}")
        print(f"   Путь к БД: {Path(db_path).absolute()}")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Ошибка при создании векторной БД: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Создание векторной БД на основе макета Template.xml")
    print("=" * 60)
    print()
    
    success = create_vector_database()
    
    print()
    if success:
        print("=" * 60)
        print("[OK] Процесс завершен успешно!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("=" * 60)
        print("[ERROR] Процесс завершен с ошибками")
        print("=" * 60)
        sys.exit(1)

