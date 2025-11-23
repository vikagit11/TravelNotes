# Руководство по тестированию TravelNotes

## Установка зависимостей

Установите все необходимые пакеты:

```bash
pip install -r requirements.txt
```

## Запуск тестов

### Запустить все тесты:
```bash
pytest
```

### Запустить тесты с подробным выводом:
```bash
pytest -v
```

### Запустить конкретный файл:
```bash
pytest tests/test_notes.py
```

### Запустить конкретный тест:
```bash
pytest tests/test_notes.py::test_create_note_success
```

### Запустить тесты с покрытием кода:
```bash
pytest --cov=app
```

## Структура тестов

```
tests/
├── conftest.py              # Общие фикстуры (БД, клиент)
├── test_notes.py            # Unit-тесты для эндпоинтов
├── test_integration.py      # Интеграционные тесты
└── README.md                # Это руководство
```

## Что реализовано

✅ Настройка тестовой базы данных (SQLite in-memory)  
✅ Фикстуры для клиента и тестовых данных  
✅ 3 примера unit-тестов  
✅ 1 пример интеграционного теста  

## Ваши задания

### Базовый уровень (обязательно):

1. Допишите закомментированные тесты в `test_notes.py`:
   - `test_create_note_without_description` 
   - `test_read_all_notes`
   - `test_read_notes_empty_list`
   - `test_search_notes_not_found`
   - `test_update_note_by_id`
   - `test_delete_note`
   - `test_delete_note_not_found`

2. Добавьте интеграционные тесты в `test_integration.py`:
   - `test_create_and_search_workflow`
   - `test_empty_database_all_endpoints`

### Продвинутый уровень (по желанию):

3. Параметризованные тесты (@pytest.mark.parametrize)
4. Тесты на граничные значения (длинные строки, спецсимволы)
5. Тесты временных меток (created_at, updated_at)
6. Тесты производительности

## Best Practices

### Структура теста (AAA паттерн):
```python
def test_example(client):
    # Arrange (подготовка)
    data = {"title": "Test"}
    
    # Act (действие)
    response = client.post("/notes", params=data)
    
    # Assert (проверка)
    assert response.status_code == 201
```

### Именование тестов:
```
test_<что_тестируем>_<ожидаемый_результат>

Примеры:
- test_create_note_success
- test_delete_note_not_found
- test_search_notes_empty_result
```

### Что проверять в тестах:
1. ✅ Статус код ответа
2. ✅ Структура данных в ответе
3. ✅ Значения полей
4. ✅ Наличие обязательных полей
5. ✅ Побочные эффекты (создание/удаление записей)

## Полезные ссылки

- [Документация pytest](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest фикстуры](https://docs.pytest.org/en/stable/fixture.html)

---

**Удачи в написании тестов! 🚀**
