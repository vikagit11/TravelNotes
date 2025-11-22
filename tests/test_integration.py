"""
Примеры интеграционных тестов для TravelNotes API.

ЗАДАНИЕ: Дописать интеграционные тесты по аналогии с примером.
"""

import pytest


def test_full_crud_workflow(client):
    """Тест полного цикла CRUD: Create -> Read -> Update -> Delete"""
    # 1. Создаём заметку
    create_response = client.post(
        "/notes",
        params={"title": "Поездка в Токио", "description": "Посетить храмы"}
    )
    assert create_response.status_code == 201
    note_id = create_response.json()["id"]
    
    # 2. Читаем список заметок
    read_response = client.get("/notes")
    assert read_response.status_code == 200
    notes = read_response.json()
    assert len(notes) == 1
    
    # 3. Обновляем заметку
    update_response = client.put(
        f"/notes/{note_id}",
        json={"title": "Поездка в Токио (обновлено)", "is_done": True}
    )
    assert update_response.status_code == 200
    assert update_response.json()["is_done"] is True
    
    # 4. Удаляем заметку
    delete_response = client.delete(f"/notes/{note_id}")
    assert delete_response.status_code == 204
    
    # 5. Проверяем, что заметка удалена
    final_response = client.get("/notes")
    assert len(final_response.json()) == 0


# TODO: Допишите интеграционные тесты:
# 1. test_create_and_search_workflow - создание и поиск нескольких заметок
# 2. test_empty_database_all_endpoints - проверка всех эндпоинтов на пустой БД
# 3. test_multiple_updates_workflow - несколько обновлений одной заметки подряд
