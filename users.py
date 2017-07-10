import json

from base import BaseHandler


class Users(BaseHandler):

    def get(self):
        users = self.db.search_by_condition('guardians', {})
        if users:
            return self.write({'users': users})
        else:
            return self.write({'error': 'INTERNAL_ERROR'})

    def post(self):
        data = json.loads(self.request.body)
        user_name = data['name']
        user_from_db = self.db.search_by_condition('guardians',
                                                   {'name': user_name})
        if user_from_db:
            return self.set_status(400, reason='CONFLICT_USER')

        user = self.db.create('guardians', data)
        if user:
            user_id = user['id']
        else:
            return self.set_status(400, reason='CREATE_USER_FAILED')

        password = data['password']
        hashed_password = self.create_hash_key(password, self.SECRET_KEY)
        result = self.db.update(
            'guardians', user_id, {'password': hashed_password})
        if result:
            return self.write({'id': user_id})
        else:
            return self.set_status(400, reason='UPDATE_PASSWORD_FAILED')


class User(BaseHandler):

    def get(self, user_id):
        user = self.db.search_by_id('users', user_id)
        print(user)
        if user:
            return self.write(user)
        else:
            return self.write({'error': 'USER_NOT_FOUND'})
