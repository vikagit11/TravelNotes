from pydantic import BaseModel
from pydantic import Field, validator
from datetime import datetime
from typing import Optional


# Базовая схема: общие поля для всех заметок
class NoteBase(BaseModel):
    """
    Базовая схема: общие поля для всех заметок
    """
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
    # валидацию данных
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Название заметки не может быть пустым')
        return v.strip()


class NoteUpdate(BaseModel):
    """
    Схема для обновления заметки
    """
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
# ПРИЧИНА: Сейчас нет возможности частичного обновления через API


#  вывод данных из базы 
class NoteResponse(NoteBase):
    """
    Вывод данных из базы 
    """
    id: int
    is_done: bool
    created_at: datetime
    updated_at: datetime

      
    class Config:
        from_attributes = True
        
        # УЛУЧШЕНИЕ: Добавить дополнительные настройки
    #json_encoders = {datetime: lambda v: v.isoformat()}
    #validate_assignment = True


class NoteFilter(BaseModel):
    """
    Схема для фильтрации/пагинации
    
    """
    skip: int = 0
    limit: int = 100
    is_done: Optional[bool] = None
    search: Optional[str] = None

