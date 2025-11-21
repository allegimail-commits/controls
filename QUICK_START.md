# Быстрый старт: Загрузка на GitHub

## ⚠️ ВАЖНО: Сначала установите Git!

Если у вас ошибка "could not find git", сначала установите Git:

```powershell
# Установите Git
winget install --id Git.Git -e --source winget

# Перезапустите PowerShell после установки!
# Затем установите Git LFS
winget install GitHub.GitLFS
```

**Подробная инструкция:** `INSTALL_GIT.md`

**Альтернатива без Git LFS:** `ALTERNATIVE_WITHOUT_LFS.md` (хранить Template.xml отдельно)

---

## Шаг 1: Проверьте структуру

```powershell
.\check_repo_structure.ps1
```

## Шаг 2: Установите Git LFS (если еще не установлен)

```powershell
# Сначала убедитесь, что Git установлен
git --version

# Затем установите Git LFS
winget install GitHub.GitLFS
git lfs install
```

## Шаг 3: Настройте Git LFS для Template.xml

```bash
git lfs track "Template.xml"
git add .gitattributes
```

## Шаг 4: Добавьте все файлы

```bash
git add .
```

## Шаг 5: Проверьте, что будет загружено

```bash
git status
```

**Убедитесь, что:**
- ✅ `src/` и все подпапки добавлены
- ✅ `Template.xml` добавлен
- ❌ `chroma_db/` НЕ добавлена
- ❌ `__pycache__/` НЕ добавлена

## Шаг 6: Создайте коммит

```bash
git commit -m "Initial commit: Streamlit app for controls management"
```

## Шаг 7: Создайте репозиторий на GitHub

1. Зайдите на https://github.com
2. Нажмите "New repository"
3. Создайте репозиторий (НЕ добавляйте README, .gitignore, лицензию)

## Шаг 8: Подключите и загрузите

```bash
# Замените YOUR_USERNAME и REPO_NAME на ваши значения
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## Готово! ✅

Теперь ваш репозиторий на GitHub. См. `DEPLOYMENT.md` для публикации приложения.

---

## Если что-то пошло не так

### Папки не загружаются?

1. Проверьте, что в папках есть файлы (не только `__pycache__`)
2. Убедитесь, что папки не в `.gitignore`
3. Выполните: `git add -f src/` (принудительное добавление)

### Template.xml не загружается?

1. Проверьте Git LFS: `git lfs version`
2. Выполните: `git lfs track "Template.xml"`
3. Добавьте файл: `git add Template.xml`
4. Проверьте: `git lfs ls-files`

### chroma_db загружается (не должна)?

```bash
git rm --cached -r chroma_db/
git commit -m "Remove chroma_db"
```

---

**Подробная инструкция:** `GITHUB_UPLOAD_GUIDE.md`

