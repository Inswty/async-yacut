# YaCut — сервис сокращения ссылок

YaCut — это сервис для сокращения длинных URL и хранения их в базе данных.  
Приложение позволяет создавать короткие ссылки, а также загружать файлы и получать для них короткие адреса.

### Как запустить проект Yacut:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
https://github.com/Inswty/async-yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

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

```
Приложение доступно по адресу:  
http://127.0.0.1:5000/

```

```
Примеры запросов к API, варианты ответов и ошибок приведены в спецификации openapi.yml;
Для работы с документом воспользуйтесь онлайн-редактором Swagger Editor.
https://editor.swagger.io/

```

```
Технологический стек:
- Python 3.12 + Flask
- Flask-WTF
- SQLAlchemy
- HTML
- CSS
- SQLite
- Jinja2
- Bootstrap
```

Автор:
Проект разработан [Павел Куличенко]
GitHub: https://github.com/Inswty