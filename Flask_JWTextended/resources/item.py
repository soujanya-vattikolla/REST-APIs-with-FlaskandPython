import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()     # to parse the request
    parser.add_argument('price',
                type=float,
                required=True,
                help="This field cannot be left blank"
        )
    parser.add_argument('store_id',
                type=int,
                required=True,
                help="Every item needs a store id."
        )

    @jwt_required()
    def get(self,name):    # defining a get method
        
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'},404

    def post(self,name):            # defining a post method
        
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already present".format(name)}, 400 # 400 is a bad request

        data = Item.parser.parse_args()
        
        item = ItemModel(name , **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured while inserting the item."},500 # internal server error

        return item.json(),201

    def delete(self,name):
        
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404
  

    def put(self,name):         # update an existing item or add an item

        data = Item.parser.parse_args()  # parse the arguments that come through the JSON payload and put the valid one in data

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()   

        return item.json()


class ItemList(Resource):
    def get(self):

        return {'items': [x.json() for x in ItemModel.find_all()]}
        

