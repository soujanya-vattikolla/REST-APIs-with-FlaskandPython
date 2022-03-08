from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT

from Storedata_SQLDB.security import authenticate,identity

app = Flask(__name__)
app.secret_key = "secretkey"  # This key should be secret
api = Api(app)

jwt = JWT(app,authenticate,identity)  #/auth 

homeitems = [] # creating a list for storing the values

class HomeItem(Resource):
    parser = reqparse.RequestParser()     # to parse the request
    parser.add_argument('price',
                type=float,
                required=True,
                help="This field cannot be left blank"
        )


    def get(self,name):    # defining a get method
        #for homeitem in homeitems:
        #    if homeitem['name'] == name:
        #        return homeitem   # return the name of the items
        # instead of above code we can use lamda 

        homeitem = next(filter(lambda x:x['name'] == name,homeitems),None)   # if they are no items in the list, it will return None
        return {'homeitem':homeitem} ,200 if homeitem else 404   # status code 404, means error

    def post(self,name):            # defining a post method
        
        if next(filter(lambda x:x['name'] == name,homeitems),None):   # if the item is no None
            return {'message': "An item with name '{}' already present".format(name)}, 400 # 400 is a bad request

        data = HomeItem.parser.parse_args()
        
        homeitem = {'name': name,'price':data['price']}
        homeitems.append(homeitem)  # adding the items to the list
        return homeitem ,201        # status code 201 means that item has been updated

    def delete(self,name):
        global homeitems
        homeitems = list(filter(lambda x:x['name']!= name,homeitems))
        return {'message':'Item Deleted'}

    def put(self,name):         # update an existing item or add an item

        data = HomeItem.parser.parse_args()  # parse the arguments that come through the JSON payload and put the valid one in data

        homeitem = next(filter(lambda x:x['name'] == name, homeitems),None)
        if homeitem is None:
            homeitem = {'name':name, 'price':data['price']}
            homeitems.append(homeitem)
        else:
            homeitem.update(data)
        return homeitem


class HomeItemList(Resource):
    def get(self):
        return {'homeitems':homeitems}
     
api.add_resource(HomeItem, '/homeitem/<string:name>')  
api.add_resource(HomeItemList, '/homeitems')

app.run(port=5000, debug=True)