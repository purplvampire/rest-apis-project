from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # 與ItemModel.store建立關聯, 且刪除store將同步刪除所有items,cascade只能用於父物件。
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")   
    # lazy="dynamic"在實際查詢資料時，相關的資料不會立即載入，而是根據需要進行動態載入。
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")  # lazy="dynamic"在實際查詢資料時，相關的資料不會立即載入，而是根據需要進行動態載入。

