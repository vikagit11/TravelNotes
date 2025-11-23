"""
Примеры тестов для API TravelNotes

ЗАДАНИЕ: Дописать тесты для всех эндпоинтов по аналогии с примерами ниже.
"""

import pytest


@pytest.fixture
def sample_note(client):
    """Фикстура создаёт тестовую заметку для использования в тестах."""
    response = client.post(
        "/notes",
        params={"title": "Тестовая заметка", "description": "Описание для теста"}
    )
    return response.json()


# ПРИМЕР 1: Простой GET запрос
def test_read_root(client):
    """Проверяем, что корневой эндпоинт возвращает правильное сообщение."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Приложение TravelNotes работает!"}


# ПРИМЕР 2: POST запрос - создание ресурса
def test_create_note_success(client):
    """Проверяем успешное создание заметки."""
    response = client.post(
        "/notes",
        params={"title": "Поездка в Париж", "description": "Посетить Эйфелеву башню"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Поездка в Париж"
    assert data["description"] == "Посетить Эйфелеву башню"
    assert data["is_done"] is False
    assert "id" in data
    assert "created_at" in data


# ПРИМЕР 3: Использование фикстуры
def test_search_notes_found(client, sample_note):
    """Проверяем поиск заметок. Фикстура sample_note автоматически создаёт заметку."""
    response = client.get("/notes/search", params={"query": "Тестовая"})
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Тестовая" in data[0]["title"]


# TODO: Допишите тесты по аналогии с примерами выше:
# 1. test_create_note_without_description - создание заметки без описания
# 2. test_read_all_notes - получение списка всех заметок
# 3. test_read_notes_empty_list - пустой список при отсутствии заметок
# 4. test_search_notes_not_found - поиск без результатов
# 5. test_update_note_by_id - обновление заметки по ID
# 6. test_delete_note - удаление заметки
# 7. test_delete_note_not_found - попытка удалить несуществующую заметку
