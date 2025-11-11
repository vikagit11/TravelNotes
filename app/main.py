from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from .database import Base, engine


# Создаём таблицы, если их ещё нет
Base.metadata.create_all(bind=engine)


app = FastAPI()

# Функция для подключения к базе
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
# маршруты


@app.get("/")
def read_root():
    return {"message": "Приложение TravelNotes работает!"}

# Получить все заметки
@app.get("/notes")
def read_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()


# Создать новую заметку
@app.post("/notes")
def create_note(title: str, description: str | None = None, db: Session = Depends(get_db)):
    new_note = models.Note(title=title, description=description)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


# Поиск заметок по слову в названии (без учёта регистра)
@app.get("/notes/search")
def search_notes(query: str, db: Session = Depends(get_db)):
    return db.query(models.Note).filter(models.Note.title.ilike(f"%{query}%")).all()


# Обновить статус заметки по слову в названии
@app.put("/notes/update_by_title")
def update_note_status_by_title(title_query: str, is_done: bool, db: Session = Depends(get_db)):
    notes = db.query(models.Note).filter(models.Note.title.ilike(f"%{title_query}%")).all()
    if not notes:
        raise HTTPException(status_code=404, detail="Заметки не найдены")
    for note in notes:
        note.is_done = is_done
        db.commit()
        db.refresh(note)
    return notes

