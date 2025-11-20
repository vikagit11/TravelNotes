from fastapi import FastAPI, Depends, HTTPException
# TODO: Добавить импорт для корректной типизации response_model
# TODO: Добавить импорт Query для валидации query параметров
from fastapi import Query, status
from sqlalchemy.orm import Session
# TODO: Добавить импорт для обработки списков в response_model
from typing import List
from . import models, schemas, database
from .database import Base, engine


# Создаём таблицы, если их ещё нет
# TODO: Переместить создание таблиц в отдельную функцию инициализации или Alembic миграции
# ПРОБЛЕМА: При каждом запуске пытается создать таблицы - не best practice
# РЕКОМЕНДАЦИЯ: Использовать Alembic для управления миграциями БД
Base.metadata.create_all(bind=engine)


# TODO: Добавить метаданные приложения для автодокументации
app = FastAPI(
     title="TravelNotes API",
     description="API для управления заметками о путешествиях",
     version="1.0.0",
     contact={"name": "Support", "email": "support@travelnotes.com"}
 )

# TODO: Добавить middleware для логирования запросов

# TODO: Добавить обработчики ошибок
# @app.exception_handler(Exception)
# async def global_exception_handler(request, exc):
#     return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Функция для подключения к базе
# TODO: Добавить docstring
def get_db():
    """
    Функция для подключения к базе данных. Подключает - и после завершения запроса - закрывает.
    
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
         # TODO: Добавить логирование закрытия сессии в debug режиме
        print("Сессия базы данных закрыта")


# маршруты

# TODO: Добавить response_model для всех эндпоинтов
# TODO: Добавить теги для группировки в документации
@app.get("/")
def read_root():
    """
    Базовый ендпоинт ддля проверки работы api.Возвращает статус работы приложения.
    """
    # УЛУЧШЕНИЕ: Добавить информацию о версии API и доступных эндпоинтах
    return {"message": "Приложение TravelNotes работает!"}


# Получить все заметки
# БАГ: Нет пагинации - может вернуть тысячи записей
# БАГ: Нет сортировки - порядок не определен
# TODO: Добавить пагинацию с skip и limit параметрами
# TODO: Добавить сортировку по дате создания или приоритету
# TODO: Добавить фильтрацию по is_done
@app.get("/notes", response_model=List[schemas.NoteResponse])
# TODO: Добавить response_model=List[schemas.Note]
# TODO: Добавить tags=["notes"] для документации
def read_notes(db: Session = Depends(get_db)):
    # БАГ: Отсутствует пагинация
    # ИСПРАВИТЬ: Добавить skip: int = 0, limit: int = 100
    # return db.query(models.Note).offset(skip).limit(limit).all()
    return db.query(models.Note).all()


# Создать новую заметку
# БАГ КРИТИЧЕСКИЙ: Не используется Pydantic схема для валидации!
# БАГ: Параметры передаются как query params вместо request body
# TODO: ИСПРАВИТЬ: Использовать schemas.NoteCreate в теле запроса
@app.post("/notes", response_model=schemas.NoteResponse, status_code=status.HTTP_201_CREATED)
# TODO: Добавить response_model=schemas.Note, status_code=status.HTTP_201_CREATED
# TODO: ИСПРАВИТЬ сигнатуру: def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
def create_note(title: str, description: str | None = None, db: Session = Depends(get_db)):
    # TODO: Добавить проверку на дубликаты заметок с одинаковым title
    # TODO: Добавить валидацию длины title и description
    # TODO: Добавить try-except для обработки ошибок БД
    new_note = models.Note(title=title, description=description)
    db.add(new_note)
    # TODO: Обернуть commit в try-except для отката транзакции при ошибке
    db.commit()
    db.refresh(new_note)
    return new_note


# Поиск заметок по слову в названии (без учёта регистра)
# TODO: Добавить поиск также по description
# TODO: Добавить валидацию query параметра (минимальная длина)
# TODO: Сделать query обязательным или вернуть ошибку если пустой
@app.get("/notes/search", response_model=List[schemas.NoteResponse])
# TODO: Добавить response_model=List[schemas.Note]
# ПРОБЛЕМА: Этот эндпоинт должен быть ПЕРЕД /notes/{id} если добавите его в будущем
def search_notes(query: str, db: Session = Depends(get_db)):
    # БАГ: query может быть пустой строкой - нет валидации
    # TODO: Добавить проверку: if not query.strip(): raise HTTPException(400, "Query cannot be empty")
    # TODO: Добавить пагинацию
    # УЛУЧШЕНИЕ: Можно добавить поиск по нескольким полям одновременно
    return db.query(models.Note).filter(models.Note.title.ilike(f"%{query}%")).all()


# Обновить статус заметки по слову в названии
# БАГ КРИТИЧЕСКИЙ: Обновляет ВСЕ заметки соответствующие запросу!
# ПРОБЛЕМА АРХИТЕКТУРНАЯ: Неправильный подход - обновление по частичному совпадению title
# TODO: ИСПРАВИТЬ: Создать эндпоинт PUT /notes/{id} для обновления конкретной заметки
# TODO: ИСПРАВИТЬ: Использовать schemas.NoteUpdate в теле запроса
@app.put("/notes/update_by_title", response_model=List[schemas.NoteResponse])
# TODO: Добавить response_model=List[schemas.Note]
def update_note_status_by_title(title_query: str, is_done: bool, db: Session = Depends(get_db)):
    # БАГ: Находит несколько заметок и обновляет все - опасное поведение!
    # КРИТИЧНО: Пользователь может случайно изменить не те заметки
    notes = db.query(models.Note).filter(models.Note.title.ilike(f"%{title_query}%")).all()
    if not notes:
        raise HTTPException(status_code=404, detail="Заметки не найдены")
    
    # БАГ: db.commit() вызывается в цикле - неэффективно
    # TODO: ИСПРАВИТЬ: Вынести db.commit() за пределы цикла
    for note in notes:
        note.is_done = is_done
       #  # БАГ: commit в цикле!
        db.refresh(note)
        db.commit() 
    
    return notes


# TODO: ДОБАВИТЬ ОТСУТСТВУЮЩИЕ CRUD операции:

# TODO: Обновить заметку по ID (правильный способ!)
@app.put("/notes/{note_id}", response_model=schemas.NoteResponse)
def update_note(note_id: int, note_update: schemas.NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    for key, value in note_update.dict(exclude_unset=True).items():
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note

# TODO: Удалить заметку по ID
@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
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

# TODO: Добавить систему логирования
# import logging
# logger = logging.getLogger(__name__)

# TODO: Добавить тесты (pytest)
# КРИТИЧНО: Нет ни одного теста!

# TODO: Добавить обработку ошибок базы данных
# TODO: Добавить аутентификацию и авторизацию если требуется


