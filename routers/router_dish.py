from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models import dish
from schemas import DishCreate, DishCreateResponse

router_dish = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Dish'],
)


@router_dish.post('/', response_model=DishCreateResponse,
                  status_code=status.HTTP_201_CREATED)
async def add_dish(submenu_id: UUID, add_dish: DishCreate,
                   session: AsyncSession = Depends(get_async_session)):
    existing_dish = (await session
                     .execute(select(dish)
                              .where(dish.c.submenu_id == submenu_id,
                                     dish.c.title == add_dish.title)))
    if existing_dish.fetchone():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Dish already exists")
    stmt = insert(dish).values(submenu_id=submenu_id,
                               **add_dish.model_dump()).returning(dish)
    result = await session.execute(stmt)
    created_dish = result.fetchone()
    await session.commit()
    return created_dish


@router_dish.delete('/{target_dish_id}')
async def delete_dish(target_dish_id: UUID,
                      session: AsyncSession = Depends(get_async_session)):
    stmt_check = select(dish).where(dish.c.id == target_dish_id)
    result_check = await session.execute(stmt_check)
    existing_dish = result_check.fetchone()

    if existing_dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Dish not found")

    stmt_delete = delete(dish).where(dish.c.id == target_dish_id)
    await session.execute(stmt_delete)
    await session.commit()

    return {'status': "done"}


@router_dish.get('/')
async def get_dishes(submenu_id: UUID,
                     session: AsyncSession = Depends(get_async_session)):
    stmt = select(dish).where(dish.c.submenu_id == submenu_id)
    result = await session.execute(stmt)
    dishes = result.fetchall()
    dishes_dict_list = [{'id': str(row.id),
                         'title': row.title,
                         'description': row.description,
                         'price': str(row.price)} for row in dishes]
    return dishes_dict_list


@router_dish.get('/{target_dish_id}', response_model=DishCreateResponse)
async def get_dish(target_dish_id: UUID,
                   submenu_id: UUID,
                   session: AsyncSession = Depends(get_async_session)):
    stmt = (select(dish)
            .where(dish.c.submenu_id == submenu_id,
                   dish.c.id == target_dish_id))
    result = await session.execute(stmt)
    target_dish = result.fetchone()

    if target_dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dish not found")

    return target_dish


@router_dish.patch('/{dish_id}')
async def update_dish(dish_id: UUID,
                      updated_dish: DishCreate,
                      session: AsyncSession = Depends(get_async_session)):
    stmt = (update(dish)
            .where(dish.c.id == dish_id)
            .values(**updated_dish.model_dump()))
    await session.execute(stmt)
    result = await session.execute(select(dish).where(dish.c.id == dish_id))
    updated_dish_info = result.fetchone()
    dish_dict = {
        'id': str(updated_dish_info.id),
        'title': updated_dish_info.title,
        'description': updated_dish_info.description,
        'price': str(updated_dish_info.price),
    }
    await session.commit()
    return JSONResponse(content=dish_dict, status_code=status.HTTP_200_OK)
