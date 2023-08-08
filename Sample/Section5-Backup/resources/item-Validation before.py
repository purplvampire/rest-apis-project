import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items

blp = Blueprint("Items", __name__, description="Operations on items")

# 抽象型別=protocol
@blp.route("/item/<string:item_id>")
class Item(MethodView):
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

    def put(self, item_id):
        item_data = request.get_json()
        # There's more validation to do here!
        # Like making sure price is a number, and also both tiems are optional
        # Difficult to do with an if statement...
        if "price" not in item_data or "name" not in item_data:
            abort(
                400, 
                message="Bad request. Ensure 'price', and 'name' are included in the JSON payload."
            )
        try:
            item = items[item_id]
            item |= item_data       # item.update(item_data), 把字典item_data的键/值对更新到item里(P3-10)
            return item
        except KeyError:
            abort(404, message="Item not found.")

@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        # 回傳JSON格式的清單,要將原本的字典取value並轉型成清單列表。
        return {"items": list(items.values())}   

    def post(self):
        item_data = request.get_json()      # 取得JSON格式的POST資料
        # Here not only we need to validate data exists,
        # But also what type of data. Price should be a float,
        # for example.
        if (
            "price" not in item_data or 
            "store_id" not in item_data or 
            "name" not in item_data
        ):
            abort(
                400, 
                message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload."
            )

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