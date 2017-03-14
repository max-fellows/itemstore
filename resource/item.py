from flask_restful import Resource
from flask_jwt import jwt_required
from flask_restful import reqparse
from flask import jsonify

from model.item import ItemModel

class Items(Resource):

    def get(self):
        return jsonify([item.json() for item in ItemModel.list_all_items()])


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="This field cannot be left blank")

    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find(name)
        return ({"item": item.json()}, 200) if item \
            else ({"message": "Item {} not found".format(name)}, 404)

    def post(self, name):
        if ItemModel.find(name):
            return {"message": "Item {} already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save()
            return item.json()
        except:
            return {"message": "An error occurred creating the item"}, 500

    def delete(self, name):
        item = ItemModel.find(name)
        if not item:
            return {"item": None}, 404
        
        try:
            item.delete()
        except:
            return {"message": "An error occurred deleting the item"}, 500

        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find(name)
        if not item:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]

        try:
            item.save()
            return item.json()
        except:
            return {"message": "An error occurred updating the item"}, 500
