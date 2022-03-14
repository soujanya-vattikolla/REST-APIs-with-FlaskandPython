import sqlite3
from db import db

class StoreModel(db.Model):

    __tablename__ = 'stores'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
   
    items = db.relationship('ItemModel',lazy='dynamic')     # many to one relationship, many items related to one store

    def __init__(self,name):
        self.name = name
 

    def json(self):
        return {'name':self.name,'items':[item.json() for item in self.items.all()]}


    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()  # which is similar to "SELECT * FROM homeitems WHERE name=name LIMIT 1, returns the first row

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)    # session means collection of objects which write to the DB
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()