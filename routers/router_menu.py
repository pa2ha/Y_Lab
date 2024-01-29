from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import and_, delete, distinct, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models import dish, menu, submenu
from schemas import MenuCreate, MenuCreateResponse, TargerMenuResponse

router_menu = APIRouter(
    prefix='/api/v1/menus',
    tags=['Menu'],
)


@router_menu.post('/',
                  response_model=MenuCreateResponse,
                  status_code=status.HTTP_201_CREATED)
async def add_menu(add_menu: MenuCreate,
                   session: AsyncSession = Depends(get_async_session)):
    stmt = insert(menu).values(**add_menu.model_dump()).returning(menu)
    result = await session.execute(stmt)
    added_menu = result.fetchone()
    await session.commit()
    return added_menu


@router_menu.delete('/{target_menu_id}')
async def delete_menu(target_menu_id: UUID,
                      session: AsyncSession = Depends(get_async_session)):
    # Проверяем, существует ли меню с указанным ID
    stmt_check = select(menu).where(menu.c.id == target_menu_id)
    result_check = await session.execute(stmt_check)
    if result_check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found")
    stmt_delete = delete(menu).where(menu.c.id == target_menu_id)
    await session.execute(stmt_delete)
    await session.commit()

    return {'status': "done"}


@router_menu.get('/', response_model=list[MenuCreate])
async def get_menus(session: AsyncSession = Depends(get_async_session)):
    stmt = select(menu.c.title, menu.c.description)
    result = await session.execute(stmt)
    list_of_menus = result.all()
    return list_of_menus


@router_menu.get('/{target_menu_id}', response_model=TargerMenuResponse)
async def get_menu(target_menu_id: UUID,
                   session: AsyncSession = Depends(get_async_session)):
    # Подзапрос для количества подменю
    stmt = (
            select(
                menu.c.id,
                menu.c.title,
                menu.c.description,
                func.count(distinct(submenu.c.id)).label('submenus_count'),
                func.count(dish.c.id).label('dishes_count'))
            .select_from(menu.outerjoin(submenu,
                                        and_(submenu.c.menu_id == menu.c.id)).outerjoin(dish))
            .where(menu.c.id == target_menu_id)
            .group_by(menu.c.id))
    result = await session.execute(stmt)
    menu_info = result.first()
    if menu_info:
        return menu_info
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="menu not found")


@router_menu.patch('/{menu_id}')
async def update_menu(menu_id: UUID, updated_menu: MenuCreate,
                      session: AsyncSession = Depends(get_async_session)):
    stmt = (update(menu)
            .where(menu.c.id == menu_id)
            .values(**updated_menu.model_dump()))
    await session.execute(stmt)
    menu_dict = {
        'id': str(menu_id),  # Преобразуем UUID в строку
        'title': updated_menu.title,
        'description': updated_menu.description
    }
    await session.commit()
    # Возвращаем JSONResponse с данными обновленного меню
    return JSONResponse(content=menu_dict, status_code=status.HTTP_200_OK)
