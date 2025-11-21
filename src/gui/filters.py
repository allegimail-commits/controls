"""
Компоненты фильтров для графического интерфейса.
"""

import streamlit as st
from typing import Dict, Optional, Callable
from ..models.control import Control


class FilterState:
    """Класс для управления состоянием фильтров."""
    
    def __init__(self):
        """Инициализирует состояние фильтров."""
        if 'filters' not in st.session_state:
            st.session_state.filters = {
                'identifier': '',
                'name': '',
                'uri': '',
                'required': None,
                'correction_available': None,
                'approval': None,
                'table_code': '',
                'taxonomy': '',
                'market': '',
            }
    
    def get_filters(self) -> Dict:
        """Возвращает текущие значения фильтров."""
        return st.session_state.filters
    
    def reset_filters(self):
        """Сбрасывает все фильтры."""
        st.session_state.filters = {
            'identifier': '',
            'name': '',
            'uri': '',
            'required': None,
            'correction_available': None,
            'approval': None,
            'table_code': '',
            'taxonomy': '',
            'market': '',
        }
    
    def apply_filters(self, controls: list[Control]) -> list[Control]:
        """
        Применяет фильтры к списку контролей.
        
        Args:
            controls: Список контролей для фильтрации
            
        Returns:
            Отфильтрованный список контролей
        """
        filters = self.get_filters()
        filtered = controls
        
        # Фильтр по идентификатору
        if filters['identifier']:
            search_term = filters['identifier'].lower()
            filtered = [c for c in filtered if search_term in (c.identifier or '').lower()]
        
        # Фильтр по наименованию
        if filters['name']:
            search_term = filters['name'].lower()
            filtered = [c for c in filtered if search_term in (c.name or '').lower()]
        
        # Фильтр по URI
        if filters['uri']:
            search_term = filters['uri'].lower()
            filtered = [c for c in filtered if search_term in (c.uri or '').lower()]
        
        # Фильтр по обязательности
        if filters['required'] is not None:
            required_value = 'да' if filters['required'] else 'нет'
            filtered = [c for c in filtered if (c.required or '').lower() == required_value.lower()]
        
        # Фильтр по доступности исправления
        if filters['correction_available'] is not None:
            correction_value = 'да' if filters['correction_available'] else 'нет'
            filtered = [c for c in filtered if (c.correction_available or '').lower() == correction_value.lower()]
        
        # Фильтр по утверждению
        if filters['approval'] is not None:
            approval_value = 'да' if filters['approval'] else 'нет'
            filtered = [c for c in filtered if (c.approval or '').lower() == approval_value.lower()]
        
        # Фильтр по коду таблицы
        if filters['table_code']:
            search_term = filters['table_code'].lower()
            filtered = [c for c in filtered if search_term in (c.table_code or '').lower()]
        
        # Фильтр по таксономии
        if filters['taxonomy']:
            search_term = filters['taxonomy'].lower()
            filtered = [c for c in filtered if search_term in (c.taxonomy or '').lower()]
        
        # Фильтр по рынку
        if filters['market']:
            search_term = filters['market'].lower()
            filtered = [c for c in filtered if search_term in (c.market or '').lower()]
        
        return filtered


