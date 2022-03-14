from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store_resource import Store,StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # the sqlalchemy is the database URI that should be used for the connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "secretkey"  # This key should be secret
api = Api(app)

@app.before_first_request
def create_tables():             #creating tables
    db.create_all()

jwt = JWT(app,authenticate,identity)  #/auth 

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')  
api.add_resource(ItemList, '/items')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister,'/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)