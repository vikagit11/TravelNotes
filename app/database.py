from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import DATABASE_URL, DEBUG


SQLALCHEMY_DATABASE_URL = DATABASE_URL


try:
    engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=True,                                                          #включили логирование SQL запросов в режиме разработки(sql в консоли)
    connect_args={"check_same_thread": False})                                                                                                                
except:
    print("Ошибка: не удалось подключиться к базе данных.")

# Сессии для работы с БД 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Функция для подключения к базе
def get_db():
    """
    Функция для подключения к базе данных. Подключает - и после завершения запроса - закрывает.
    
    """
    try:
     db = SessionLocal()
     yield db
    except:
       print("Ошибка подключения к базе данных")
        
    finally:
        db.close()
        
        if  DEBUG:                                   #печатаем информацию о том ,что происходит в debug режиме
            print("Сессия базы данных закрыта")