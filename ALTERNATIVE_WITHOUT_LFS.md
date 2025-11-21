# Альтернативные способы загрузки без Git LFS

Если вы не хотите устанавливать Git LFS, есть несколько альтернативных способов работы с большим файлом `Template.xml` (22.65 МБ).

## Вариант 1: Хранить Template.xml отдельно (Рекомендуется)

### Шаг 1: Исключите Template.xml из репозитория

Добавьте в `.gitignore`:
```
Template.xml
```

### Шаг 2: Загрузите файл в облачное хранилище

Варианты:
- **Google Drive** - создайте публичную ссылку
- **Dropbox** - создайте публичную ссылку
- **GitHub Releases** - загрузите как релиз
- **Облачное хранилище вашей организации**

### Шаг 3: Модифицируйте код для автоматической загрузки

Обновите `src/main.py` для загрузки файла при первом запуске:

```python
import requests
from pathlib import Path
import streamlit as st

# URL к файлу (можно хранить в секретах Streamlit)
TEMPLATE_XML_URL = st.secrets.get(
    "TEMPLATE_XML_URL", 
    "https://your-link-to-file.com/Template.xml"
)

XML_FILE_PATH = project_root / "Template.xml"

# Загрузка файла, если его нет
if not XML_FILE_PATH.exists():
    with st.spinner("Загрузка Template.xml..."):
        try:
            response = requests.get(TEMPLATE_XML_URL, timeout=60)
            response.raise_for_status()
            XML_FILE_PATH.write_bytes(response.content)
            st.success("✅ Template.xml загружен")
        except Exception as e:
            st.error(f"❌ Ошибка загрузки Template.xml: {str(e)}")
            st.stop()
```

### Шаг 4: Для Streamlit Community Cloud

1. Загрузите `Template.xml` в облачное хранилище
2. Получите прямую ссылку на скачивание
3. Добавьте URL в секреты Streamlit:
   - В настройках приложения: Settings → Secrets
   - Добавьте:
     ```toml
     TEMPLATE_XML_URL = "https://your-link-to-file.com/Template.xml"
     ```

---

## Вариант 2: Сжать файл

Если `Template.xml` можно сжать:

1. Создайте архив: `Template.xml.zip` или `Template.xml.gz`
2. Загрузите архив в репозиторий (он будет меньше 25 МБ)
3. Модифицируйте код для распаковки:

```python
import zipfile
import gzip
from pathlib import Path

XML_FILE_PATH = project_root / "Template.xml"
XML_ZIP_PATH = project_root / "Template.xml.zip"

if not XML_FILE_PATH.exists() and XML_ZIP_PATH.exists():
    with st.spinner("Распаковка Template.xml..."):
        with zipfile.ZipFile(XML_ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(project_root)
```

---

## Вариант 3: Разбить файл на части

Если файл можно разделить на логические части, можно:

1. Разбить XML на несколько файлов
2. Загрузить все части в репозиторий
3. Объединить при загрузке

---

## Вариант 4: Использовать GitHub Releases

1. Загрузите `Template.xml` как файл релиза на GitHub
2. Скачивайте при деплое через API GitHub

---

## Рекомендация

**Используйте Вариант 1** - это самый простой и надежный способ:
- Не требует Git LFS
- Файл хранится отдельно
- Легко обновлять файл без изменения кода
- Работает на всех платформах

---

## Быстрая настройка (Вариант 1)

1. Добавьте в `.gitignore`:
   ```
   Template.xml
   ```

2. Загрузите `Template.xml` в Google Drive или другое хранилище

3. Получите прямую ссылку на скачивание

4. Обновите код (см. пример выше)

5. Загрузите репозиторий на GitHub без `Template.xml`

6. При деплое добавьте URL в секреты Streamlit

---

## Обновление requirements.txt

Если используете вариант с загрузкой через requests, убедитесь, что в `requirements.txt` есть:

```
requests>=2.28.0
```


