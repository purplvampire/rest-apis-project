import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores
from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operations on stores")

# 抽象型別=protocol
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")  # 找不到可傳值
    # 這個沒裝飾器
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")
        
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))  # 以清單形式回應結果
    def get(self):
        # 回傳JSON格式的清單,要將原本的字典取value並轉型成清單列表。
        return stores.values()
    
    @blp.arguments(StoreSchema)     # 驗證來源資料
    @blp.response(200, StoreSchema) # 回應結果
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex # 生成獨特ID
        store = {**store_data, "id": store_id} # 建立新店家字典物件, **表示不定長度的key-value pairs. P3-9
        stores[store_id] = store    # 新增一筆店家清單,存進字典檔

        return store                # 回傳值給response裝飾器
