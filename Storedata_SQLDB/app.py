from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from Storedata_SQLDB.security import authenticate,identity
from Storedata_SQLDB.user import UserRegister
from Storedata_SQLDB.item import HomeItem,HomeItemList

app = Flask(__name__)
app.secret_key = "secretkey"  # This key should be secret
api = Api(app)

jwt = JWT(app,authenticate,identity)  #/auth 

     
api.add_resource(HomeItem, '/homeitem/<string:name>')  
api.add_resource(HomeItemList, '/homeitems')

api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)