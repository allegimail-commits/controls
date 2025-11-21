"""
Модель данных для контроля дополнительных проверок.
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Control:
    """
    Модель данных контроля дополнительной проверки.
    
    Атрибуты:
        uri: URI (ссылки на XSD-схемы, разделенные точкой с запятой)
        identifier: Идентификатор контроля
        name: Наименование контроля
        algorithm: Алгоритм (код на языке 1С)
        verification_uri: Сверочный URI
        correction_available: Доступность исправления (да/нет)
        description: Описание контроля
        required: Обязательный (да/нет)
        approval: Утверждение (да/нет)
        table_code: Код таблицы
        based_on_cbr_requirement: На основании требования ЦБ
        cbr_check_description: Описание проверки по данным ЦБ
        comment: Комментарий
        cbr_approval_code: Код утверждения ЦБ
        taxonomy: Таксономия
        market: Рынок
    """
    uri: str = ""
    identifier: str = ""
    name: str = ""
    algorithm: str = ""
    verification_uri: str = ""
    correction_available: str = ""
    description: str = ""
    required: str = ""
    approval: str = ""
    table_code: str = ""
    based_on_cbr_requirement: str = ""
    cbr_check_description: str = ""
    comment: str = ""
    cbr_approval_code: str = ""
    taxonomy: str = ""
    market: str = ""
    
    def get_uri_list(self) -> List[str]:
        """Возвращает список URI из строки с разделителями."""
        if not self.uri:
            return []
        return [u.strip() for u in self.uri.split(';') if u.strip()]
    
    def to_dict(self) -> dict:
        """Преобразует контроль в словарь."""
        return {
            'uri': self.uri,
            'identifier': self.identifier,
            'name': self.name,
            'algorithm': self.algorithm,
            'verification_uri': self.verification_uri,
            'correction_available': self.correction_available,
            'description': self.description,
            'required': self.required,
            'approval': self.approval,
            'table_code': self.table_code,
            'based_on_cbr_requirement': self.based_on_cbr_requirement,
            'cbr_check_description': self.cbr_check_description,
            'comment': self.comment,
            'cbr_approval_code': self.cbr_approval_code,
            'taxonomy': self.taxonomy,
            'market': self.market,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Control':
        """Создает контроль из словаря."""
        return cls(**data)
    
    def get_text_for_embedding(self) -> str:
        """
        Возвращает объединенный текст для создания эмбеддинга.
        Включает основные текстовые поля контроля.
        """
        parts = []
        if self.identifier:
            parts.append(f"Идентификатор: {self.identifier}")
        if self.name:
            parts.append(f"Наименование: {self.name}")
        if self.description:
            parts.append(f"Описание: {self.description}")
        if self.algorithm:
            parts.append(f"Алгоритм: {self.algorithm}")
        if self.cbr_check_description:
            parts.append(f"Описание проверки ЦБ: {self.cbr_check_description}")
        if self.comment:
            parts.append(f"Комментарий: {self.comment}")
        return "\n".join(parts)

