from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import DATABASE_URL, DEBUG
import logging


SQLALCHEMY_DATABASE_URL = DATABASE_URL

logger = logging.getLogger(__name__)
    
try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        echo=DEBUG,
        connect_args={"check_same_thread": False}
    )
    # Проверяем подключение
    with engine.connect() as conn:
        pass
except Exception as e:
    logger.critical(f"Failed to connect to database: {e}")
    raise                                                                     # Перевыбрасываем - приложение не должно запускаться без БД

    
# Сессии для работы с БД 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Функция для подключения к базе               
def get_db():
    """Функция для подключения к базе данных. Подключает - и после завершения запроса - закрывает."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()
        if DEBUG:
            logger.debug("Database session closed")