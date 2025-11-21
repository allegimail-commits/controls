# Быстрый старт БЕЗ Git LFS

Если вы не хотите устанавливать Git LFS, используйте этот вариант.

## Шаг 1: Установите Git (если еще не установлен)

```powershell
winget install --id Git.Git -e --source winget
```

Перезапустите PowerShell после установки.

## Шаг 2: Исключите Template.xml из репозитория

Добавьте в `.gitignore` (если еще нет):
```
Template.xml
```

## Шаг 3: Инициализируйте Git репозиторий

```bash
cd D:\projects\DK
git init
```

## Шаг 4: Добавьте файлы (без Template.xml)

```bash
git add .
```

Проверьте, что `Template.xml` НЕ в списке:
```bash
git status
```

## Шаг 5: Создайте коммит

```bash
git commit -m "Initial commit: Streamlit app for controls management"
```

## Шаг 6: Создайте репозиторий на GitHub

1. Зайдите на https://github.com
2. Создайте новый репозиторий (НЕ добавляйте README, .gitignore)

## Шаг 7: Загрузите код

```bash
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## Шаг 8: Загрузите Template.xml отдельно

### Вариант A: GitHub Releases

1. На странице репозитория: Releases → Create a new release
2. Загрузите `Template.xml` как файл релиза
3. Получите прямую ссылку на скачивание

### Вариант B: Облачное хранилище

1. Загрузите `Template.xml` в Google Drive / Dropbox
2. Получите прямую ссылку на скачивание

## Шаг 9: Настройте автоматическую загрузку (для деплоя)

См. `ALTERNATIVE_WITHOUT_LFS.md` для инструкций по модификации кода.

---

## Готово! ✅

Теперь:
- Код на GitHub (без Template.xml)
- Template.xml хранится отдельно
- При деплое файл будет загружаться автоматически

**Подробная инструкция:** `ALTERNATIVE_WITHOUT_LFS.md`


