from flask import Flask, request


app = Flask(__name__)

stores = {[
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
            
        ]
        
    }
]}

# 取得所有店家資料
@app.get("/store") # http://127.0.0.1:5000/store 
def get_stores():
    return {"stores": stores}   # 回傳JSON格式的清單

# 取得指定店家資料
@app.get("/store/<string:name>") # http://127.0.0.1:5000/store 
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404  # 找不到可傳值

# 取得指定店家item資料
@app.get("/store/<string:name>/item") # http://127.0.0.1:5000/store
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404  # 找不到可傳值

# 新增store資料
@app.post("/store") # http://127.0.0.1:5000/store 
def create_store():
    request_data = request.get_json()   # 取得JSON格式的POST資料
    new_store = {"name": request_data["name"], "items": []} # 建立新店家字典物件
    stores.append(new_store)    # 新增一筆店家清單
    return new_store, 201       # 回傳JSON格式的清單,與Server的回應

# 新增item資料
@app.post("/store/<string:name>/item")  # 指定店家目錄
def create_item(name):
    request_data = request.get_json()   # 取得JSON格式的POST資料
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201                # 回傳上傳成功的資料與伺服器回應
    return {"message": "Store not found"}, 404  # 找不到可傳值
