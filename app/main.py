from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database, version
from .database import Base, engine


import logging

logger = logging.getLogger(__name__)                        #система логирования


# Создаём таблицы, если их ещё нет
# TODO: Переместить создание таблиц в отдельную функцию инициализации или Alembic миграции
# ПРОБЛЕМА: При каждом запуске пытается создать таблицы - не best practice
# РЕКОМЕНДАЦИЯ: Использовать Alembic для управления миграциями БД
Base.metadata.create_all(bind=engine)


app = FastAPI(
     title="TravelNotes API",
     description="API для управления заметками о путешествиях",
     version=version,
     contact={"name": "Support", "email": "support@travelnotes.com"},
     debug = True
 )

# TODO: Добавить middleware для логирования запросов

# TODO: Добавить обработчики ошибок
# @app.exception_handler(Exception)
# async def global_exception_handler(request, exc):
#     return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Функция для подключения к базе
def get_db():
    """
    Функция для подключения к базе данных. Подключает - и после завершения запроса - закрывает.
    
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        if app.debug:                                   #печатаем информацию о том ,что происходит в debug режиме
            print("Сессия базы данных закрыта")


# маршруты

# TODO: Добавить response_model для всех эндпоинтов
@app.get("/", tags=["info"])
def read_root():
    """
    Базовый ендпоинт для проверки работы api.Возвращает: - статус работы приложения,
                                                          - версию API, 
                                                          - список основных эндпоинтов.
    """
    # Информацию о версии API и доступных эндпоинтах
    return {"message": "Приложение TravelNotes работает",
            "status": "ok",
            "version": "1.0.0",
            "endpoints": [
                "/notes",
                "/notes/{id}",
                "/notes/search",
                ],
            }


# Получить все заметки
# БАГ: Нет сортировки - порядок не определен
# TODO: Добавить сортировку по дате создания или приоритету
# TODO: Добавить фильтрацию по is_done
@app.get("/notes", response_model=List[schemas.NoteResponse],tags=["notes"])
def read_notes(db: Session = Depends(get_db),
               skip: int = 0, 
               limit: int = 100 ):
    return db.query(models.Note).offset(skip).limit(limit).all()


# Создать новую заметку
# БАГ КРИТИЧЕСКИЙ: Не используется Pydantic схема для валидации!
# БАГ: Параметры передаются как query params вместо request body
@app.post("/notes", response_model=schemas.NoteCreate, status_code=status.HTTP_201_CREATED,tags=["notes"] )
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    # проверка на дубликаты заметок с одинаковым title
    existing = db.query(models.Note).filter(models.Note.title == note.title).first()
    if existing:
        raise HTTPException(status_code=400, detail="Заметка с таким названием уже существует")
    # валидация длины title и description
    if len(note.title.strip()) < 3:
        raise HTTPException(status_code=400, detail="Название слишком короткое")
    if note.description is not None and len(note.description.strip()) < 3:
        raise HTTPException(status_code=400, detail="Описание слишком короткое")
    # TODO: Добавить try-except для обработки ошибок БД
    new_note = models.Note(title=note.title, description=note.description)
    db.add(new_note)
    # TODO: Обернуть commit в try-except для отката транзакции при ошибке
    db.commit()
    db.refresh(new_note)
    return new_note


# Поиск заметок по слову в названии (без учёта регистра)
# TODO: Добавить поиск также по description
# TODO: Добавить валидацию query параметра (минимальная длина)
# TODO: Сделать query обязательным или вернуть ошибку если пустой
@app.get("/notes/search", response_model=List[schemas.NoteResponse], tags=["notes"])
def search_notes(query: str, db: Session = Depends(get_db)):
    # проверка, что строка не пустая
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    # TODO: Добавить пагинацию
    # УЛУЧШЕНИЕ: Можно добавить поиск по нескольким полям одновременно
    return db.query(models.Note).filter(models.Note.title.ilike(f"%{query}%")).all()


# Обновить статус заметки по слову в названии
# БАГ КРИТИЧЕСКИЙ: Обновляет ВСЕ заметки соответствующие запросу!
# ПРОБЛЕМА АРХИТЕКТУРНАЯ: Неправильный подход - обновление по частичному совпадению title
# TODO: ИСПРАВИТЬ: Использовать schemas.NoteUpdate в теле запроса
@app.put("/notes/update_by_title", response_model=List[schemas.NoteResponse], tags=["notes"])
def update_note_status_by_title(title_query: str, is_done: bool, db: Session = Depends(get_db)):
    # БАГ: Находит несколько заметок и обновляет все - опасное поведение!
    # КРИТИЧНО: Пользователь может случайно изменить не те заметки
    notes = db.query(models.Note).filter(models.Note.title.ilike(f"%{title_query}%")).all()
    if not notes:
        raise HTTPException(status_code=404, detail="Заметки не найдены")
    
    
    for note in notes:
        note.is_done = is_done
        db.refresh(note)
        db.commit() 
    return notes

# Обновить заметку по ID (правильный способ!)
@app.put("/notes/{note_id}", response_model=schemas.NoteResponse, tags=["notes"])
def update_note(note_id: int, note_update: schemas.NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    for key, value in note_update.dict(exclude_unset=True).items():
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note

# Удалить заметку по ID
@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["notes"])
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    db.delete(note)
    db.commit()
    return None

# TODO: Вынести всю бизнес-логику в отдельный слой (services)
# АРХИТЕКТУРА: Сейчас логика смешана с роутами - плохая практика
# РЕКОМЕНДАЦИЯ: Создать app/services/note_service.py для бизнес-логики



# TODO: Добавить тесты (pytest)
# КРИТИЧНО: Нет ни одного теста!

# TODO: Добавить обработку ошибок базы данных
# TODO: Добавить аутентификацию и авторизацию если требуется


