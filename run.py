"""
Скрипт для запуска Streamlit приложения.
Запускайте этот файл из корневой директории проекта.
"""

import subprocess
import sys
import shutil
from pathlib import Path

if __name__ == "__main__":
    # Получаем путь к main.py
    project_root = Path(__file__).parent
    main_file = project_root / "src" / "main.py"
    
    # Пытаемся использовать Python 3.12 через py launcher
    python_cmd = shutil.which("py")
    if python_cmd:
        # Используем py launcher с указанием версии 3.12
        subprocess.run([python_cmd, "-3.12", "-m", "streamlit", "run", str(main_file)])
    else:
        # Fallback на sys.executable
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(main_file)])

