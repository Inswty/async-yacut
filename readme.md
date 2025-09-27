## YaCut — сервис сокращения ссылок

YaCut — это сервис для сокращения длинных URL и хранения их в базе данных.  
Приложение позволяет создавать короткие ссылки, а также асинхронно загружать файлы и получать для них короткие адреса.

### Технологический стек:
- Python 3.12
- Flask
- Flask-WTF
- SQLAlchemy
- SQLite
- HTML
- CSS
- Jinja2
- Bootstrap
- Swagger

### Как запустить проект Yacut:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Inswty/async-yacut.git
cd yacut

```
Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/Scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создать в директории проекта файл .env с четыремя переменными окружения:

```
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key
DB=sqlite:///db.sqlite3
```

Создать базу данных и применить миграции:

```
flask db upgrade
```

Запустить проект:

```
flask run
```

Приложение доступно по адресу:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)


Примеры запросов к API, варианты ответов и ошибок приведены в спецификации openapi.yml  
Для работы с документом перейдите по адресу:  
[http://localhost:5000/docs/](http://localhost:5000/docs/)



## Автор:
Проект разработан 
[Павел Куличенко](https://github.com/Inswty)
