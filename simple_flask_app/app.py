from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'My store',
        'items':[
            {
                'name':'Item1',
                'price': 15.99
            },
            {
                'name':'Item2',
                'price': 4.77
            },
            {
                'name':'Item3',
                'price': 1.55
            }
        ]
    },
    {
        'name': 'Second Store',
        'items':[
            {
                'name':'Item4',
                'price': 9.54
            },
            {
                'name':'Item5',
                'price': 7.56
            },
            {
                'name':'Item6',
                'price': 5.51
            }
        ]
    }
]

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/store', methods=['POST'])
def create_store():
    request_data=request.get_json()
    new_store={
        'name': request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return jsonify(new_store)

@app.route('/store/<string:name>')
def get_store(name):
    # iterate over the stores
    # if store name matches, return it
    # if not matches, return an error message
    for store in stores:
        if store['name']== name:
            return jsonify(store)

    return jsonify({'message': '{} store not found'.format(name)})

@app.route('/store')
def get_stores():
    return jsonify({'stores':stores})

@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name']==name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)

    return jsonify({'message': '{} store not found'.format(name)})

@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    pass


app.run(port=5000)