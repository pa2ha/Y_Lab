from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models import dish, menu, submenu
from schemas import MenuCreate

router_menu = APIRouter(
    prefix='/api/v1/menus'
)


@router_menu.post('/')
async def addMenu(
    add_menu: MenuCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(menu).values(**add_menu.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': "done"}


@router_menu.delete('/')
async def deleteMenu(menu_id: int, session: AsyncSession = Depends(get_async_session)):
    delete_stmt = delete(menu).where(menu.c.id == menu_id)

    await session.execute(delete_stmt)
    await session.commit()

    return {'status': "done"}


@router_menu.get('/')
async def get_menus(session: AsyncSession = Depends(get_async_session)):
    stmt = select(menu)
    result = await session.execute(stmt)
    menus = result.fetchall()
    menus_dict_list = [row._asdict() for row in menus]
    
    return menus_dict_list


@router_menu.get('/{target_menu_id}')
async def get_menu(target_menu_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = select(menu).where(menu.c.id == target_menu_id)
    result = await session.execute(stmt)
    target_menu = result.fetchone()

    if target_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    target_menu_dict = target_menu._asdict()
    return target_menu_dict


@router_menu.patch('/{menu_id}')
async def update_menu(
    menu_id: int, updated_menu: MenuCreate, session: AsyncSession = Depends(
        get_async_session)):
    stmt = update(menu).where(menu.c.id == menu_id).values(
        **updated_menu.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'done'}