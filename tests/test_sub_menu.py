import pytest
from conftest import async_session_maker, client
from sqlalchemy import select

from models import submenu


@pytest.fixture
async def created_menu():
    # Создание меню
    new_menu_data = {"title": "New Menu",
                     "description": "Description of new menu"}
    response_menu = client.post("/api/v1/menus", json=new_menu_data)
    assert response_menu.status_code == 201

    # Возвращаем ID созданного меню
    return response_menu.json()["id"]


@pytest.fixture
async def created_submenu(created_menu):
    # Получаем ID созданного меню
    menu_id = created_menu

    # Добавляем подменю
    new_submenu_data = {"title": "New SubMenu",
                        "description": "Description of new submenu",
                        "menu_id": menu_id}
    response_submenu = client.post(f"/api/v1/menus/{menu_id}/submenus",
                                   json=new_submenu_data)
    assert response_submenu.status_code == 201

    # Возвращаем ID созданного подменю
    return response_submenu.json()["id"]


async def test_create_submenu(created_menu):
    # Получаем ID созданного меню
    menu_id = created_menu

    # Добавляем подменю
    new_submenu_data = {"title": "New SubMenu",
                        "description": "Description of new submenu",
                        "menu_id": menu_id}
    response_submenu = client.post(f"/api/v1/menus/{menu_id}/"
                                   f"submenus", json=new_submenu_data)
    assert response_submenu.status_code == 201

    # Проверяем, что подменю успешно добавлено
    async with async_session_maker() as session:
        query = select(submenu).where(submenu.c.menu_id == menu_id)
        result = await session.execute(query)
        submenus = result.fetchall()
        assert len(submenus) == 1
        assert submenus[0].title == new_submenu_data["title"]
        assert submenus[0].description == new_submenu_data["description"]


async def test_update_submenu(created_menu, created_submenu):
    # Получаем ID созданного меню
    menu_id = created_menu

    # Получаем ID созданного подменю
    submenu_id = created_submenu

    # Обновляем данные подменю
    updated_submenu_data = {"title": "Updated SubMenu",
                            "description": "Updated"
                            " description of the submenu"}
    response_update = client.patch(f"/api/v1/menus/{menu_id}/"
                                   f"submenus/{submenu_id}",
                                   json=updated_submenu_data)
    assert response_update.status_code == 200

    # Проверяем, что данные подменю успешно обновлены
    response_get = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    updated_submenu = response_get.json()
    assert updated_submenu["title"] == updated_submenu_data["title"]
    assert updated_submenu["description"] == updated_submenu_data[
        "description"]


async def test_delete_submenu(created_menu, created_submenu):
    # Получаем ID созданного меню
    menu_id = created_menu

    # Получаем ID созданного подменю
    submenu_id = created_submenu

    # Удаляем подменю
    response_delete = client.delete(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response_delete.status_code == 200

    # Проверяем, что подменю успешно удалено
    async with async_session_maker() as session:
        query = select(submenu).where(submenu.c.id == submenu_id)
        result = await session.execute(query)
        assert result.fetchone() is None
