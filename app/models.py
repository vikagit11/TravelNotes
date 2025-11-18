from sqlalchemy import Column, Integer, String, Boolean
# TODO: Добавить импорт DateTime для отслеживания времени создания/обновления заметок
# from sqlalchemy import DateTime
# from datetime import datetime
from .database import Base

# TODO: Добавить docstring для класса, описывающий назначение модели
# TODO: Добавить метод __repr__ для удобного отображения объектов
class Note(Base):
    __tablename__ = "notes"  # имя таблицы в базе

    # TODO: Добавить autoincrement=True явно для ясности
    id = Column(Integer, primary_key=True)             # ID
    
    # TODO: Добавить ограничения на длину строки: String(200)
    # TODO: Добавить nullable=False для обязательных полей
    # БАГ: index=True создает индекс, но нет проверки на пустое значение
    title = Column(String, index=True)                 # заголовок заметки
    
    # TODO: Добавить ограничения на длину: String(1000)
    # УЛУЧШЕНИЕ: Использовать Text для длинных описаний вместо String
    description = Column(String)                      # описание заметки
    
    is_done = Column(Boolean, default=False)          # статус выполнения
    
    # УЛУЧШЕНИЕ: Добавить временные метки для аудита
    # created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # УЛУЧШЕНИЕ: Добавить приоритет задачи
    # priority = Column(Integer, default=0)  # 0-низкий, 1-средний, 2-высокий
    
    # УЛУЧШЕНИЕ: Добавить категорию/теги для группировки заметок
    # category = Column(String(50))
    
    # TODO: Добавить метод для удобного отображения
    # def __repr__(self):
    #     return f"<Note(id={self.id}, title='{self.title}', is_done={self.is_done})>"

