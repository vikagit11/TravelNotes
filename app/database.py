from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# TODO: Вынести URL базы данных в переменные окружения или config файл
# Пример: DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./travelnotes.db")
SQLALCHEMY_DATABASE_URL = "sqlite:///./travelnotes.db"

# TODO: Добавить обработку ошибок подключения к базе данных
# РЕКОМЕНДАЦИЯ: Обернуть создание engine в try-except блок
# TODO: Добавить логирование (echo=True в режиме разработки)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Сессии для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

