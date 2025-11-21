#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для быстрого обновления приложения на Streamlit
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# Цвета для вывода (ANSI коды)
class Colors:
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    RESET = '\033[0m'

def print_colored(message, color=Colors.RESET):
    """Выводит цветное сообщение"""
    print(f"{color}{message}{Colors.RESET}")

def run_command(command, check=True, capture_output=False):
    """
    Выполняет команду и возвращает результат
    
    Args:
        command: Список аргументов команды
        check: Если True, вызывает исключение при ошибке
        capture_output: Если True, возвращает вывод команды
    
    Returns:
        CompletedProcess объект
    """
    try:
        if capture_output:
            result = subprocess.run(
                command,
                check=check,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return result
        else:
            result = subprocess.run(
                command,
                check=check,
                text=True,
                encoding='utf-8'
            )
            return result
    except subprocess.CalledProcessError as e:
        return None

def main():
    """Основная функция скрипта"""
    # Настройка парсера аргументов
    parser = argparse.ArgumentParser(
        description='Скрипт для быстрого обновления приложения на Streamlit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Примеры использования:\n  python update.py "Исправление бага"\n  python update.py -m "Добавлена новая функция"'
    )
    parser.add_argument(
        'message',
        nargs='?',
        help='Сообщение коммита (позиционный аргумент)'
    )
    parser.add_argument(
        '-m', '--message',
        dest='message_flag',
        help='Сообщение коммита (флаг)'
    )
    
    args = parser.parse_args()
    
    # Определяем сообщение коммита (приоритет у флага -m/--message)
    commit_message = args.message_flag or args.message
    if not commit_message:
        parser.print_help()
        print_colored("\nОшибка: необходимо указать сообщение коммита", Colors.RED)
        print_colored("Использование: python update.py \"Сообщение коммита\"", Colors.YELLOW)
        sys.exit(1)
    
    # Переходим в директорию скрипта
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print_colored('=== Обновление приложения ===', Colors.CYAN)
    print()
    
    # Проверяем статус
    print_colored('Проверка изменений...', Colors.YELLOW)
    status_result = run_command(['git', 'status', '--short'], check=False, capture_output=True)
    
    if status_result and status_result.stdout.strip():
        print_colored('Найдены изменения:', Colors.GREEN)
        for line in status_result.stdout.strip().split('\n'):
            if line.strip():
                print_colored(f"  {line}", Colors.GRAY)
    else:
        print_colored('Нет изменений для коммита', Colors.YELLOW)
        sys.exit(0)
    
    print()
    print_colored('Добавление файлов...', Colors.YELLOW)
    add_result = run_command(['git', 'add', '.'], check=False)
    
    if add_result is None:
        print_colored('Ошибка при добавлении файлов!', Colors.RED)
        sys.exit(1)
    
    print_colored('Создание коммита...', Colors.YELLOW)
    commit_result = run_command(['git', 'commit', '-m', commit_message], check=False)
    
    if commit_result is None:
        print_colored('Ошибка при создании коммита!', Colors.RED)
        sys.exit(1)
    
    # Сначала получаем изменения с удаленного репозитория
    print_colored('Получение изменений с GitHub...', Colors.YELLOW)
    pull_result = run_command(['git', 'pull', '--rebase'], check=False)
    
    if pull_result is None:
        print_colored('Предупреждение: возникли проблемы при получении изменений', Colors.YELLOW)
        print_colored('Попытка продолжить загрузку...', Colors.YELLOW)
    
    print_colored('Загрузка на GitHub...', Colors.YELLOW)
    push_result = run_command(['git', 'push'], check=False)
    
    if push_result is not None:
        print()
        print_colored('Изменения успешно загружены на GitHub!', Colors.GREEN)
        print_colored('Streamlit автоматически обновит приложение через 1-2 минуты.', Colors.CYAN)
        print()
        print_colored('Проверьте статус на: https://share.streamlit.io/', Colors.GRAY)
    else:
        print()
        print_colored('Ошибка при загрузке на GitHub', Colors.RED)
        print_colored('Возможно, нужно разрешить конфликты вручную.', Colors.YELLOW)
        sys.exit(1)

if __name__ == '__main__':
    main()

