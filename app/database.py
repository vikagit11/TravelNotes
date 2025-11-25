from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import DATABASE_URL, DEBUG


SQLALCHEMY_DATABASE_URL = DATABASE_URL

# TODO: Пустой except - если подключение не удалось, engine будет undefined
# Используйте: except Exception as e: + logger.critical() + raise
try:
    engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=True,                                                          #включили логирование SQL запросов в режиме разработки(sql в консоли)
    connect_args={"check_same_thread": False})                                                                                                                
except:
    print("Ошибка: не удалось подключиться к базе данных.")  # TODO: raise вместо print

# Сессии для работы с БД 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Функция для подключения к базе
def get_db():
    """
    Функция для подключения к базе данных. Подключает - и после завершения запроса - закрывает.
    
    """
    # TODO: Пустой except скрывает ошибки + db может быть undefined
    # Уберите try/except из начала, оставьте только в yield
    try:
     db = SessionLocal()
     yield db
    except:
       print("Ошибка подключения к базе данных")  # TODO: logger.error() + raise
        
    finally:
        db.close()
        
        if  DEBUG:                                   #печатаем информацию о том ,что происходит в debug режиме
            print("Сессия базы данных закрыта")