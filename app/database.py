from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Путь к базе данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./travelnotes.db"

#  соединение с SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Сессии для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей( note будут наследоваться от base)
Base = declarative_base()
