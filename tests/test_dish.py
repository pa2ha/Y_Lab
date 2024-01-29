import pytest
from conftest import async_session_maker, client
from sqlalchemy import select

from models import dish


@pytest.fixture
async def created_menu():
    # Создание меню
    new_menu_data = {"title": "New Menu",
                     "description": "Description of new menu"}
    response_menu = client.post("/api/v1/menus", json=new_menu_data)
    assert response_menu.status_code == 201
    menu_id = response_menu.json()["id"]
    return menu_id


@pytest.fixture
async def created_submenu(created_menu):
    # Создание подменю для созданного меню
    menu_id = created_menu
    new_submenu_data = {"title": "New SubMenu",
                        "description": "Description of new submenu",
                        "menu_id": menu_id}
    response_submenu = client.post(f"/api/v1/menus/{menu_id}/submenus",
                                   json=new_submenu_data)
    assert response_submenu.status_code == 201
    submenu_id = response_submenu.json()["id"]
    return submenu_id


@pytest.fixture
async def created_dish(created_menu, created_submenu):
    # Создание блюда для созданного меню и подменю
    menu_id = created_menu
    submenu_id = created_submenu
    new_dish_data = {"title": "New Dish",
                     "description": "Description of new dish",
                     "price": "9.99"}
    response_dish = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json=new_dish_data)
    assert response_dish.status_code == 201
    dish_id = response_dish.json()["id"]
    return dish_id


async def test_add_dish(created_menu, created_submenu):
    # Добавляем блюдо
    new_dish_data = {"title": "New Dish",
                     "description": "Description of new dish",
                     "price": 9.99}
    response_dish = client.post(
        f"/api/v1/menus/{created_menu}/submenus/{created_submenu}/dishes",
        json=new_dish_data)
    assert response_dish.status_code == 201

    # Проверяем, что блюдо успешно добавлено
    async with async_session_maker() as session:
        query = select(dish).where(dish.c.title == "New Dish")
        result = await session.execute(query)
        dishes = result.fetchall()
        assert len(dishes) == 1
        assert dishes[0].title == new_dish_data["title"]
        assert dishes[0].description == new_dish_data["description"]
        assert float(dishes[0].price) == new_dish_data["price"]


async def test_modify_dish(created_dish, created_menu, created_submenu):
    # Получаем ID созданного блюда
    dish_id = created_dish

    # Обновляем данные блюда
    updated_dish_data = {"title": "Updated Dish",
                         "description": "Updated description of the dish",
                         "price": "12.99"}
    response_update = client.patch(f"/api/v1/menus/{created_menu}/"
                                   f"submenus/{created_submenu}/"
                                   f"dishes/{dish_id}",
                                   json=updated_dish_data)
    assert response_update.status_code == 200

    # Проверяем, что данные блюда успешно обновлены
    response_get = client.get(
        f"/api/v1/menus/{created_menu}/"
        f"submenus/{created_submenu}/dishes/{dish_id}")
    updated_dish = response_get.json()
    assert updated_dish["title"] == updated_dish_data["title"]
    assert updated_dish["description"] == updated_dish_data["description"]
    assert updated_dish["price"] == updated_dish_data["price"]


async def test_delete_dish(created_dish, created_menu, created_submenu):
    # Получаем ID созданного блюда
    dish_id = created_dish

    # Удаляем блюдо
    response_delete = client.delete(
        f"/api/v1/menus/{created_menu}/"
        f"submenus/{created_submenu}/dishes/{dish_id}")
    assert response_delete.status_code == 200

    # Проверяем, что блюдо успешно удалено
    async with async_session_maker() as session:
        query = select(dish).where(dish.c.id == dish_id)
        result = await session.execute(query)
        dishes = result.fetchall()
        assert len(dishes) == 0
