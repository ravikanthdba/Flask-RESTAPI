from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float, required=True, help="The price field is mandatory")

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items where name = ?"
        cursor.execute(query, (name,))
        item = cursor.fetchone()
        connection.close()
        return {'item': item}, 200 if item else 404



    def post(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT name FROM items where name = ?"
        cursor.execute(query, (name,))
        item = cursor.fetchone()
        if item:
            return {"message": "An item with name {} already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        new_item = {
            'name': name,
            'price': data['price']
        }
        query = "INSERT INTO items values(NULL, ?, ?)"
        cursor.execute(query, (name, data['price']))
        connection.commit()
        connection.close()
        return new_item, 201


    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items where name = ?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {"message": "Item {} has been deleted".format(name)}


    def put(self, name):

        data = Item.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name = ?"
        cursor.execute(query, (name,))
        record = cursor.fetchone()
        if record:
            query = "UPDATE items SET price = ? WHERE name = ?"
            cursor.execute(query, (data['price'], name))
            connection.commit()
            return {"message": "Item {} has been updated.".format(name)}
        else:
            query = "INSERT INTO items VALUES (NULL, ?, ?)"
            cursor.execute(query, (name, data['price'],))
            connection.commit()
            return {"message": "Item {} has been inserted".format(name)}
        connection.close()


class ItemList(Resource):
    def get(self):
        items = []
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT id, name, price FROM items"
        cursor.execute(query)
        storeItems = cursor.fetchall()
        items = []
        for storeItem in storeItems:
            item = {"id": storeItem[0], "name": storeItem[1], "price": storeItem[2]}
            items.append(item)
        connection.close()
        return {'ItemsList': items}