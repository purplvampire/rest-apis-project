from marshmallow import Schema, fields
# 用來檢查JSON格式的型別

class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

# 與關聯欄位相關的型別另外建立繼承型別處理，一對多的子，多對多的父
class ItemSchema(PlainItemSchema):  
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)   # 說明屬性是PlainStoreSchema的型別
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True) # 多對多的父

# 與關聯欄位相關的型別另外建立繼承型別處理，一對多的父
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainStoreSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

# 與關聯欄位相關的型別另外建立繼承型別處理，一對多的子
class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)               # 一對多的子
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)   # 多對多的父

# 多對多關聯資料表，多對多的子
class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True) # 只能Return
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) # 只能載入不能回傳

class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)