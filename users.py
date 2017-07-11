import json

from base import BaseHandler


class Users(BaseHandler):

    def get(self):
        condition = self.request.query_arguments
        flag, users = self.db.search_by_condition('users', condition)
        if not flag:
            return self.set_status(500, reason='REQUEST_DB_FAILED')

        return self.write({'users': users})

    def post(self):
        data = json.loads(self.request.body)
        user_name = data['name']
        flag, user_from_db = self.db.search_by_condition('users',
                                                   {'name': user_name})
        if not flag:
            return self.set_status(500, reason='REQUEST_DB_FAILED')

        if user_from_db:
            return self.set_status(400, reason='CONFLICT_USER')

        user = self.db.create('users', data)
        if user:
            user_id = user['id']
        else:
            return self.set_status(400, reason='CREATE_USER_FAILED')

        password = data['password']
        hashed_password = self.create_hash_key(password, self.SECRET_KEY)
        print(type(hashed_password))
        result = self.db.update(
            'users', user_id, {'password': hashed_password})
        if result:
            return self.write({'id': user_id})
        else:
            return self.set_status(400, reason='UPDATE_PASSWORD_FAILED')


class User(BaseHandler):

    def get(self, user_id):
        flag, user = self.db.search_by_id('users', user_id)
        if not flag:
            return self.set_status(500, reason='REQUEST_DB_FAILED')

        if not user:
            return self.set_status(400, reason='USER_NOT_FOUND')

        return self.write(user)
