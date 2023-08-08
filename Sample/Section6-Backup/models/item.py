from db import db


class ItemModel(db.Model):
    __tablename__ = 'items' # Create or Modify Tablename

    id = db.Column(db.Integer, primary_key=True)    # Set Primary Column
    name = db.Column(db.String(80), unique=True, nullable=False) # Set name Column
    price = db.Column(db.Float(precision=2), unique=False, nullable=False) # Set Price Column
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False) # Set Store Column(Foreign Key)
    store = db.relationship("StoreModel", back_populates="items")   # 與StoreModel.items建立關聯

if __name__ == "__main__":
    x = ItemModel.query.all()
    print(x)
