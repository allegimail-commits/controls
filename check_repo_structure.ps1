# Скрипт для проверки структуры репозитория перед загрузкой на GitHub

Write-Host "=== Проверка структуры репозитория ===" -ForegroundColor Cyan
Write-Host ""

# Проверка обязательных файлов
$requiredFiles = @(
    "src\main.py",
    "src\__init__.py",
    "src\gui\__init__.py",
    "src\models\__init__.py",
    "src\parser\__init__.py",
    "src\vector_db\__init__.py",
    "requirements.txt",
    "run.py",
    "Template.xml",
    ".streamlit\config.toml",
    ".gitignore",
    ".gitattributes"
)

Write-Host "Проверка обязательных файлов:" -ForegroundColor Yellow
$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file - ОТСУТСТВУЕТ!" -ForegroundColor Red
        $missingFiles += $file
    }
}

Write-Host ""
Write-Host "Проверка исходного кода:" -ForegroundColor Yellow
$srcFiles = Get-ChildItem -Path "src" -Recurse -File -Filter "*.py" | Where-Object { $_.FullName -notlike "*__pycache__*" }
Write-Host "  Найдено Python файлов: $($srcFiles.Count)" -ForegroundColor Cyan
foreach ($file in $srcFiles) {
    $relativePath = $file.FullName.Replace((Get-Location).Path + "\", "")
    Write-Host "    - $relativePath" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Проверка размера Template.xml:" -ForegroundColor Yellow
if (Test-Path "Template.xml") {
    $size = (Get-Item "Template.xml").Length / 1MB
    Write-Host "  Размер: $([math]::Round($size, 2)) МБ" -ForegroundColor Cyan
    if ($size -gt 25) {
        Write-Host "  ⚠ ВНИМАНИЕ: Файл больше 25 МБ, нужен Git LFS!" -ForegroundColor Red
    } elseif ($size -gt 20) {
        Write-Host "  ⚠ Рекомендуется использовать Git LFS" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Проверка игнорируемых файлов:" -ForegroundColor Yellow
$ignoredDirs = @("chroma_db", "__pycache__", ".cache", "venv")
foreach ($dir in $ignoredDirs) {
    if (Test-Path $dir) {
        Write-Host "  ✓ $dir существует (должен быть в .gitignore)" -ForegroundColor Green
    } else {
        Write-Host "  - $dir не найден" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Проверка Git LFS:" -ForegroundColor Yellow
try {
    $lfsVersion = git lfs version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Git LFS установлен" -ForegroundColor Green
        Write-Host "    $lfsVersion" -ForegroundColor Gray
    } else {
        Write-Host "  ✗ Git LFS не установлен или не настроен" -ForegroundColor Red
        Write-Host "    Установите: winget install GitHub.GitLFS" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ✗ Git LFS не найден" -ForegroundColor Red
    Write-Host "    Установите: winget install GitHub.GitLFS" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Итоги ===" -ForegroundColor Cyan
if ($missingFiles.Count -eq 0) {
    Write-Host "✓ Все обязательные файлы на месте!" -ForegroundColor Green
} else {
    Write-Host "✗ Отсутствуют файлы: $($missingFiles.Count)" -ForegroundColor Red
    foreach ($file in $missingFiles) {
        Write-Host "  - $file" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Следующие шаги:" -ForegroundColor Cyan
Write-Host "1. Убедитесь, что Git LFS установлен и настроен" -ForegroundColor White
Write-Host "2. Выполните: git lfs track 'Template.xml'" -ForegroundColor White
Write-Host "3. Выполните: git add ." -ForegroundColor White
Write-Host "4. Проверьте: git status" -ForegroundColor White
Write-Host "5. Создайте коммит и загрузите на GitHub" -ForegroundColor White


