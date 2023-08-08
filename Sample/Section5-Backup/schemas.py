from marshmallow import Schema, fields
# 用來檢查JSON格式的型別

class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

# 與關聯欄位相關的型別另外建立繼承型別處理，用lambda餵入class並回傳值表示關聯性。
class ItemSchema(PlainItemSchema):  
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(lambda: StoreSchema(), dump_only=True)   # 說明屬性是PlainStoreSchema的型別

# 與關聯欄位相關的型別另外建立繼承型別處理
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(lambda: ItemSchema()), dump_only=True)