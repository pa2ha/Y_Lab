## Клонировать проект
```
git clone git@github.com:pa2ha/Y_Lab.git
cd Y_Lab
```
# Как запустить Тесты!
Находясь в корнейвой папке проекта выполнить:
```
docker-compose up -для запуска контейнеров
```
### В другом терминале после поднятия контейнеров
```
docker-compose exec api-test pytest - для запуска тестов
docker-compose exec api-test pytest tests/script.py - для запуска сценария из тестов
```
### Пример сложного запроса(пункт 3)
можно увидеть в routers/router_menu.py/get_menus()

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

Cоздать файл .env и заполнить его

```
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASS=
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
