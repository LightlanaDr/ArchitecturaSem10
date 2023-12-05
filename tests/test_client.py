import pytest
from fastapi.testclient import TestClient
from main import app


def test_get_all_clients(temp_db):
    "Тест GET-запроса для получения всех клиентов"

    with TestClient(app) as client:
        response = client.get("/clients/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_client(temp_db):
    "Тест POST-запроса для создания нового клиента"
    client_data = {
        "document": "1234567890",
        "surName": "Дружкова",
        "firstName": "Светлана",
        "patronymic": "Алексеевна",
        "birthday": "1993-01-01",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 200
    assert "id" in response.json()


def test_birthday_validating(temp_db):
    "Тест валидации даты рождения при создании клиента"
    client_data = {
        "document": "1234567890",
        "surName": "Дружкова",
        "firstName": "Светлана",
        "patronymic": "Алексеевна",
        "birthday": "2023-01-01",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 404
    detail = {
        'detail': 'Возраст не может быть меньше 18 лет'
    }
    assert response.json() == detail


def test_update_client(temp_db):
    "Тест обновления данных клиента"
    client_data = {
        "document": "1234567890",
        "surName": "Дружкова",
        "firstName": "Светлана",
        "patronymic": "Алексеевна",
        "birthday": "1993-01-01",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 200
    client_id = response.json()["id"]

    new_client_data = {
        "document": "1234567890",
        "surName": "Дружкова",
        "firstName": "Ольга",
        "patronymic": "Сергеевна",
        "birthday": "1993-01-01",
    }
    with TestClient(app) as client:
        response = client.put(f"/clients/{client_id}", json=new_client_data)
    assert response.status_code == 200
    assert response.json() == {**new_client_data, "id": client_id}


def test_delete_client(temp_db):
    "Тест удаления клиента"
    client_data = {
        "document": "1234567890",
        "surName": "Дружкова",
        "firstName": "Ольга",
        "patronymic": "Сергеевна",
        "birthday": "1993-01-01",
    }
    with TestClient(app) as client:
        response = client.post("/clients/", json=client_data)
    assert response.status_code == 200
    client_id = response.json()["id"]

    with TestClient(app) as client:
        response = client.delete(f"/clients/{client_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Пользователь удален"}

    with TestClient(app) as client:
        response = client.get(f"/clients/{client_id}")
    assert response.status_code == 404


if __name__ == '__main__':
    pytest.main(['-v'])
