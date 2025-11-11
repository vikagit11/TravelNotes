from pydantic import BaseModel


# Базовая схема: общие поля для всех заметок
class NoteBase(BaseModel):
    title: str
    description: str | None = None


# создание новой заметки (наследует NoteBase)
class NoteCreate(NoteBase):
    pass


#  вывод данных из базы 
class Note(NoteBase):
    id: int
    is_done: bool

    class Config:
        orm_mode = True
