# Инструкция по публикации приложения

Этот документ описывает различные способы публикации вашего Streamlit приложения, чтобы другие люди могли открыть его в браузере.

## Вариант 1: Streamlit Community Cloud (Рекомендуется) ⭐

**Преимущества:**
- ✅ Бесплатно
- ✅ Простая настройка (5 минут)
- ✅ Автоматический деплой из GitHub
- ✅ HTTPS из коробки
- ✅ Не требует настройки сервера

**Требования:**
- Аккаунт на GitHub
- Репозиторий с вашим кодом

### Шаги:

1. **Создайте репозиторий на GitHub:**
   - Зайдите на https://github.com
   - Создайте новый репозиторий (например, `dk-controls-app`)
   - Загрузите туда весь код проекта

2. **Зарегистрируйтесь на Streamlit Community Cloud:**
   - Перейдите на https://share.streamlit.io/
   - Войдите через GitHub аккаунт

3. **Деплой приложения:**
   - Нажмите "New app"
   - Выберите ваш репозиторий
   - Укажите путь к главному файлу: `src/main.py`
   - Нажмите "Deploy"

4. **Важно:** 
   - Убедитесь, что файл `Template.xml` находится в репозитории в корневой директории проекта
   - Если файл больше 25 МБ, используйте Git LFS (см. `GIT_LFS_SETUP.md`)

5. **После деплоя:** Вы получите URL вида `https://your-app-name.streamlit.app`, который можно открыть в браузере

6. **Обновление приложения:** После внесения изменений в код:
   - Загрузите изменения на GitHub: `git add .`, `git commit -m "..."`, `git push`
   - Streamlit автоматически обнаружит изменения и обновит приложение через 1-2 минуты
   - Подробнее см. `UPDATE_APP.md`

---

## Вариант 2: Docker + любой хостинг

**Преимущества:**
- ✅ Работает на любом хостинге (AWS, Google Cloud, Azure, DigitalOcean и т.д.)
- ✅ Изолированная среда
- ✅ Легко масштабируется

### Шаги:

1. **Создайте Dockerfile** (уже создан в проекте)

2. **Соберите образ:**
   ```bash
   docker build -t dk-controls-app .
   ```

3. **Запустите контейнер:**
   ```bash
   docker run -p 8501:8501 dk-controls-app
   ```

4. **Для публикации:**
   - Загрузите образ в Docker Hub или Container Registry
   - Разверните на любом хостинге, поддерживающем Docker

---

## Вариант 3: VPS/Собственный сервер

**Преимущества:**
- ✅ Полный контроль
- ✅ Можно использовать свой домен
- ✅ Нет ограничений платформы

**Требования:**
- VPS с Linux (Ubuntu, Debian и т.д.)
- Python 3.8+
- Доступ по SSH

### Шаги:

1. **Подключитесь к серверу по SSH**

2. **Установите зависимости:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git
   ```

3. **Клонируйте репозиторий:**
   ```bash
   git clone <ваш-репозиторий>
   cd DK
   pip3 install -r requirements.txt
   ```

4. **Настройте файрвол:**
   ```bash
   sudo ufw allow 8501
   ```

5. **Запустите приложение:**
   ```bash
   streamlit run src/main.py --server.port 8501 --server.address 0.0.0.0
   ```

6. **Для постоянной работы используйте systemd или screen/tmux:**
   
   Создайте файл `/etc/systemd/system/dk-app.service`:
   ```ini
   [Unit]
   Description=DK Controls App
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/path/to/DK
   ExecStart=/usr/bin/python3 -m streamlit run src/main.py --server.port 8501 --server.address 0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Затем:
   ```bash
   sudo systemctl enable dk-app
   sudo systemctl start dk-app
   ```

7. **Настройте домен (опционально):**
   - Используйте Nginx как reverse proxy
   - Настройте SSL через Let's Encrypt

---

## Вариант 4: Heroku

**Преимущества:**
- ✅ Простой деплой
- ✅ Автоматическое масштабирование

**Недостатки:**
- ⚠️ Платный (бесплатный план отменен)

### Шаги:

1. Установите Heroku CLI
2. Создайте `Procfile`:
   ```
   web: streamlit run src/main.py --server.port=$PORT --server.address=0.0.0.0
   ```
3. Деплой:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

---

## Важные замечания

### Безопасность

- ⚠️ По умолчанию Streamlit не имеет аутентификации
- Для публичного доступа рассмотрите добавление пароля через `.streamlit/config.toml`:
  ```toml
  [server]
  enableXsrfProtection = true
  ```

- Или используйте Streamlit Authenticator для более сложной аутентификации

### Файл Template.xml

- Убедитесь, что файл `Template.xml` находится в репозитории
- При обновлении файла перезапустите приложение

### ChromaDB

- Векторная БД создается локально в директории `chroma_db`
- При деплое на облачные платформы эта директория может быть временной
- Для постоянного хранения используйте внешнее хранилище (S3, Google Cloud Storage и т.д.)

---

## Рекомендация

Для быстрого старта используйте **Streamlit Community Cloud** - это самый простой и бесплатный способ.

Для production окружения с требованиями безопасности и масштабирования рассмотрите **Docker + облачный хостинг** или **VPS**.

