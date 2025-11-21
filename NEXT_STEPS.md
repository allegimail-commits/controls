# Следующие шаги: Настройка репозитория

✅ **Git установлен:** версия 2.52.0  
✅ **Git LFS установлен:** версия 3.7.1

Winget не нужен - у вас уже все установлено! Теперь нужно настроить репозиторий.

## Шаг 1: Настройте Git (если еще не настроен)

Выполните в PowerShell (замените на ваши данные):

```powershell
git config --global user.name "Ваше Имя"
git config --global user.email "ваш@email.com"
```

## Шаг 2: Инициализируйте репозиторий

```powershell
cd D:\projects\DK
git init
```

## Шаг 3: Настройте Git LFS для Template.xml

```powershell
git lfs install
git lfs track "Template.xml"
```

## Шаг 4: Добавьте файлы в репозиторий

```powershell
git add .
```

## Шаг 5: Проверьте, что будет загружено

```powershell
git status
```

**Убедитесь, что:**
- ✅ Папка `src/` и все файлы добавлены
- ✅ `Template.xml` добавлен
- ✅ Все `.py` файлы добавлены
- ❌ `chroma_db/` НЕ должна быть в списке
- ❌ `__pycache__/` НЕ должна быть в списке

## Шаг 6: Создайте первый коммит

```powershell
git commit -m "Initial commit: Streamlit app for controls management"
```

## Шаг 7: Проверьте, что Template.xml в LFS

```powershell
git lfs ls-files
```

Должен показать `Template.xml`.

## Шаг 8: Создайте репозиторий на GitHub

1. Зайдите на https://github.com
2. Нажмите "New repository" (или "+" → "New repository")
3. Заполните:
   - **Repository name**: `dk-controls-app` (или любое другое имя)
   - **Description**: "Информационная система по дополнительным контролям"
   - **Visibility**: Public или Private
   - **НЕ** добавляйте README, .gitignore или лицензию (у вас уже есть)
4. Нажмите "Create repository"

## Шаг 9: Подключите локальный репозиторий к GitHub

GitHub покажет инструкции, но вот команды (замените YOUR_USERNAME и REPO_NAME):

```powershell
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## Готово! ✅

Теперь ваш репозиторий на GitHub.

---

## Если возникли проблемы

### Проблема: "Template.xml" не в LFS

```powershell
git lfs track "Template.xml"
git add .gitattributes
git add Template.xml
git commit -m "Add Template.xml via Git LFS"
```

### Проблема: chroma_db загружается (не должна)

```powershell
git rm --cached -r chroma_db/
git commit -m "Remove chroma_db from repository"
```

### Проблема: Папки не загружаются

```powershell
# Принудительно добавьте папку src
git add -f src/
```

---

**Подробная инструкция:** `GITHUB_UPLOAD_GUIDE.md`  
**Быстрая шпаргалка:** `QUICK_START.md`

