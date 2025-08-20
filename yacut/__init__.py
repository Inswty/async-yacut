from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

from settings import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- Swagger UI ---
SWAGGER_URL = '/docs'
API_URL = '/static/docs/openapi.yml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "My API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

from . import api_views, error_handlers, models, views
