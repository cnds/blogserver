from base import BaseHandler
from dendy.request import req
from dendy.response import resp
from dendy.utils.encryption_base import create_md5_key, validate_hash_key


class Sessions(BaseHandler):

    def get(self):
        return '<h1>200 OK!</h1>'

    def post(self):
        body = req.body
        name = body.get('name')
        password = body.get('password')

        flag, account_from_db = self.db.search_by_condition('users', {'name': name})
        if not flag:
            return resp.set_status(500)

        if len(account_from_db) == 0:
            return resp.set_status(400, 'USER_NOT_FOUND')

        elif len(account_from_db) > 1:
            return resp.set_status(500)

        else:
            password_from_db = account_from_db[0]['password']

        secret_key = create_md5_key(self.SECRET_KEY)
        if not validate_hash_key(password, password_from_db, secret_key):
            return resp.set_status(400, 'PASSWORD_VERIFICATION_FAILED')

        # TODO
        # return jwt
        return 'login success'

