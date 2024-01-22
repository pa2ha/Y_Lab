from decimal import Decimal

from pydantic import UUID4, BaseModel


class MenuCreate(BaseModel):
    title: str
    description: str


class MenuCreateResponse(BaseModel):
    id: UUID4
    title: str
    description: str


class TargerMenuResponse(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class SubMenuCreateResponse(BaseModel):
    id: UUID4
    title: str
    description: str


class SubMenuCreate(BaseModel):
    title: str
    description: str


class TargetSubMenuResponse(BaseModel):
    id: UUID4
    title: str
    description: str
    dishes_count: int


class DishCreate(BaseModel):
    title: str
    description: str
    price: Decimal


class DishCreateResponse(BaseModel):
    id: UUID4
    title: str
    description: str
    price: Decimal
