import sqlite3
from flask import Flask
from flask import request
from flask_restful import Resource
from flask_restful import Api
from flask_jwt import JWT

from security.security import AuthenticationService
from resource.user import User
from resource.item import Items
from resource.item import Item
from resource.store import Stores
from resource.store import Store

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../data.db"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

auth = AuthenticationService()
app.secret_key = "foo"
jwt = JWT(app, auth.authenticate, auth.identity) # /auth

api.add_resource(Items, "/items")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(User, "/register")
api.add_resource(Stores, "/stores")
api.add_resource(Store, "/store/<string:name>")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=8080, debug=True)
