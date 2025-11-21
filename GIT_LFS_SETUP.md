# Настройка Git LFS для больших файлов

В проекте есть большие файлы, которые превышают лимит GitHub (25 МБ):
- `Template.xml` - 22.65 МБ
- `chroma_db/chroma.sqlite3` - 147.7 МБ

Для работы с такими файлами нужно использовать **Git LFS** (Large File Storage).

**⚠️ ВАЖНО:** Файл `chroma.sqlite3` обычно **НЕ должен** храниться в репозитории - это временная база данных, которая создается автоматически при первом запуске. Убедитесь, что он в `.gitignore`.

## Вариант 1: Использование Git LFS (Рекомендуется)

### Шаг 1: Установите Git LFS

**Windows:**
- Скачайте установщик с https://git-lfs.github.com/
- Или через Chocolatey: `choco install git-lfs`
- Или через winget: `winget install GitHub.GitLFS`

**Проверка установки:**
```bash
git lfs version
```

### Шаг 2: Инициализируйте Git LFS в репозитории

```bash
cd D:\projects\DK
git lfs install
```

### Шаг 3: Добавьте файлы в Git LFS

```bash
# Добавьте Template.xml в LFS
git lfs track "Template.xml"

# Если нужно хранить chroma.sqlite3 (НЕ рекомендуется - см. ниже)
# git lfs track "*.sqlite3"

# Добавьте файлы в индекс
git add .gitattributes
git add Template.xml

# Коммит и пуш
git commit -m "Add Template.xml via Git LFS"
git push
```

### Шаг 4: Проверьте, что файл в LFS

```bash
git lfs ls-files
```

Должен показать `Template.xml`.

---

## Вариант 2: Хранить файл отдельно (Альтернатива)

Если не хотите использовать Git LFS, можно хранить `Template.xml` отдельно и загружать его при деплое.

### Для Streamlit Community Cloud:

1. **Удалите Template.xml из репозитория:**
   - Добавьте в `.gitignore`: `Template.xml`
   - Удалите из git: `git rm --cached Template.xml`

2. **Загрузите файл в облачное хранилище:**
   - Google Drive, Dropbox, или другой сервис
   - Получите прямую ссылку на скачивание

3. **Модифицируйте код для загрузки файла:**
   - При первом запуске скачивайте `Template.xml` из облака
   - Или используйте секреты Streamlit для хранения URL

### Пример кода для загрузки файла:

```python
import requests
from pathlib import Path

XML_URL = st.secrets.get("TEMPLATE_XML_URL", "https://your-link-to-file.com/Template.xml")
XML_FILE_PATH = project_root / "Template.xml"

if not XML_FILE_PATH.exists():
    with st.spinner("Загрузка Template.xml..."):
        response = requests.get(XML_URL)
        XML_FILE_PATH.write_bytes(response.content)
```

---

## Вариант 3: Сжать файл (если возможно)

Если `Template.xml` можно сжать без потери функциональности:

1. Создайте архив: `Template.xml.zip` или `Template.xml.gz`
2. Загрузите архив в репозиторий
3. Модифицируйте код для распаковки при запуске

---

## Рекомендация

**Используйте Вариант 1 (Git LFS)** - это стандартный способ работы с большими файлами в Git. GitHub предоставляет 1 ГБ бесплатного хранилища LFS, что более чем достаточно для вашего файла.

---

## О файле chroma.sqlite3

**⚠️ ВАЖНО:** Файл `chroma.sqlite3` (147.7 МБ) - это база данных ChromaDB, которая:
- Создается автоматически при первом запуске приложения
- Содержит векторные данные, которые можно пересоздать из `Template.xml`
- **НЕ должна храниться в репозитории** - она уже в `.gitignore`

### Если файл уже в репозитории:

1. **Удалите его из Git (но оставьте локально):**
   ```bash
   git rm --cached chroma_db/chroma.sqlite3
   git commit -m "Remove chroma.sqlite3 from repository"
   ```

2. **Убедитесь, что он в `.gitignore`:**
   - Проверьте, что в `.gitignore` есть `chroma_db/` и `*.sqlite3`

3. **При деплое:** База данных будет создана автоматически при первом запуске

### Если все же нужно хранить базу данных:

Если у вас есть веская причина хранить `chroma.sqlite3` в репозитории:
```bash
git lfs track "*.sqlite3"
git add chroma_db/chroma.sqlite3
git commit -m "Add chroma.sqlite3 via Git LFS"
```

Но это **не рекомендуется**, так как файл очень большой и может быть пересоздан.

---

## Важные замечания

- ⚠️ Если файл уже был закоммичен без LFS, нужно переписать историю:
  ```bash
  git lfs migrate import --include="Template.xml" --everything
  ```

- ⚠️ Все, кто клонирует репозиторий, должны иметь установленный Git LFS

- ⚠️ При деплое на Streamlit Community Cloud Git LFS поддерживается автоматически

- ⚠️ **Удалите chroma.sqlite3 из репозитория**, если он там есть - он будет создан автоматически

