import pytest
from conftest import client


@pytest.fixture
async def created_menu():
    # Создание меню
    new_menu_data = {"title": "New Menu",
                     "description": "Description of new menu"}
    response_menu = client.post("/api/v1/menus", json=new_menu_data)

    # Проверка статус кода
    assert response_menu.status_code == 201

    # Проверка, что меню было успешно создано
    assert "id" in response_menu.json()

    return response_menu.json()["id"]


async def test_add_menu(created_menu):
    # Получаем созданное меню
    menu_id = created_menu

    # Проверяем, что меню было создано и имеет ожидаемые данные
    response_get = client.get(f"/api/v1/menus/{menu_id}")
    assert response_get.status_code == 200
    assert response_get.json()["title"] == "New Menu"
    assert response_get.json()["description"] == "Description of new menu"


async def test_modify_menu(created_menu):
    # Получаем созданное меню
    menu_id = created_menu

    # Новые данные для обновления меню
    updated_menu_data = {"title": "Updated Menu",
                         "description": "Updated description of the menu"}

    # Отправляем PATCH-запрос для обновления меню
    response_patch = client.patch(f"/api/v1/menus/{menu_id}",
                                  json=updated_menu_data)
    assert response_patch.status_code == 200

    # Проверяем, что меню было успешно обновлено
    response_get = client.get(f"/api/v1/menus/{menu_id}")
    assert response_get.status_code == 200
    assert response_get.json()["title"] == "Updated Menu"
    assert (response_get.json()["description"] == "Up"
            "dated description of the menu")


async def test_delete_menu(created_menu):
    # Получаем созданное меню
    menu_id = created_menu

    # Отправляем DELETE-запрос для удаления меню
    response_delete = client.delete(f"/api/v1/menus/{menu_id}")
    assert response_delete.status_code == 200

    # Проверяем, что меню больше не существует
    response_get = client.get(f"/api/v1/menus/{menu_id}")
    assert response_get.status_code == 404
