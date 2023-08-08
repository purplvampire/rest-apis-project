from marshmallow import Schema, fields


class ItemSchema(Schema):
    # Here not only we need to validate data exists,
    # But also what type of data. Price should be a float,
    # for example.
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    # There's more validation to do here!
    # Like making sure price is a number, and also both tiems are optional
    # Difficult to do with an if statement...
    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)