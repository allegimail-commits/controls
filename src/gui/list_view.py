"""
Компонент для отображения списка контролей в табличном виде.
"""

import streamlit as st
import pandas as pd
from typing import List, Optional
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from ..models.control import Control
from .filters import FilterState


def render_controls_list(all_controls: List[Control], filter_state: FilterState, selected_control_id: Optional[str] = None) -> Optional[str]:
    """
    Отображает список контролей в табличном виде.
    
    Args:
        all_controls: Список всех контролей (для фильтрации)
        filter_state: Объект состояния фильтров
        selected_control_id: ID выбранного контроля
        
    Returns:
        ID выбранного контроля или None
    """
    if not all_controls:
        st.info("Нет контролей для отображения")
        return None
    
    st.header("📋 Список контролей")
    
    # Применяем фильтры
    controls = filter_state.apply_filters(all_controls)
    
    # Кнопка сброса фильтров (перед виджетами, чтобы можно было сбросить их значения)
    col_btn1, col_btn2 = st.columns([10, 1])
    with col_btn2:
        if st.button("🔄 Сбросить фильтры", use_container_width=True, key='reset_aggrid_filters'):
            # Сбрасываем фильтры FilterState
            filter_state.reset_filters()
            # Удаляем ключ быстрого поиска из session_state (будет пересоздан с пустым значением)
            if 'quick_search' in st.session_state:
                del st.session_state.quick_search
            # Увеличиваем счетчик для пересоздания таблицы (это сбросит фильтры AgGrid)
            if 'aggrid_reset_counter' not in st.session_state:
                st.session_state.aggrid_reset_counter = 0
            st.session_state.aggrid_reset_counter += 1
            st.rerun()
    
    # Быстрый поиск
    search_term = st.text_input("🔍 Быстрый поиск по таблице", key="quick_search")
    
    # Подготавливаем данные для таблицы
    table_data = []
    for idx, control in enumerate(controls):
        # Применяем быстрый поиск
        if search_term:
            search_lower = search_term.lower()
            if not any(search_lower in str(val).lower() for val in [
                control.identifier, control.name, control.table_code, 
                control.taxonomy, control.market
            ]):
                continue
        
        # Обрезаем URI для отображения
        uri_display = control.uri[:100] + "..." if len(control.uri) > 100 else control.uri
        
        table_data.append({
            'ID': idx,
            'Идентификатор': control.identifier or '',
            'Наименование': control.name or '',
            'URI': uri_display,
            'Обязательный': '✓' if (control.required or '').lower() == 'да' else '',
            'ДоступноИсправление': '✓' if (control.correction_available or '').lower() == 'да' else '',
            'Утверждение': '✓' if (control.approval or '').lower() == 'да' else '',
            'КодТаблицы': control.table_code or '',
            'Таксономия': control.taxonomy or '',
            'Рынок': control.market or '',
        })
    
    if not table_data:
        st.info("Нет результатов, соответствующих критериям поиска")
        return None
    
    # Создаем DataFrame
    df = pd.DataFrame(table_data)
    
    # Инициализируем счетчик для сброса таблицы
    if 'aggrid_reset_counter' not in st.session_state:
        st.session_state.aggrid_reset_counter = 0
    
    # Настройка AgGrid с встроенными фильтрами в колонках
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        filter=True,
        sortable=True,
        resizable=True,
        editable=False
    )
    
    # Настройка ширины колонок
    gb.configure_column("ID", width=80)
    gb.configure_column("Идентификатор", width=150)
    gb.configure_column("Наименование", width=200)
    gb.configure_column("URI", width=200)
    gb.configure_column("Обязательный", width=100)
    gb.configure_column("ДоступноИсправление", width=150)
    gb.configure_column("Утверждение", width=100)
    gb.configure_column("КодТаблицы", width=150)
    gb.configure_column("Таксономия", width=150)
    gb.configure_column("Рынок", width=150)
    
    # Отключаем пагинацию - показываем все элементы на одной странице
    gb.configure_pagination(enabled=False)
    
    # Настройка выбора строк
    gb.configure_selection('single')
    
    grid_options = gb.build()
    
    # Отображаем таблицу с встроенными фильтрами в колонках
    # Используем счетчик в ключе для пересоздания таблицы при сбросе фильтров
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        theme='streamlit',
        height=800,
        fit_columns_on_grid_load=True,
        key=f'controls_table_{st.session_state.aggrid_reset_counter}'
    )
    
    # Получаем выбранную строку
    selected_rows = grid_response.get('selected_rows', [])
    
    # Информация о количестве отфильтрованных результатов
    if len(controls) != len(all_controls):
        st.info(f"🔍 Показано {len(df)} из {len(all_controls)} контролей (применены фильтры)")
    else:
        st.info(f"📋 Всего контролей: {len(df)}")
    
    # Обработка выбранной строки из AgGrid
    if selected_rows is not None:
        # selected_rows может быть DataFrame или списком словарей
        if isinstance(selected_rows, pd.DataFrame):
            if not selected_rows.empty:
                selected_row = selected_rows.iloc[0].to_dict()
                selected_identifier = selected_row.get('Идентификатор', '')
                for idx, control in enumerate(controls):
                    if control.identifier == selected_identifier:
                        return f"{control.identifier}_{idx}"
        elif isinstance(selected_rows, list):
            if len(selected_rows) > 0:
                selected_row = selected_rows[0]
                if isinstance(selected_row, dict):
                    selected_identifier = selected_row.get('Идентификатор', '')
                else:
                    selected_identifier = getattr(selected_row, 'Идентификатор', '')
                for idx, control in enumerate(controls):
                    if control.identifier == selected_identifier:
                        return f"{control.identifier}_{idx}"
    
    return selected_control_id

