from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Note(Base):
    __tablename__ = "notes"  # имя таблицы в базе

    id = Column(Integer, primary_key=True)             # ID
    title = Column(String, index=True)                 # заголовок заметки
    description = Column(String)                      # описание заметки
    is_done = Column(Boolean, default=False)          # статус выполнения
