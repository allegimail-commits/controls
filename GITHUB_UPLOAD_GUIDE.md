# Инструкция по загрузке репозитория на GitHub

Это пошаговая инструкция по правильной загрузке вашего проекта на GitHub.

## Шаг 1: Проверьте структуру проекта

Убедитесь, что у вас есть все необходимые файлы:

### Обязательные файлы и папки:

```
DK/
├── .streamlit/
│   └── config.toml          # Конфигурация Streamlit
├── src/                      # Исходный код
│   ├── __init__.py
│   ├── main.py              # Главный файл приложения
│   ├── gui/                 # GUI компоненты
│   │   ├── __init__.py
│   │   ├── commands.py
│   │   ├── details_view.py
│   │   ├── filters.py
│   │   └── list_view.py
│   ├── models/              # Модели данных
│   │   ├── __init__.py
│   │   └── control.py
│   ├── parser/              # Парсеры
│   │   ├── __init__.py
│   │   └── xml_parser.py
│   └── vector_db/           # Работа с векторной БД
│       ├── __init__.py
│       ├── chroma_manager.py
│       └── embeddings.py
├── Template.xml             # XML файл (22.65 МБ - нужен Git LFS)
├── requirements.txt         # Зависимости
├── run.py                   # Скрипт запуска
├── README.md                # Документация
├── .gitignore               # Игнорируемые файлы
├── .gitattributes           # Настройки Git LFS
├── Dockerfile               # Для Docker деплоя
├── Procfile                 # Для Heroku деплоя
└── DEPLOYMENT.md            # Инструкции по деплою
```

### Файлы, которые НЕ должны быть в репозитории (уже в .gitignore):

- `chroma_db/` - база данных (создается автоматически)
- `__pycache__/` - кэш Python
- `.cache/` - кэш моделей
- `venv/` - виртуальное окружение

---

## Шаг 2: Установите Git LFS (если еще не установлен)

Файл `Template.xml` весит 22.65 МБ, поэтому нужен Git LFS.

### Windows:

1. Скачайте установщик: https://git-lfs.github.com/
2. Или через winget:
   ```powershell
   winget install GitHub.GitLFS
   ```
3. Проверьте установку:
   ```bash
   git lfs version
   ```

---

## Шаг 3: Инициализируйте Git репозиторий (если еще не сделано)

```bash
cd D:\projects\DK

# Инициализируйте Git
git init

# Настройте Git LFS
git lfs install

# Добавьте Template.xml в LFS
git lfs track "Template.xml"
```

---

## Шаг 4: Добавьте файлы в репозиторий

### 4.1. Проверьте статус:

```bash
git status
```

Вы должны увидеть список файлов, которые будут добавлены.

### 4.2. Добавьте все файлы:

```bash
# Добавьте конфигурационные файлы
git add .gitignore
git add .gitattributes
git add .streamlit/config.toml

# Добавьте исходный код
git add src/
git add *.py
git add requirements.txt

# Добавьте документацию
git add *.md

# Добавьте файлы для деплоя
git add Dockerfile
git add Procfile
git add .dockerignore

# Добавьте Template.xml (через LFS)
git add Template.xml
```

Или добавьте все сразу (кроме игнорируемых):
```bash
git add .
```

### 4.3. Проверьте, что Template.xml в LFS:

```bash
git lfs ls-files
```

Должен показать `Template.xml`.

---

## Шаг 5: Убедитесь, что chroma_db НЕ добавлена

Проверьте, что `chroma_db/` не в списке файлов для коммита:

```bash
git status
```

Если `chroma_db/` там есть, удалите ее:
```bash
git rm --cached -r chroma_db/
```

---

## Шаг 6: Создайте первый коммит

```bash
git commit -m "Initial commit: Streamlit app for controls management"
```

---

## Шаг 7: Создайте репозиторий на GitHub

1. Зайдите на https://github.com
2. Нажмите "New repository" (или "+" → "New repository")
3. Заполните:
   - **Repository name**: `dk-controls-app` (или любое другое имя)
   - **Description**: "Информационная система по дополнительным контролям"
   - **Visibility**: Public или Private (на ваше усмотрение)
   - **НЕ** добавляйте README, .gitignore или лицензию (у вас уже есть)
4. Нажмите "Create repository"

---

## Шаг 8: Подключите локальный репозиторий к GitHub

GitHub покажет инструкции, но вот команды:

```bash
# Добавьте удаленный репозиторий (замените YOUR_USERNAME и REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Переименуйте ветку в main (если нужно)
git branch -M main

# Загрузите код на GitHub
git push -u origin main
```

---

## Шаг 9: Проверьте результат

1. Обновите страницу репозитория на GitHub
2. Убедитесь, что все папки и файлы загружены:
   - ✅ `src/` со всеми подпапками
   - ✅ `Template.xml` (должен быть помечен как LFS)
   - ✅ Все `.py` файлы
   - ✅ Конфигурационные файлы
   - ❌ `chroma_db/` НЕ должна быть видна
   - ❌ `__pycache__/` НЕ должна быть видна

---

## Возможные проблемы и решения

### Проблема: Папки пустые на GitHub

**Причина:** Папки содержат только `__pycache__/`, который игнорируется.

**Решение:** Убедитесь, что в каждой папке есть файлы `.py` или `__init__.py`:
```bash
# Проверьте структуру
Get-ChildItem -Recurse -File | Where-Object { $_.Extension -eq '.py' }
```

### Проблема: Template.xml не загружается

**Причина:** Git LFS не настроен или файл слишком большой.

**Решение:**
1. Убедитесь, что Git LFS установлен: `git lfs version`
2. Выполните: `git lfs track "Template.xml"`
3. Добавьте файл: `git add Template.xml`
4. Проверьте: `git lfs ls-files`

### Проблема: chroma_db загружается (не должна)

**Решение:**
```bash
git rm --cached -r chroma_db/
git commit -m "Remove chroma_db from repository"
git push
```

### Проблема: Ошибка "file too large"

**Решение:** Используйте Git LFS для больших файлов (см. `GIT_LFS_SETUP.md`)

---

## Быстрая проверка перед загрузкой

Выполните эти команды для проверки:

```bash
# Проверьте, что все важные файлы на месте
dir src\main.py
dir Template.xml
dir requirements.txt
dir .streamlit\config.toml

# Проверьте статус Git
git status

# Проверьте, что Template.xml в LFS
git lfs ls-files

# Проверьте, что chroma_db игнорируется
git check-ignore chroma_db/
```

---

## После успешной загрузки

Теперь вы можете:
1. Деплоить на Streamlit Community Cloud (см. `DEPLOYMENT.md`)
2. Клонировать репозиторий на других компьютерах
3. Работать в команде

---

## Полезные команды

```bash
# Посмотреть, что будет закоммичено
git status

# Посмотреть, что игнорируется
git status --ignored

# Проверить размер файлов
git ls-files | ForEach-Object { if (Test-Path $_) { Get-Item $_ | Select-Object Name, @{Name='Size(MB)';Expression={[math]::Round($_.Length/1MB, 2)}} } }
```


