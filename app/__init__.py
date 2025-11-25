"""
TravelNotes Application Package

Приложение для управления заметками о путешествиях.

"""
version= "1.0.0"

from app import models, schemas, database
from app.main import app
from .schemas import NoteCreate, NoteUpdate, NoteResponse
