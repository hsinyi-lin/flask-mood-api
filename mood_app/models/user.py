from datetime import datetime


class UserModel:
    @staticmethod
    def create_user(user_col, data, hash_pw):
        new_user = {
            'username': data['username'],
            'email': data['email'],
            'password': hash_pw,
            'createTime': datetime.now()
        }

        inserted_id = user_col.insert_one(new_user).inserted_id
        new_user['_id'] = str(inserted_id)

        return new_user