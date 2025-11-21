"""
Главный файл Streamlit приложения информационной системы по дополнительным контролям.
"""

import streamlit as st
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь для импортов
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.parser.xml_parser import load_controls
from src.models.control import Control
from src.gui.filters import FilterState
from src.gui.list_view import render_controls_list
from src.gui.details_view import render_control_details


# Настройка страницы
st.set_page_config(
    page_title="Информационная система по дополнительным контролям",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Скрываем боковую панель полностью
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="stSidebar"][aria-expanded="true"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Путь к XML файлу (фиксированный, настраивается администратором)
XML_FILE_PATH = project_root / "Template.xml"

# Инициализация состояния сессии
if 'controls' not in st.session_state:
    st.session_state.controls = []
if 'selected_control_id' not in st.session_state:
    st.session_state.selected_control_id = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False


def load_controls_from_xml(xml_path: str) -> list[Control]:
    """
    Загружает контроли из XML файла.
    
    Args:
        xml_path: Путь к XML файлу
        
    Returns:
        Список контролей
    """
    try:
        controls = load_controls(xml_path)
        return controls
    except Exception as e:
        st.error(f"Ошибка при загрузке XML: {str(e)}")
        return []


def main():
    """Главная функция приложения."""
    
    # Автоматическая загрузка данных при первом запуске
    if not st.session_state.data_loaded:
        if XML_FILE_PATH.exists():
            with st.spinner("Загрузка данных..."):
                controls = load_controls_from_xml(str(XML_FILE_PATH))
                if controls:
                    st.session_state.controls = controls
                    st.session_state.data_loaded = True
                    st.session_state.selected_control_id = None
                    st.success(f"✅ Загружено {len(controls)} контролей")
                    st.rerun()
                else:
                    st.error("Не удалось загрузить контроли из файла")
                    st.stop()
        else:
            st.error(f"❌ Файл Template.xml не найден по пути: {XML_FILE_PATH}")
            st.info("Обратитесь к администратору для настройки файла макета.")
            st.stop()
    
    controls = st.session_state.controls
    
    # Заголовок
    st.title("📊 Информационная система по дополнительным контролям")
    
    # Инициализируем состояние фильтров
    filter_state = FilterState()
    
    # Добавляем CSS для прокрутки нижней панели
    st.markdown("""
    <style>
        /* Стили для нижней панели с прокруткой - применяем к контейнеру после divider */
        hr + div[data-testid="stVerticalBlock"] {
            max-height: calc(100vh - 450px) !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
        }
        
        /* Альтернативный селектор для нижней панели */
        .stDivider + div {
            max-height: calc(100vh - 450px) !important;
            overflow-y: auto !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Верхняя панель - список контролей
    # Список контролей (фильтры отображаются и применяются внутри)
    selected_id = render_controls_list(controls, filter_state, st.session_state.selected_control_id)
    if selected_id:
        st.session_state.selected_control_id = selected_id
    
    # Разделитель между панелями
    st.divider()
    
    # Нижняя панель - описание контроля
    # Описание контроля (применяем фильтры для консистентности)
    filtered_controls = filter_state.apply_filters(controls)
    render_control_details(filtered_controls, st.session_state.selected_control_id)


if __name__ == "__main__":
    main()

