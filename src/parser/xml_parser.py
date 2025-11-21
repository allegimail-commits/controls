"""
Парсер XML-макета Template.xml для извлечения данных о контролях.
"""

import xml.etree.ElementTree as ET
from typing import List, Optional
from pathlib import Path

from ..models.control import Control


def extract_text_from_cell(cell_element) -> str:
    """
    Извлекает текст из ячейки XML.
    
    Args:
        cell_element: Элемент ячейки XML
        
    Returns:
        Текст из ячейки или пустая строка
    """
    if cell_element is None:
        return ""
    
    # Ищем элемент item (пробуем разные namespace)
    item = cell_element.find('.//{http://v8.1c.ru/8.1/data/core}item')
    if item is None:
        item = cell_element.find('.//{http://v8.1c.ru/8.2/data/core}item')
    if item is None:
        item = cell_element.find('.//item')
    
    if item is not None:
        content = item.find('{http://v8.1c.ru/8.1/data/core}content')
        if content is None:
            content = item.find('{http://v8.1c.ru/8.2/data/core}content')
        if content is None:
            content = item.find('content')
        if content is not None and content.text:
            return content.text.strip()
    
    return ""


def parse_template_xml(xml_path: str) -> List[Control]:
    """
    Парсит XML-макет и извлекает данные о контролях.
    
    Args:
        xml_path: Путь к файлу Template.xml
        
    Returns:
        Список объектов Control
        
    Raises:
        FileNotFoundError: Если файл не найден
        ET.ParseError: Если XML невалиден
    """
    xml_path = Path(xml_path)
    if not xml_path.exists():
        raise FileNotFoundError(f"Файл не найден: {xml_path}")
    
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Определяем namespace
    # Пробуем разные версии namespace
    namespaces = {
        'ss': 'http://v8.1c.ru/8.2/data/spreadsheet',
        'ss8': 'http://v8.1c.ru/8.1/data/spreadsheet',
        'core': 'http://v8.1c.ru/8.1/data/core',
        'core8': 'http://v8.1c.ru/8.2/data/core',
    }
    
    # Находим все строки (пробуем с namespace)
    rows = root.findall('.//{http://v8.1c.ru/8.2/data/spreadsheet}rowsItem')
    if not rows:
        # Пробуем без namespace
        rows = root.findall('.//rowsItem')
    if not rows:
        return []
    
    # Первая строка содержит заголовки
    if len(rows) == 0:
        raise ValueError("Не найдено строк в XML")
    
    header_row = rows[0]
    
    # Извлекаем заголовки (только прямые дочерние элементы c в row)
    header_row_element = header_row.find('{http://v8.1c.ru/8.2/data/spreadsheet}row')
    if header_row_element is None:
        header_row_element = header_row.find('row')
    if header_row_element is None:
        raise ValueError("Не найдена структура row в строке заголовков")
    
    header_cells = header_row_element.findall('{http://v8.1c.ru/8.2/data/spreadsheet}c')
    if not header_cells:
        header_cells = header_row_element.findall('c')
    headers = []
    for cell in header_cells:
        text = extract_text_from_cell(cell)
        headers.append(text)
    
    # Создаем маппинг индекса колонки к имени заголовка
    column_mapping = {}
    for idx, header in enumerate(headers):
        if header:
            column_mapping[idx] = header
    
    # Парсим данные (начиная со второй строки, первая - заголовки)
    controls = []
    for row_idx, row in enumerate(rows):
        # Пропускаем первую строку (заголовки)
        if row_idx == 0:
            continue
        
        # Извлекаем ячейки строки (только прямые дочерние элементы c в row)
        row_element = row.find('{http://v8.1c.ru/8.2/data/spreadsheet}row')
        if row_element is None:
            row_element = row.find('row')
        if row_element is None:
            continue
        
        cells = row_element.findall('{http://v8.1c.ru/8.2/data/spreadsheet}c')
        if not cells:
            cells = row_element.findall('c')
        if not cells:
            continue
        
        # Создаем словарь для текущего контроля
        control_data = {}
        
        # Извлекаем данные из ячеек
        for idx, cell in enumerate(cells):
            if idx in column_mapping:
                header_name = column_mapping[idx]
                text = extract_text_from_cell(cell)
                
                # Маппинг заголовков на поля модели
                if header_name == 'Uri':
                    control_data['uri'] = text
                elif header_name == 'Идентификатор':
                    control_data['identifier'] = text
                elif header_name == 'Наименование':
                    control_data['name'] = text
                elif header_name == 'Алгоритм':
                    control_data['algorithm'] = text
                elif header_name == 'Сверочный Uri':
                    control_data['verification_uri'] = text
                elif header_name == 'ДоступноИсправление':
                    control_data['correction_available'] = text
                elif header_name == 'Описание':
                    control_data['description'] = text
                elif header_name == 'Обязательный':
                    control_data['required'] = text
                elif header_name == 'Утверждение':
                    control_data['approval'] = text
                elif header_name == 'КодТаблицы':
                    control_data['table_code'] = text
                elif header_name == 'НаОснованииТребованияЦБ':
                    control_data['based_on_cbr_requirement'] = text
                elif header_name == 'ОписаниеПроверкиПоДаннымЦБ':
                    control_data['cbr_check_description'] = text
                elif header_name == 'Комменатрий':  # Опечатка в оригинале
                    control_data['comment'] = text
                elif header_name == 'КодУтвержденияЦБ':
                    control_data['cbr_approval_code'] = text
                elif header_name == 'Таксомномия':
                    control_data['taxonomy'] = text
                elif header_name == 'Рынок':
                    control_data['market'] = text
        
        # Создаем объект Control только если есть хотя бы идентификатор или наименование
        if control_data.get('identifier') or control_data.get('name'):
            control = Control(**control_data)
            controls.append(control)
    
    return controls


def load_controls(xml_path: str) -> List[Control]:
    """
    Загружает контроли из XML-файла.
    
    Args:
        xml_path: Путь к файлу Template.xml
        
    Returns:
        Список объектов Control
    """
    return parse_template_xml(xml_path)

