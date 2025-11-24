"""
Файл конфигурации pytest с общими фикстурами.

conftest.py - специальный файл pytest, который содержит фикстуры,
доступные для всех тестов в проекте.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base


# Конфигурация тестовой базы данных
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    """
    Создаёт и очищает базу данных для каждого теста.
    scope="function" означает, что фикстура вызывается перед каждым тестом.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    """
    Создаёт сессию базы данных для теста.
    Полезно, если нужно напрямую работать с БД в тесте.
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(test_db):
    """
    Создаёт тестовый HTTP клиент для FastAPI приложения.
    """
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
