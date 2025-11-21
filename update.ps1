# Скрипт для быстрого обновления приложения на Streamlit

param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

# Переходим в директорию проекта
Set-Location $PSScriptRoot

Write-Host "=== Обновление приложения ===" -ForegroundColor Cyan
Write-Host ""

# Проверяем статус
Write-Host "Проверка изменений..." -ForegroundColor Yellow
$status = git status --short
if ($status) {
    Write-Host "Найдены изменения:" -ForegroundColor Green
    $status | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
} else {
    Write-Host "Нет изменений для коммита" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Добавление файлов..." -ForegroundColor Yellow
git add .

Write-Host "Создание коммита..." -ForegroundColor Yellow
git commit -m $Message

if ($LASTEXITCODE -ne 0) {
    Write-Host "Ошибка при создании коммита!" -ForegroundColor Red
    exit 1
}

Write-Host "Загрузка на GitHub..." -ForegroundColor Yellow
git push

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Изменения успешно загружены на GitHub!" -ForegroundColor Green
    Write-Host "Streamlit автоматически обновит приложение через 1-2 минуты." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Проверьте статус на: https://share.streamlit.io/" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "❌ Ошибка при загрузке на GitHub" -ForegroundColor Red
    exit 1
}

