import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items
from schemas import ItemSchema

blp = Blueprint("Items", __name__, description="Operations on items")

# 裝飾器Decorating
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")  # 找不到可傳值

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")


    @blp.arguments(ItemUpdateSchema)    # 驗證來源資料
    @blp.response(200, ItemSchema)      # 回應結果(注意裝飾器順序)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data       # item.update(item_data), 把字典item_data的键/值对更新到item里(P3-10)
            
            return item
        except KeyError:
            abort(404, message="Item not found.")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))   # 以清單形式回應結果
    def get(self):
        # 回傳JSON格式的清單,要將原本的字典取value並轉型成清單列表。
        return items.values()       # 將回傳值拋到裝飾器response

    @blp.arguments(ItemSchema)      # 驗證來源資料
    @blp.response(201, ItemSchema)  # 回應結果(注意裝飾器順序)
    def post(self, item_data):
        for item in items.values():
            if (
                item_data["name"] == item["name"] and
                item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"Item already exists.")
        
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item           # 存進字典檔

        return item               # 回傳上傳成功的資料與伺服器回應