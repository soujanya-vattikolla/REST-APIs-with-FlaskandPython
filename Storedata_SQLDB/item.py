import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class HomeItem(Resource):
    parser = reqparse.RequestParser()     # to parse the request
    parser.add_argument('price',
                type=float,
                required=True,
                help="This field cannot be left blank"
        )


    def get(self,name):    # defining a get method
        
        homeitem = self.find_by_name(name)
        if homeitem:
            return homeitem
        return {'message': 'Item not found'},404

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM homeitems WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row: # if row exists
            return {'homeitem': {'name': row[0], 'price': row[1]}}
        


    def post(self,name):            # defining a post method
        
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already present".format(name)}, 400 # 400 is a bad request

        data = HomeItem.parser.parse_args()
        
        homeitem = {'name': name,'price':data['price']}

        try:
            self.insert(homeitem)
        except:
            return {"message": "An error occured while inserting the item."},500 # internal server error

        return homeitem,201

    
    @classmethod

    def insert(cls,homeitem):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO homeitems VALUES (?,?)"
        cursor.execute(query, (homeitem['name'],homeitem['price']))

        connection.commit()
        connection.close()



    def delete(self,name):
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM homeitems WHERE name=?"
        cursor.execute(query,(name,))

        connection.commit()
        connection.close()

        return {'message':'Item Deleted'}


    def put(self,name):         # update an existing item or add an item

        data = HomeItem.parser.parse_args()  # parse the arguments that come through the JSON payload and put the valid one in data

        homeitem = self.find_by_name(name)
        updated_homeitem = {'name':name, 'price':data['price']}

        if homeitem is None:
            try:
                 self.insert(updated_homeitem)
            except:
                return {"message": "An error occured while inserting the item."},500 # internal server error
        else:
            try:
                self.update(updated_homeitem)
            except:
                return {"message": "An error occured while updating the item."},500 # internal server error
        return updated_homeitem

    @classmethod
    def update(cls,homeitem):
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE homeitems SET price=? WHERE name=?"
        cursor.execute(query,(homeitem['price'],homeitem['name']))

        connection.commit()
        connection.close()

        return {'message':'Item Deleted'}


class HomeItemList(Resource):
    def get(self):
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM homeitems"
        result = cursor.execute(query)
        homeitems = []
        for row in result:
            homeitems.append({'name':row[0],'price':row[1]})

        connection.close()

        return {'homeitems':homeitems}
        

