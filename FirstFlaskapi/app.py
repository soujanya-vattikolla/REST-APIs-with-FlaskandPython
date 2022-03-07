from flask import Flask, jsonify, request,render_template
# here Flask is a class, flask is a package

app = Flask(__name__)


bookstores = [{
       'name':'Text Books',
       'items':[{ 'name':'Hindi book', 'cost':50 }]
    }]

@app.route('/') # for ex: 'http://www.goole.com/', which means a home page of the application
def home():
    return render_template('index.html')


# POST /bookstore data: {name:}
@app.route('/bookstore',methods=['POST'])
def create_bookstore():
    request_data = request.get_json()   # browser sends requests to create a store and name of the store
    new_bookstore = {
        'name':request_data['name'],
        'items':[] }
    bookstores.append(new_bookstore)
    return jsonify(new_bookstore)


# GET /bookstore/<string:name>
@app.route('/bookstore/<string:name>')  # 'http://127.0.0.1:5000/bookstore/some_name'
def get_bookstore(name):
    # Iterate over bookstores
    for bookstore in bookstores:
    # if the bookstore name matches, return it
       if bookstore['name'] == name:
           return jsonify(bookstore)
    # if it is not matching, return an error message
    return jsonify({'message':'bookstore not found'})




# GET /bookstore
@app.route('/bookstore')
def get_bookstores():
    return jsonify({'bookstores':bookstores})


# POST /bookstore/<string:name>/item {name:, cost:}
@app.route('/bookstore/<string:name>/item',methods=['POST'])
def create_item_in_bookstore(name):
    request_data = request.get_json()
    for bookstore in bookstores:
        if bookstore['name'] == name:
            new_item = {
                'name':request_data['name'],
                'cost':request_data['cost']  }
            bookstore['items'].append(new_item)
            return jsonify(bookstore)
    return jsonify({'message':'bookstore not found'})


# GET /store/<string:name>/item
@app.route('/bookstore/<string:name>/item')   # 'http://127.0.0.1:5000/bookstore/some_name'
def get_item_in_bookstore(name):
    for bookstore in bookstores:
        if bookstore['name'] == name:
            return jsonify({'items':bookstore['items']})
    return jsonify({'message':'bookstore not found'})

app.run(port=5000) # to run the app, 5000 is the default


