from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from random import randint

# create an instance in the flask frame
app = Flask(__name__)

# SQLite datebase link
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///example.db'
app.config['SECRET_KEY'] = os.urandom(10)

# connect app with SQLAchemy(SQLite)
db = SQLAlchemy(app)

# create data list and column
class DBFrame(db.Model):
    __tablename__ = "tablename"
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(60))
    grade       = db.Column(db.Integer)

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
        
    def __repr__(self):
        return '< {} , {} , {}  >'.format(self.id,
                                        self.name,
                                        self.grade)
def add_data():
    # You can change that what kind of database you need
    for x in range(1,5):
        item = DBFrame('John',randint(60,100))
        db.session.add(item)
    for x in range(1,5):
        item = DBFrame('Mary',randint(60,100))
        db.session.add(item)
    for x in range(1,5):
        item = DBFrame('Edgar',randint(60,100))
        db.session.add(item)
    
    # database commit is a important step
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        add_data()