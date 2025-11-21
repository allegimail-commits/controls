"""
Компонент для отображения списка контролей в табличном виде.
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from typing import List, Optional
from openpyxl.utils import get_column_letter
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
    
    # Быстрый поиск и кнопки в одной строке
    # Добавляем CSS для выравнивания высоты кнопок с высотой строки поиска
    st.markdown("""
        <style>
        /* Выравнивание всех элементов в строке поиска по верхнему краю */
        div[data-testid="column"] {
            vertical-align: top !important;
        }
        /* Выравнивание внутренних контейнеров колонок */
        div[data-testid="column"] > div[style*="flex"] {
            align-items: flex-start !important;
        }
        /* Фиксированная высота и выравнивание всех кнопок */
        .stButton {
            margin-top: 0 !important;
        }
        .stButton > button {
            height: 38px !important;
            min-height: 38px !important;
            max-height: 38px !important;
            line-height: 1.1 !important;
            white-space: normal !important;
            padding: 0.25rem 0.5rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            vertical-align: top !important;
            margin-top: 0 !important;
        }
        /* Стили для кнопки загрузки (download_button) */
        .stDownloadButton {
            margin-top: 0 !important;
        }
        .stDownloadButton > button {
            height: 38px !important;
            min-height: 38px !important;
            max-height: 38px !important;
            line-height: 1.1 !important;
            white-space: normal !important;
            padding: 0.25rem 0.5rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            vertical-align: top !important;
            margin-top: 0 !important;
        }
        /* Универсальные стили для всех кнопок в колонках */
        div[data-testid="column"] .stButton > button,
        div[data-testid="column"] .stDownloadButton > button,
        div[data-testid="column"] button[data-testid="baseButton-secondary"],
        div[data-testid="column"] button[data-testid="baseButton-primary"] {
            height: 38px !important;
            min-height: 38px !important;
            max-height: 38px !important;
            line-height: 1.1 !important;
            padding: 0.25rem 0.5rem !important;
        }
        /* Выравнивание текстового поля */
        .stTextInput {
            margin-top: 0 !important;
        }
        .stTextInput > div > div > input {
            height: 38px !important;
            box-sizing: border-box !important;
            margin-top: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Создаем интерфейс поиска и кнопок
    col_search, col_find, col_btn, col_export = st.columns([7, 1, 1, 1])
    with col_search:
        search_term = st.text_input("", placeholder="Быстрый поиск по таблице", key="quick_search", label_visibility="collapsed")
    with col_find:
        if st.button("Найти", use_container_width=True, key='find_button'):
            st.rerun()
    with col_btn:
        if st.button("Сбросить настройки", use_container_width=True, key='reset_aggrid_filters'):
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
    with col_export:
        # Placeholder для кнопки экспорта (будет обновлен после подготовки данных)
        export_button_placeholder = st.empty()
    
    # Подготавливаем данные для таблицы и экспорта
    table_data = []
    export_data = []
    
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
        
        # Данные для таблицы (с обрезанным URI и символами для чекбоксов)
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
        
        # Данные для экспорта (с полными URI и исходными значениями)
        export_data.append({
            'ID': idx,
            'Идентификатор': control.identifier or '',
            'Наименование': control.name or '',
            'URI': control.uri or '',
            'Обязательный': control.required or '',
            'ДоступноИсправление': control.correction_available or '',
            'Утверждение': control.approval or '',
            'КодТаблицы': control.table_code or '',
            'Таксономия': control.taxonomy or '',
            'Рынок': control.market or '',
        })
    
    # Подготавливаем Excel файл для экспорта
    excel_bytes = None
    if export_data:
        df_export = pd.DataFrame(export_data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Контроли')
            # Настраиваем ширину колонок
            worksheet = writer.sheets['Контроли']
            for col_idx, col in enumerate(df_export.columns, 1):
                max_length = max(
                    df_export[col].astype(str).map(len).max(),
                    len(col)
                )
                # Ограничиваем максимальную ширину колонки
                adjusted_width = min(max_length + 2, 50)
                # Получаем букву колонки (A, B, C, ..., Z, AA, AB, ...)
                col_letter = get_column_letter(col_idx)
                worksheet.column_dimensions[col_letter].width = adjusted_width
        
        excel_bytes = output.getvalue()
    
    # Обновляем кнопку экспорта в Excel
    if excel_bytes:
        with export_button_placeholder.container():
            st.download_button(
                label="Выгрузить в Excel",
                data=excel_bytes,
                file_name="контроли.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key='export_excel_button'
            )
    
    if not table_data:
        st.info("Нет результатов, соответствующих критериям поиска")
        return None
    
    # Создаем DataFrame для отображения
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

