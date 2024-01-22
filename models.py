import uuid

from sqlalchemy import Column, ForeignKey, MetaData, Numeric, String, Table
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

# Определение таблицы menu
menu = Table(
    "menu",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String, index=True),
    Column("description", String),
)

# Определение таблицы submenu
submenu = Table(
    "submenu",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String, index=True),
    Column("description", String),
    Column("menu_id", UUID(as_uuid=True), ForeignKey("menu.id", ondelete="CASCADE")),
)

# Определение таблицы dish
dish = Table(
    "dish",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String, index=True),
    Column("description", String),
    Column("price", Numeric(precision=10, scale=2)),
    Column("submenu_id", UUID(as_uuid=True), ForeignKey("submenu.id", ondelete="CASCADE")),
)
