# Следующие шаги: Коммит и загрузка на GitHub

✅ **Репозиторий инициализирован**  
✅ **Git LFS настроен**  
✅ **Template.xml отслеживается через LFS**  
✅ **Все файлы добавлены**

Теперь нужно создать коммит и загрузить на GitHub.

## Шаг 1: Настройте Git (если еще не настроен)

Выполните в PowerShell (замените на ваши данные):

```powershell
git config --global user.name "Ваше Имя"
git config --global user.email "ваш@email.com"
```

## Шаг 2: Создайте первый коммит

```powershell
cd D:\projects\DK
git commit -m "Initial commit: Streamlit app for controls management"
```

## Шаг 3: Проверьте, что Template.xml в LFS

```powershell
git lfs ls-files
```

Должен показать `Template.xml`.

## Шаг 4: Создайте репозиторий на GitHub

1. Зайдите на https://github.com
2. Войдите в свой аккаунт (или создайте новый)
3. Нажмите **"New repository"** (или "+" → "New repository")
4. Заполните форму:
   - **Repository name**: `dk-controls-app` (или любое другое имя)
   - **Description**: "Информационная система по дополнительным контролям"
   - **Visibility**: 
     - Public - все могут видеть
     - Private - только вы можете видеть
   - **ВАЖНО:** НЕ ставьте галочки на:
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license
   (У вас уже есть эти файлы!)
5. Нажмите **"Create repository"**

## Шаг 5: Подключите локальный репозиторий к GitHub

После создания репозитория GitHub покажет инструкции. Выполните команды (замените YOUR_USERNAME и REPO_NAME на ваши значения):

```powershell
# Добавьте удаленный репозиторий
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Переименуйте ветку в main (если нужно)
git branch -M main

# Загрузите код на GitHub
git push -u origin main
```

**Пример:**
Если ваш username `oleg123`, а репозиторий называется `dk-controls-app`, команда будет:
```powershell
git remote add origin https://github.com/oleg123/dk-controls-app.git
git branch -M main
git push -u origin main
```

## Шаг 6: Проверьте результат

1. Обновите страницу репозитория на GitHub
2. Убедитесь, что все файлы загружены:
   - ✅ Папка `src/` со всеми подпапками
   - ✅ `Template.xml` (должен быть помечен как LFS)
   - ✅ Все `.py` файлы
   - ✅ Конфигурационные файлы
   - ❌ `chroma_db/` НЕ должна быть видна
   - ❌ `__pycache__/` НЕ должна быть видна

## Готово! ✅

Теперь ваш репозиторий на GitHub. Следующий шаг - публикация приложения:
- См. `DEPLOYMENT.md` для инструкций по деплою на Streamlit Community Cloud

---

## Возможные проблемы

### Ошибка: "remote origin already exists"

Если репозиторий уже подключен, удалите и добавьте заново:
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### Ошибка: "Authentication failed"

1. GitHub больше не поддерживает пароли для Git
2. Используйте Personal Access Token:
   - Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token
   - Выберите права: `repo`
   - Используйте токен вместо пароля при `git push`

### Ошибка: "Template.xml too large"

Убедитесь, что Git LFS работает:
```powershell
git lfs ls-files
git lfs track "Template.xml"
git add Template.xml
```

### Ошибка при push: "LFS objects not found"

```powershell
git lfs push origin main --all
```

---

**Нужна помощь?** См. `GITHUB_UPLOAD_GUIDE.md` для подробной инструкции.

