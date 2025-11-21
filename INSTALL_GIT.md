# Установка Git и Git LFS

## Проблема

Git LFS не может быть установлен, потому что Git не установлен на вашем компьютере.

## Решение: Установите Git

### Вариант 1: Через winget (Рекомендуется)

```powershell
# Установите Git
winget install --id Git.Git -e --source winget

# После установки перезапустите PowerShell или командную строку
# Затем установите Git LFS
winget install GitHub.GitLFS
```

### Вариант 2: Через официальный установщик

1. Скачайте Git для Windows: https://git-scm.com/download/win
2. Запустите установщик
3. Используйте настройки по умолчанию (просто нажимайте "Next")
4. После установки перезапустите PowerShell
5. Установите Git LFS: https://git-lfs.github.com/

### Вариант 3: Через Chocolatey (если установлен)

```powershell
choco install git
choco install git-lfs
```

## Проверка установки

После установки откройте **новое** окно PowerShell и выполните:

```powershell
git --version
git lfs version
```

Оба должны показать версии без ошибок.

## После установки Git

1. Настройте Git (первый раз):
   ```bash
   git config --global user.name "Ваше Имя"
   git config --global user.email "ваш@email.com"
   ```

2. Инициализируйте репозиторий:
   ```bash
   cd D:\projects\DK
   git init
   git lfs install
   git lfs track "Template.xml"
   ```

---

## Альтернатива: Без Git LFS

Если вы не хотите устанавливать Git LFS, можно использовать другие методы для работы с большим файлом `Template.xml`. См. `ALTERNATIVE_WITHOUT_LFS.md`.


