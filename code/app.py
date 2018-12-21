from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
api = Api(app)
app.secret_key="secret-world"

jwt = JWT(app, authenticate, identity)


api.add_resource(Item, "/item/<string:name>") # http://127.0.0.1:5000/
api.add_resource(ItemList, "/items/") # http://127.0.0.1:5000/
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)



