# Как запустить проект
Клонировать проект
```
git clone git@github.com:pa2ha/Y_Lab.git
cd Y_Lab
```
Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
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
