"""
TravelNotes Application Package

Приложение для управления заметками о путешествиях.

TODO: Добавить экспорт основных компонентов для удобного импорта
Пример:
    from app import models, schemas, database
    from app.main import app

"""

version= "1.0.0"

from .models import Note
from .schemas import NoteCreate, NoteUpdate, NoteResponse
#from .database import get_db, Base, engine
