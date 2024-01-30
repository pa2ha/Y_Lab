## Клонировать проект
```
git clone git@github.com:pa2ha/Y_Lab.git
cd Y_Lab
```
# Как запустить Тесты!

Cоздать файл .env в корне проекта и заполнить его
## Если запускаем для тестов, то просто копируем
```
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=menu
POSTGRES_USER=fastapi
POSTGRES_PASSWORD=mypass

DB_HOST_TEST=db
DB_PORT_TEST=5432
DB_NAME_TEST=menu
DB_USER_TEST=fastapi
DB_PASS_TEST=mypass
```
## Если запускаем API, то оставляем без тестов
```
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=menu
POSTGRES_USER=fastapi
POSTGRES_PASSWORD=mypass
```


Находясь в корнейвой папке проекта выполнить:


для запуска контейнеров
```
docker-compose up
```
### В другом терминале после поднятия контейнеров



для запуска тестов
```
docker-compose exec api-test pytest

```
для запуска сценария из тестов
```
docker-compose exec api-test pytest tests/script.py 
```

### Пример сложного запроса(пункт 3)
```
можно увидеть в routers/router_menu.py/get_menus()
```
# Как запустить проект
Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```



Запустить миграции
```
alembic upgrade ca4c86d31d20
```
Запустить uvicorn

```
uvicorn main:app --reload
```
Готово, можно проверять проект
