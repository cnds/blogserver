import json
from base import BaseHandler


class Sessions(BaseHandler):

    def get(self):
        self.set_header('content-type', 'text/html')
        return self.write('<h1>Hello World!</h1>')

    def post(self):
        data = json.loads(self.request.body)
        user = data.get('user')
        password = data.get('password')
        password.encode('utf-8')
        user_from_db = self.db['accounts'].find_one({'name': user})
        if not user_from_db:
            return self.write('search by user name failed')

        password_from_db = user_from_db['password']
        user_id = str(user_from_db['_id'])
        secret_key = self.create_md5_key(user_id)
        # print(password_from_db)

        if self.validate_hash_key(password, password_from_db, secret_key):
            return self.write({'id': user_id})
        else:
            return self.write({'error': 'VERIFICATION_FAILED'})
