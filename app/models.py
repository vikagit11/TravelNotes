from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy import DateTime
from datetime import datetime
from .database import Base


class Note(Base):
    """
    Модель заметки в базе данных.Хранит заголовок, описание, статус выполнения.
    Дату создания, дату обновления, приоритет и категорию.
    """
    __tablename__ = "notes"                                                 # имя таблицы в базе

   
    id = Column(Integer, primary_key=True, autoincrement=True)              # ID
    title = Column(String(200), nullable=False, index=True)                 # заголовок заметки
    description = Column(Text)                                              # описание заметки
    is_done = Column(Boolean, default=False)                                # статус выполнения
    
    # временные метки для аудита
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # приоритет задачи
    priority = Column(Integer, default=0)  # 0-низкий, 1-средний, 2-высокий
    
    # категорию/теги для группировки заметок
    category = Column(String(50))
    
    #метод для удобного отображения
    def __repr__(self):
        return f"<Note(id={self.id}, title='{self.title}', is_done={self.is_done})>"

