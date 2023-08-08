import secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from db import db
from blocklist import BLOCKLIST
import models       # 要在SQLAlchemy實作之前匯入models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag  import blp as TagBlueprint
from resources.user import blp as UserBlueprint

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

    # 移轉DB
    migrate = Migrate(app, db)

    # 建立JWT Token "secrets.SystemRandom().getrandbits(128)"
    app.config["JWT_SECRET_KEY"] = "Jason"
    jwt = JWTManager(app)

    # 檢查token是否被放入封鎖清單中 
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token has been revoked.",
                    "error": "token_revoked"
                }
            ),
            401,
        )

    # 要求傳遞的是須更新的憑證
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required"
                }
            ),
            401,
        )

    # 驗證jwt token
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Look in the database and see whether the user is an admin.
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    # jwt錯誤處理
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "message": "The token has expired.", 
                    "error": "token_expired"
                }
            ),
            401,
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Signature verification failed.", 
                    "error": "invalid_token"
                }
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.", 
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # 透過Migrate不再需要本地建立DB
    # with app.app_context():
    #     db.create_all()     # 從models中找到要建立的Table

    # 建立API文件查詢網站
    api = Api(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app

# 更新容器套件資料：docker build -t rest-apis-flask-python .
# 同步容器目錄資料 docker run -dp 5005:5000 -w /app -v "$(pwd):/app" rest-apis-flask-python