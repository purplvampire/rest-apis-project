# from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError  # exception

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")

# 裝飾器Decorating
@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
            
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted successfully."}

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)    # 驗證來源資料
    @blp.response(200, ItemSchema)      # 回應結果(注意裝飾器順序)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)   # 若item=None,則以item_id新建檔案

        db.session.add(item)
        db.session.commit()

        return item

@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))   # 以清單形式回應結果
    def get(self):
        # 回傳JSON格式的清單,要將原本的字典取value並轉型成清單列表。
        return ItemModel.query.all()       # 將回傳值拋到裝飾器response

    @jwt_required(fresh=True)       # 要求須更新的憑證
    @blp.arguments(ItemSchema)      # 驗證來源資料
    @blp.response(201, ItemSchema)  # 回應結果(注意裝飾器順序)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()     # save to disk
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item               # 回傳上傳成功的資料與伺服器回應