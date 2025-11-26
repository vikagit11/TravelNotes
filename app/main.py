from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, database, version
from .database import Base, engine, get_db
from fastapi.responses import JSONResponse
from app.services.note_service import get_root_info, get_notes, create_note_service, search_notes_service, update_note_service, delete_note_service
from app.config import DEBUG
import logging

logger = logging.getLogger(__name__)                        #система логирования


# Создаём таблицы, если их ещё нет
Base.metadata.create_all(bind=engine)

app = FastAPI(
     title="TravelNotes API",
     description="API для управления заметками о путешествиях",
     version=version,
     contact={"name": "Support", "email": "support@travelnotes.com"},
     debug = DEBUG
 )

# обработчики ошибок
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# маршруты

@app.get("/", response_model = schemas.InfoResponse, tags=["info"])
def read_root():
    """
    Базовый ендпоинт для проверки работы api.
    """
    return get_root_info()


# Получить все заметки
@app.get("/notes", response_model=List[schemas.NoteResponse],tags=["notes"])
def read_notes(db: Session = Depends(get_db),
               skip: int = 0, 
               limit: int = 100,
               is_done: Optional[bool] = None):
            return get_notes(db, skip, limit, is_done)


# Создать новую заметку
@app.post("/notes",response_model=schemas.NoteResponse,status_code=status.HTTP_201_CREATED, tags=["notes"])
def create_note(title: str = Query(..., min_length=1),description: Optional[str] = Query(None),db: Session = Depends(get_db)):
    note_data = schemas.NoteCreate(title=title,description=description)
    return create_note_service(note_data, db)


# Поиск заметок по слову в названии (без учёта регистра)
@app.get("/notes/search", response_model=List[schemas.NoteResponse], tags=["notes"])
def search_notes(query: str = Query(..., min_length=3), db: Session = Depends(get_db)):
    return search_notes_service(query, db)

 
# Обновить заметку по ID 
@app.put("/notes/{note_id}", response_model=schemas.NoteResponse, tags=["notes"])
def update_note(note_id: int, note_update: schemas.NoteUpdate, db: Session = Depends(get_db)):
    return update_note_service(note_id, note_update, db)

# Удалить заметку по ID
@app.delete("/notes/{note_id}",response_model=None, status_code=status.HTTP_204_NO_CONTENT, tags=["notes"])
def delete_note(note_id: int, db: Session = Depends(get_db)):
    return delete_note_service(note_id, db)



