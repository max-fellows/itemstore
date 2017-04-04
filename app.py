import os

from flask import Flask
from flask import request
from flask_restful import Resource
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
from flask_cors import cross_origin

from security.security import AuthenticationService
from resource.user import User
from resource.item import Items
from resource.item import Item
from resource.store import Stores
from resource.store import Store

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
CORS(app)
api = Api(app)

auth = AuthenticationService()
app.secret_key = "foo"
jwt = JWT(app, auth.authenticate, auth.identity) # /auth

api.add_resource(Items, "/items")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(User, "/register")
api.add_resource(Stores, "/stores")
api.add_resource(Store, "/store/<string:name>")