def render_table_headers_with_filters(filter_state: FilterState, controls: list[Control]) -> None:
    """
    Отображает заголовки таблицы со встроенными фильтрами.
    
    Args:
        filter_state: Объект состояния фильтров
        controls: Список всех контролей (для получения уникальных значений)
    """
    filters = filter_state.get_filters()
    
    # Получаем уникальные значения для выпадающих списков
    unique_table_codes = sorted(set([c.table_code for c in controls if c.table_code]))
    unique_taxonomies = sorted(set([c.taxonomy for c in controls if c.taxonomy]))
    unique_markets = sorted(set([c.market for c in controls if c.market]))
    
    # Создаем колонки для заголовков с фильтрами (соответствуют колонкам таблицы)
    # Веса подобраны для выравнивания с колонками таблицы
    col_id, col_identifier, col_name, col_uri, col_req, col_corr, col_appr, col_table, col_tax, col_market = st.columns(
        [0.8, 1.5, 2, 2, 1, 1.5, 1, 1.5, 1.5, 1.5]
    )
    
    # ID (без фильтра, только заголовок)
    with col_id:
        st.markdown("**ID**")
    
    # Идентификатор
    with col_identifier:
        st.markdown("**Идентификатор**")
        filters['identifier'] = st.text_input(
            "Идентификатор",
            value=filters['identifier'],
            key='filter_identifier',
            label_visibility="collapsed"
        )
    
    # Наименование
    with col_name:
        st.markdown("**Наименование**")
        filters['name'] = st.text_input(
            "Наименование",
            value=filters['name'],
            key='filter_name',
            label_visibility="collapsed"
        )
    
    # URI
    with col_uri:
        st.markdown("**URI**")
        filters['uri'] = st.text_input(
            "URI",
            value=filters['uri'],
            key='filter_uri',
            label_visibility="collapsed"
        )
    
    # Обязательный
    with col_req:
        st.markdown("**Обязательный**")
        required_options = ["Все", "Да", "Нет"]
        required_index = 0 if filters['required'] is None else (1 if filters['required'] else 2)
        required_choice = st.selectbox(
            "Обязательный",
            options=required_options,
            index=required_index,
            key='filter_required',
            label_visibility="collapsed"
        )
        filters['required'] = None if required_choice == "Все" else (required_choice == "Да")
    
    # ДоступноИсправление
    with col_corr:
        st.markdown("**ДоступноИсправление**")
        correction_options = ["Все", "Да", "Нет"]
        correction_index = 0 if filters['correction_available'] is None else (1 if filters['correction_available'] else 2)
        correction_choice = st.selectbox(
            "ДоступноИсправление",
            options=correction_options,
            index=correction_index,
            key='filter_correction',
            label_visibility="collapsed"
        )
        filters['correction_available'] = None if correction_choice == "Все" else (correction_choice == "Да")
    
    # Утверждение
    with col_appr:
        st.markdown("**Утверждение**")
        approval_options = ["Все", "Да", "Нет"]
        approval_index = 0 if filters['approval'] is None else (1 if filters['approval'] else 2)
        approval_choice = st.selectbox(
            "Утверждение",
            options=approval_options,
            index=approval_index,
            key='filter_approval',
            label_visibility="collapsed"
        )
        filters['approval'] = None if approval_choice == "Все" else (approval_choice == "Да")
    
    # КодТаблицы
    with col_table:
        st.markdown("**КодТаблицы**")
        table_code_index = 0 if not filters['table_code'] else (unique_table_codes.index(filters['table_code']) + 1 if filters['table_code'] in unique_table_codes else 0)
        table_code_choice = st.selectbox(
            "КодТаблицы",
            options=["Все"] + unique_table_codes,
            index=table_code_index,
            key='filter_table_code',
            label_visibility="collapsed"
        )
        filters['table_code'] = '' if table_code_choice == "Все" else table_code_choice
    
    # Таксономия
    with col_tax:
        st.markdown("**Таксономия**")
        taxonomy_index = 0 if not filters['taxonomy'] else (unique_taxonomies.index(filters['taxonomy']) + 1 if filters['taxonomy'] in unique_taxonomies else 0)
        taxonomy_choice = st.selectbox(
            "Таксономия",
            options=["Все"] + unique_taxonomies,
            index=taxonomy_index,
            key='filter_taxonomy',
            label_visibility="collapsed"
        )
        filters['taxonomy'] = '' if taxonomy_choice == "Все" else taxonomy_choice
    
    # Рынок
    with col_market:
        st.markdown("**Рынок**")
        market_index = 0 if not filters['market'] else (unique_markets.index(filters['market']) + 1 if filters['market'] in unique_markets else 0)
        market_choice = st.selectbox(
            "Рынок",
            options=["Все"] + unique_markets,
            index=market_index,
            key='filter_market',
            label_visibility="collapsed"
        )
        filters['market'] = '' if market_choice == "Все" else market_choice
    
    # Кнопки управления фильтрами (в отдельной строке)
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([10, 1, 1])
    with col_btn2:
        if st.button("🔄 Сбросить", use_container_width=True, key='filter_reset'):
            filter_state.reset_filters()
            st.rerun()
    with col_btn3:
        if st.button("✅ Применить", use_container_width=True, type="primary", key='filter_apply'):
            st.rerun()
    
    # Обновляем состояние
    st.session_state.filters = filters


def render_filters_panel(filter_state: FilterState, controls: list[Control]) -> None:
    """
    Отображает панель фильтров в горизонтальной компоновке над таблицей.
    Устаревшая функция, используется render_table_headers_with_filters.
    
    Args:
        filter_state: Объект состояния фильтров
        controls: Список всех контролей (для получения уникальных значений)
    """
    render_table_headers_with_filters(filter_state, controls)

