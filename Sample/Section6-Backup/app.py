from flask import Flask
from flask_smorest import Api

from db import db
import models       # 要在SQLAlchemy實作之前匯入models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"   # 從環境變數取得連線帳密
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # 會降低速度
    app.config["PROPAGATE_EXCEPTIONS"] = True
    
    db.init_app(app)

    with app.app_context():
        db.create_all()     # 從models中找到要建立的Table

    # 建立API網站
    api = Api(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app

# 同步Docker目錄資料 docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api