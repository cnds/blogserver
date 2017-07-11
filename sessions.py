import json
from base import BaseHandler


class Sessions(BaseHandler):

    def get(self):
        self.set_header('content-type', 'text/html')
        return self.write('<h1>200 OK!</h1>')

    def post(self):
        data = json.loads(self.request.body)
        user = data.get('name')
        password = data.get('password')
        flag, user_from_db = self.db.search_by_condition('users', {'name': user})
        if not flag:
            return self.set_status(500, reason='REQUEST_DB_FAILED')

        if not user_from_db:
            return self.set_status(400, reason='USER_NOT_FOUND')

        password_from_db = user_from_db[0]['password']
        user_id = str(user_from_db[0]['id'])

        if self.validate_hash_key(password, password_from_db, self.SECRET_KEY):
            token = self.create_jwt({'id': user_id}, self.SECRET_KEY)
            return self.write({
                'id': user_id,
                'name': user,
                'token': token.decode('ascii')
            })
        else:
            self.set_status(400, reason='VERIFICATION_FAILED')
            return
