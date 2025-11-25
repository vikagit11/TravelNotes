from app import version
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Query, status 
from app import models, schemas, database, version
from app.database import get_db



def get_root_info():
    """
    Формирование информации о приложении.
    Возвращает статус, версию и список основных эндпоинтов.
    """
    return {"message": "Приложение TravelNotes работает!",     # Информация о версии API и доступных эндпоинтах
            "status": "ok",
            "version": version, 
            "endpoints": [
                "/notes",
                "/notes/{id}",
                "/notes/search",
                ],
            }
    
def get_notes(db: Session = Depends(get_db),
               skip: int = 0, 
               limit: int = 100,
               is_done: Optional[bool] = None):
            """
            Получение списка заметок с фильтрацией по статусу и сортировкой.
            """
            query = db.query(models.Note)                                #создаем базовый запрос
            if is_done is not None:                                      #фильтрация по is_done
               query = query.filter(models.Note.is_done == is_done)         # возвращаем все true или все false
            query = query.order_by(models.Note.created_at.desc())        #сортировка по дате создания от новых к старым
            return query.offset(skip).limit(limit).all() 
        
        
def create_note_service( title: str,                                   
                 description: Optional[str] = None,
                 db: Session = Depends(get_db)):
    """Создает новую заметку"""
    # проверка на дубликаты заметок с одинаковым title
    existing = db.query(models.Note).filter(models.Note.title == title).first()
    if existing:
        raise HTTPException(status_code=400, detail="Заметка с таким названием уже существует")
    # валидация длины title и description
    if len(title.strip()) < 3:
        raise HTTPException(status_code=400, detail="Название слишком короткое")
    if description is not None and len(description.strip()) < 3:
        raise HTTPException(status_code=400, detail="Описание слишком короткое")
    try:
        new_note = models.Note(title=title, description=description)
        db.add(new_note)
    except:
        print("Ошибка базы данных")    
    try:
        db.commit()
    except:
        print("Ошибка: откат транзакции")
    db.refresh(new_note)
    return new_note



def search_notes_service(query: str, db: Session = Depends(get_db)):
    """Поиск заметок"""
    if not query.strip():                                                                         # проверка, что строка не пустая
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    if len(query.strip()) < 3:
        raise HTTPException(status_code=400, detail="Query too short")                            # проверка на минимальную длину
    # УЛУЧШЕНИЕ: Можно добавить поиск по нескольким полям одновременно                            # поиск по title ИЛИ по description
    return db.query(models.Note).filter(models.Note.title.ilike(f"%{query}%" | models.Note.description.ilike(f"%{query}%"))).all() 


def update_note_service(note_id: int, note_update: schemas.NoteUpdate, db: Session = Depends(get_db)):
    """Обновление заметки по id"""
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    for key, value in note_update.dict(exclude_unset=True).items():
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note


def delete_note_service(note_id: int, db: Session = Depends(get_db)):
    """Удаление заметки по id"""
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    db.delete(note)
    db.commit()
    return None