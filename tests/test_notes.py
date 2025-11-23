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
    
    data = response.json()
    assert data["message"] == "Приложение TravelNotes работает!"


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
    
# Получение списка всех заметок
def test_read_all_notes(client,sample_note):
    """Получаем список всех заметок"""
    response = client.get("/notes")
    assert response.status_code == 200
    data = response.json()
    first_note = data[0]
    assert "title" in first_note

    
    
#Удаление заметки по id
def test_delete_note(client, sample_note):
    """Проверяем успешное удаление заметки по ID"""
    note_id = sample_note["id"]
    response = client.delete(f"/notes/{note_id}")
    
    assert response.status_code == 204
    
#Попытка удалить несуществующую заметку
def test_delete_note_not_found(client):
    """Попытка удалить несуществующую заметку"""
    response =client.delete("/notes/999")
    assert response.status_code == 404
    
# поиск без результатов
def test_search_notes_not_found(client):
    """Поиск без результатов, который не найдет ничего"""
    response = client.get("/notes/search", params={"query": "?????????"})            
    assert response.status_code == 200
    data = response.json()
    assert data == []
    
    


# TODO: Допишите тесты по аналогии с примерами выше:
# 1. test_create_note_without_description - создание заметки без описания
# 3. test_read_notes_empty_list - пустой список при отсутствии заметок
# 6. test_delete_note - удаление заметки
