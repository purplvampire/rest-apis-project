import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


# 取得所有店家資料
@app.get("/store") # http://127.0.0.1:5000/store 
def get_stores():
    # return "Hello World"
    return {"stores": list(stores.values())}   # 回傳JSON格式的清單,要將原本的字典取value並轉型成清單列表。

# 取得指定店家資料
@app.get("/store/<string:store_id>") # http://127.0.0.1:5000/store/<string:store_id>
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")  # 找不到可傳值

# 新增store資料
@app.post("/store") # http://127.0.0.1:5000/store 
def create_store():
    store_data = request.get_json()   # 取得JSON格式的POST資料
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")

    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")

    store_id = uuid.uuid4().hex # 生成獨特ID
    store = {**store_data, "id": store_id} # 建立新店家字典物件, **表示不定長度的key-value pairs. P3-9
    stores[store_id] = store    # 新增一筆店家清單,存進字典檔
    return store, 201           # 回傳JSON格式的清單,與Server的回應

# 刪除店家資料
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")

# 取得所有商品資料
@app.get("/item") # http://127.0.0.1:5000/item
def get_all_items():
    # return "Hello, world!"
    return {"items": list(items.values())}   # 回傳JSON格式的清單,要將原本的字典取value並轉型成清單列表。

# 取得指定品項資料
@app.get("/item/<string:item_id>") # http://127.0.0.1:5000/item/<string:item_id>
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")  # 找不到可傳值

# 新增品項資料
@app.post("/item")  # 指定店家目錄
def create_item():
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

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.")  # 找不到可傳值
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item           # 存進字典檔
    return item, 201                # 回傳上傳成功的資料與伺服器回應

# 刪除品項資料
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")

# 更新品項資料   
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.")

    try:
        item = items[item_id]
        item |= item_data       # item.update(item_data), 把字典item_data的键/值对更新到item里(P3-10)

        return item
    except KeyError:
        abort(404, message="Item not found.")

# 同步Docker目錄資料 docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api