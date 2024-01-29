import pytest
from conftest import async_session_maker, client
from sqlalchemy import select

from models import dish


@pytest.fixture(scope="session")
async def created_menu():
    # Создаем меню
    new_menu_data = {"title": "New Menu",
                     "description": "Description of new menu"}
    response_menu = client.post("/api/v1/menus", json=new_menu_data)
    assert response_menu.status_code == 201
    menu_id = response_menu.json()["id"]
    return menu_id


@pytest.fixture(scope="session")
async def created_submenu(created_menu):
    # Создаем подменю для созданного меню
    menu_id = created_menu
    new_submenu_data = {"title": "New SubMenu",
                        "description": "Description of new submenu",
                        "menu_id": menu_id}
    response_submenu = client.post(f"/api/v1/menus/{menu_id}/submenus",
                                   json=new_submenu_data)
    assert response_submenu.status_code == 201
    submenu_id = response_submenu.json()["id"]
    return submenu_id


@pytest.fixture(scope="session")
async def created_dish_1(created_menu, created_submenu):
    # Создаем первое блюдо для созданного меню и подменю
    menu_id = created_menu
    submenu_id = created_submenu
    new_dish_data = {"title": "Dish 1",
                     "description": "Description of dish 1",
                     "price": 9.99}
    response_dish = client.post(
        f"/api/v1/menus/{menu_id}/"
        f"submenus/{submenu_id}/dishes",
        json=new_dish_data)
    assert response_dish.status_code == 201
    dish_id = response_dish.json()["id"]
    return dish_id


@pytest.fixture(scope="session")
async def created_dish_2(created_menu, created_submenu):
    # Создаем второе блюдо для созданного меню и подменю
    menu_id = created_menu
    submenu_id = created_submenu
    new_dish_data = {"title": "Dish 2",
                     "description": "Description of dish 2",
                     "price": 12.99}
    response_dish = client.post(f"/api/v1/menus/{menu_id}/"
                                f"submenus/{submenu_id}/dishes",
                                json=new_dish_data)
    assert response_dish.status_code == 201
    dish_id = response_dish.json()["id"]
    return dish_id


async def test_create_menu(created_menu):
    # Получаем данные созданного меню
    response = client.get(f"/api/v1/menus/{created_menu}")
    assert response.status_code == 200
    menu_data = response.json()

    # Проверяем, что атрибуты созданного меню соответствуют ожидаемым
    assert menu_data["title"] == "New Menu"
    assert menu_data["description"] == "Description of new menu"


async def test_create_submenu(created_submenu, created_menu):
    # Получаем данные созданного подменю
    response = client.get(
        f"/api/v1/menus/{created_menu}/submenus/{created_submenu}")
    assert response.status_code == 200
    submenu_data = response.json()

    # Проверяем, что атрибуты созданного подменю соответствуют ожидаемым
    assert submenu_data["title"] == "New SubMenu"
    assert submenu_data["description"] == "Description of new submenu"


async def test_create_dish_1(created_dish_1, created_submenu):
    # Получаем данные созданного блюда
    response = client.get(
        f"/api/v1/menus/{created_menu}/submenus/{created_submenu}/"
        f"dishes/{created_dish_1}")
    assert response.status_code == 200
    dish_data = response.json()

    # Проверяем, что атрибуты созданного блюда соответствуют ожидаемым
    assert dish_data["title"] == "Dish 1"
    assert dish_data["description"] == "Description of dish 1"
    assert dish_data["price"] == "9.99"


async def test_create_dish_2(created_dish_2, created_submenu):
    # Получаем данные созданного блюда
    response = client.get(
        f"/api/v1/menus/{created_menu}/"
        f"submenus/{created_submenu}/dishes/{created_dish_2}")
    assert response.status_code == 200
    dish_data = response.json()

    # Проверяем, что атрибуты созданного блюда соответствуют ожидаемым
    assert dish_data["title"] == "Dish 2"
    assert dish_data["description"] == "Description of dish 2"
    assert dish_data["price"] == "12.99"


async def test_view_menu_with_submenus_and_dishes(created_menu,
                                                  created_submenu,
                                                  created_dish_1,
                                                  created_dish_2):
    # Получаем данные о созданном меню с подменю и блюдами
    response = client.get(f"/api/v1/menus/{created_menu}")
    assert response.status_code == 200
    menu_data = response.json()

    # Проверяем, что атрибуты созданного меню соответствуют ожидаемым
    assert menu_data["id"] == created_menu

    # Проверяем количество подменю и блюд
    assert menu_data["submenus_count"] == 1
    assert menu_data["dishes_count"] == 2


async def test_view_submenu(created_menu,
                            created_submenu,
                            created_dish_1,
                            created_dish_2):
    # Отправляем запрос на получение информации о созданном подменю
    response = client.get(
        f"/api/v1/menus/{created_menu}/submenus/{created_submenu}")
    assert response.status_code == 200

    # Проверяем, что ответ содержит ожидаемые данные подменю
    submenu_data = response.json()
    assert submenu_data["id"] == created_submenu
    assert submenu_data["dishes_count"] == 2


async def test_delete_submenu(created_menu, created_submenu):
    # Удаляем подменю
    response = client.delete(
        f"/api/v1/menus/{created_menu}/submenus/{created_submenu}")
    assert response.status_code == 200


async def test_view_deleted_submenu(created_menu):
    # Пытаемся получить информацию о удаленном подменю
    response = client.get(f"/api/v1/menus/{created_menu}/submenus/")
    assert response.status_code == 200
    assert response.json() == []


async def test_view_dishes_of_deleted_submenu(created_menu, created_submenu):
    # Пытаемся получить список блюд удаленного подменю
    response = client.get(
        f"/api/v1/menus/{created_menu}/submenus/{created_submenu}/dishes")

    # Ожидается, что запрос вернет пустой список блюд
    assert response.status_code == 200
    assert response.json() == []


async def test_view_menu_with_submenus_and_dishes2(created_menu):
    # Получаем данные о созданном меню с подменю и блюдами
    response = client.get(f"/api/v1/menus/{created_menu}")
    assert response.status_code == 200
    menu_data = response.json()

    # Проверяем, что атрибуты созданного меню соответствуют ожидаемым
    assert menu_data["id"] == created_menu

    # Проверяем количество подменю и блюд
    assert menu_data["submenus_count"] == 0
    assert menu_data["dishes_count"] == 0


async def test_delete_menu(created_menu):
    # Удаляем меню
    response = client.delete(f"/api/v1/menus/{created_menu}")
    assert response.status_code == 200


async def test_view_menus():
    # Получаем список меню
    response = client.get("/api/v1/menus")

    # Ожидается, что запрос вернет пустой список меню
    print(response.json())
    assert response.status_code == 200
    assert response.json() == []
