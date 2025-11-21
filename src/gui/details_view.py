"""
Компонент для отображения детального описания контроля.
"""

import streamlit as st
from typing import List, Optional
from ..models.control import Control


def render_control_details(controls: List[Control], selected_control_id: Optional[str] = None) -> None:
    """
    Отображает детальное описание выбранного контроля.
    
    Args:
        controls: Список всех контролей
        selected_control_id: ID выбранного контроля (формат: "identifier_index")
    """
    st.header("📄 Описание контроля и основные характеристики")
    
    if not selected_control_id or not controls:
        st.info("Выберите контроль из списка для просмотра деталей")
        return
    
    # Парсим ID выбранного контроля
    try:
        parts = selected_control_id.rsplit('_', 1)
        if len(parts) == 2:
            index = int(parts[1])
            if 0 <= index < len(controls):
                control = controls[index]
            else:
                st.error("Неверный индекс контроля")
                return
        else:
            # Пытаемся найти по идентификатору
            control = next((c for c in controls if c.identifier == selected_control_id), None)
            if not control:
                st.error("Контроль не найден")
                return
    except (ValueError, IndexError):
        st.error("Неверный формат ID контроля")
        return
    
    # Находим индекс текущего контроля
    current_index = next((i for i, c in enumerate(controls) if c.identifier == control.identifier), 0)
    
    # Навигация между контролями
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("◀️ Предыдущий", disabled=current_index == 0):
            if current_index > 0:
                prev_control = controls[current_index - 1]
                st.session_state.selected_control_id = f"{prev_control.identifier}_{current_index - 1}"
                st.rerun()
    
    with col2:
        st.write(f"**Контроль {current_index + 1} из {len(controls)}**")
    
    with col3:
        if st.button("Следующий ▶️", disabled=current_index >= len(controls) - 1):
            if current_index < len(controls) - 1:
                next_control = controls[current_index + 1]
                st.session_state.selected_control_id = f"{next_control.identifier}_{current_index + 1}"
                st.rerun()
    
    st.divider()
    
    # Основная информация
    st.subheader("Основная информация")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Идентификатор", value=control.identifier or '', disabled=True, key='detail_identifier')
        st.text_input("Наименование", value=control.name or '', disabled=True, key='detail_name')
        st.text_input("КодТаблицы", value=control.table_code or '', disabled=True, key='detail_table_code')
        st.text_input("Таксономия", value=control.taxonomy or '', disabled=True, key='detail_taxonomy')
        st.text_input("Рынок", value=control.market or '', disabled=True, key='detail_market')
    
    with col2:
        st.text_input("Обязательный", value=control.required or '', disabled=True, key='detail_required')
        st.text_input("ДоступноИсправление", value=control.correction_available or '', disabled=True, key='detail_correction')
        st.text_input("Утверждение", value=control.approval or '', disabled=True, key='detail_approval')
        st.text_input("КодУтвержденияЦБ", value=control.cbr_approval_code or '', disabled=True, key='detail_cbr_approval')
        st.text_input("НаОснованииТребованияЦБ", value=control.based_on_cbr_requirement or '', disabled=True, key='detail_cbr_req')
    
    # URI
    st.subheader("URI")
    uri_list = control.get_uri_list()
    if uri_list:
        for idx, uri in enumerate(uri_list):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(uri)
            with col2:
                # Используем индекс для уникальности ключа
                if st.button("📋 Копировать", key=f"copy_uri_{current_index}_{idx}"):
                    st.write("Скопировано в буфер обмена")
    else:
        st.text(control.uri or '')
    
    # Сверочный URI
    if control.verification_uri:
        st.subheader("Сверочный URI")
        st.text(control.verification_uri)
    
    # Описание
    if control.description:
        st.subheader("Описание")
        st.text_area("", value=control.description, disabled=True, height=100, key='detail_description')
    
    # Описание проверки по данным ЦБ
    if control.cbr_check_description:
        st.subheader("Описание проверки по данным ЦБ")
        st.text_area("", value=control.cbr_check_description, disabled=True, height=100, key='detail_cbr_check')
    
    # Комментарий
    if control.comment:
        st.subheader("Комментарий")
        st.text_area("", value=control.comment, disabled=True, height=100, key='detail_comment')
    
    # Алгоритм (скрыто для будущего использования)
    # if control.algorithm:
    #     st.subheader("Алгоритм")
    #     # Используем code блок для подсветки синтаксиса (1С язык)
    #     st.code(control.algorithm, language=None)  # Streamlit не поддерживает 1С напрямую, но покажет как код
    
    # Кнопка печати (через браузер)
    st.divider()
    if st.button("🖨️ Печать"):
        st.info("Используйте функцию печати браузера (Ctrl+P)")

