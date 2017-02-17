from flask_restful import Resource
from flask_jwt import jwt_required
from flask_restful import reqparse
from flask import jsonify

from model.store import StoreModel

class Stores(Resource):

    def get(self):
        return jsonify([store.json() for store in StoreModel.list_all_stores()])


class Store(Resource):

    def get(self, name):
        store = StoreModel.find(name)
        if store:
            return store.json()

        return {"message": "Store not found"}, 404

    def post(self, name):
        if StoreModel.find(name):
            return {"message": "Store '{}' already exists".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save()
        except:
            return {"message": "An error occurred while creating the store"}, 500

        return store.json(), 200

    def delete(self, name):
        store = StoreModel.find(name)
        if store:
            store.delete()

        return {"message": "Store deleted"}