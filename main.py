from fastapi import FastAPI

from routers.router_dish import router_dish
from routers.router_menu import router_menu
from routers.router_submenu import router_submenu

app = FastAPI(
    tittle="Menu APP"
)

app.include_router(router_menu)
app.include_router(router_submenu)
app.include_router(router_dish)
