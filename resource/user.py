from flask_restful import Resource
from flask import request
from flask_restful import reqparse
from model.user import UserModel

class User(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type=str,
        required=True,
        help="Username is required")

    parser.add_argument(
        "password",
        type=str,
        required=True,
        help="Password is required")

    def post(self):
        data = User.parser.parse_args()
        user = UserModel.find(data["username"])
        if user:
            return {"message": "User {} already exists".format(data["username"])}, 400

        user = UserModel(**data)
        user.save()

        return {"message": "User added"}, 201
