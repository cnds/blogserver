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
        user_from_db = self.db.search_by_condition('guardians', {'name': user})
        if not user_from_db:
            return self.write(json.dumps('search by user name failed'))

        password_from_db = user_from_db[0]['password']
        user_id = str(user_from_db[0]['id'])
        secret_key = self.create_md5_key(user_id)

        if self.validate_hash_key(password, password_from_db, secret_key):
            token = self.create_jwt({'id': user_id}, secret_key)
            return self.write({
                'id': user_id,
                'name': user,
                'token': token.decode('ascii')
            })
        else:
            self.set_status(400, reason='VERIFICATION_FAILED')
            return
