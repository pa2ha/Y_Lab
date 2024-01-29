from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models import dish, submenu
from schemas import SubMenuCreate, SubMenuCreateResponse, TargetSubMenuResponse

router_submenu = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=['SubMenu'],
)


@router_submenu.post('/', response_model=SubMenuCreateResponse,
                     status_code=status.HTTP_201_CREATED)
async def add_submenu(menu_id: UUID, add_submenu: SubMenuCreate,
                      session: AsyncSession = Depends(get_async_session)):

    existing_submenu = (await session.
                        execute(select(submenu).
                                where(submenu.c.menu_id == menu_id,
                                      submenu.c.title == add_submenu.title)))
    if existing_submenu.fetchone():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Submenu already exists")

    stmt = (insert(submenu).
            values(menu_id=menu_id, **add_submenu.model_dump()).returning(submenu))
    result = await session.execute(stmt)
    created_submenu = result.fetchone()
    await session.commit()

    return created_submenu


@router_submenu.delete('/{target_submenu_id}')
async def delete_submenu(target_submenu_id: UUID,
                         session: AsyncSession = Depends(get_async_session)):
    stmt_check = select(submenu).where(submenu.c.id == target_submenu_id)
    result_check = await session.execute(stmt_check)
    existing_submenu = result_check.fetchone()

    if existing_submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found")

    stmt_delete = delete(submenu).where(submenu.c.id == target_submenu_id)
    await session.execute(stmt_delete)
    await session.commit()

    return {'status': "done"}


@router_submenu.get('/', response_model=list[SubMenuCreateResponse])
async def get_submenus(menu_id: UUID,
                       session: AsyncSession = Depends(get_async_session)):
    stmt = select(submenu).where(submenu.c.menu_id == menu_id)
    result = await session.execute(stmt)
    submenus = result.fetchall()
    return submenus


@router_submenu.get('/{target_submenu_id}',
                    response_model=TargetSubMenuResponse)
async def get_submenu(target_submenu_id: UUID,
                      menu_id: UUID,
                      session: AsyncSession = Depends(get_async_session)):
    stmt = (
        select(
            submenu,
            func.count(dish.c.id).label('dishes_count')
        )
        .select_from(submenu.outerjoin(dish))
        .where(submenu.c.menu_id == menu_id, submenu.c.id == target_submenu_id)
        .group_by(submenu.c.id, submenu.c.title, submenu.c.description)
    )

    result = await session.execute(stmt)
    menu_info = result.first()
    if menu_info:
        return menu_info
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="submenu not found")


@router_submenu.patch('/{submenu_id}')
async def update_submenu(submenu_id: UUID,
                         updated_submenu: SubMenuCreate,
                         session: AsyncSession = Depends(get_async_session)):
    stmt = (update(submenu)
            .where(submenu.c.id == submenu_id)
            .values(**updated_submenu.model_dump()))
    await session.execute(stmt)
    submenu_dict = {
        'id': str(submenu_id),
        'title': updated_submenu.title,
        'description': updated_submenu.description
    }
    await session.commit()
    return JSONResponse(content=submenu_dict, status_code=status.HTTP_200_OK)
