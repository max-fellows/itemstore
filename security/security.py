from werkzeug.security import safe_str_cmp
from model.user import UserModel

class AuthenticationService:

    def authenticate(self, username, password):
        user = UserModel.find(username)
        if user and safe_str_cmp(user.password, password):
            return user

    def identity(self, payload):
        user_id = payload["identity"]
        return UserModel.find_by_id(user_id)
