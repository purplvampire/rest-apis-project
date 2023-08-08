from db import db


class ItemTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    # 多對多關聯
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id   = db.Column(db.Integer, db.ForeignKey("tags.id"))