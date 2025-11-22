from pydantic import BaseModel
# TODO: Добавить импорт Field для валидации
from pydantic import Field, validator
# TODO: Добавить импорт datetime для временных меток
from datetime import datetime
from typing import Optional


# Базовая схема: общие поля для всех заметок
# TODO: Добавить docstring для классов Pydantic
class NoteBase(BaseModel):
    """
    Базовая схема: общие поля для всех заметок
    """
    # TODO: Добавить валидацию длины title с помощью Field
    title: str = Field(..., min_length=1, max_length=200, description="Название заметки")
    # БАГ: title может быть пустой строкой - нет минимальной длины
    
    
    # TODO: Добавить валидацию длины description
    description: Optional[str] = Field(None, max_length=1000, description="Описание заметки")
    


# создание новой заметки (наследует NoteBase)
# УЛУЧШЕНИЕ: Можно добавить дополнительные поля только для создания
# Например: tags, priority, deadline
class NoteCreate(NoteBase):
    """
    Схема для создания новой заметки
    """
    pass
    # TODO: Добавить валидацию данных
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Название заметки не может быть пустым')
        return v.strip()


# TODO: Добавить схему для обновления заметки (NoteUpdate)
class NoteUpdate(BaseModel):
    """
    Схема для обновления заметки
    """
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
# ПРИЧИНА: Сейчас нет возможности частичного обновления через API


#  вывод данных из базы 
# TODO: Переименовать в NoteResponse для ясности назначения
class NoteResponse(NoteBase):
    """
    Вывод данных из базы 
    """
    id: int
    is_done: bool
    # TODO: Добавить временные метки при их внедрении в модель
    created_at: datetime
    updated_at: datetime

    # TODO: УСТАРЕЛО! orm_mode переименован в from_attributes в Pydantic v2
    # ИСПРАВИТЬ: Использовать from_attributes=True вместо orm_mode
    class Config:
    #     orm_mode = True
        # БАГ: В Pydantic v2 должно быть:
        from_attributes = True
        
        # УЛУЧШЕНИЕ: Добавить дополнительные настройки
    #json_encoders = {datetime: lambda v: v.isoformat()}
    #validate_assignment = True


# TODO: Добавить схему для фильтрации/пагинации
class NoteFilter(BaseModel):
    """
    Схема для фильтрации/пагинации
    
    """
    skip: int = 0
    limit: int = 100
    is_done: Optional[bool] = None
    search: Optional[str] = None

