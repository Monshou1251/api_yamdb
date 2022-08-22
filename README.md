
## Api_yamdb
***
### Описание проекта:

Api_yamdb главный конкурент IMDB.

***
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/cooper30/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Загрузить тестовые данные:

```
python3 manage.py loaddata
```
***
## Tech
Yatube API uses a number of open source projects to work properly:

- [Python] - a programming language that lets you work quickly and integrate systems more effectively.
- [Django] - a high-level Python web framework
***
## Authors
- [Никита Звеков](https://github.com/cooper30)
- [Ирина Смирнова](https://github.com/IrinaSMR)
- [Григорий Юрченко](https://github.com/Monshou1251)

***
## Requests examples
Samples of how this API works could be found through Redoc - http://127.0.0.1:8000/redoc/

Comments GET request:
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```sh
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```

Comments POST request:
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```sh
{
  "text": "string"
}
```
Response samples:
```sh
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
