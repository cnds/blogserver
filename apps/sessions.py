from apps.base import BaseHandler
from apps.json_validate import SCHEMA
from dendy.request import req
from dendy.response import resp
from dendy.utils.encryption_base import create_md5_key, validate_hash_key


class Sessions(BaseHandler):

    def post(self):
        body = req.body
        is_valid = self.validate_dict_with_schema(
            body, SCHEMA['schema_sessions_post'])
        if not is_valid:
            resp.set_status(400, {'error': 'INVALID_BODY_CONTENT'})
            return

        name = body['name']
        password = body['password']
        flag, account_from_db = self.db.search_by_condition('users',
                                                            {'name': name})
        if not flag:
            return resp.set_status(500)

        if len(account_from_db) == 0:
            return resp.set_status(400, {'error': 'USER_NOT_FOUND'})

        elif len(account_from_db) > 1:
            return resp.set_status(500)

        else:
            password_from_db = account_from_db[0]['password']
            account_id = account_from_db[0]['id']

        secret_key = create_md5_key(self.SECRET_KEY)
        if not validate_hash_key(password, password_from_db, secret_key):
            return resp.set_status(
                400, {'error': 'PASSWORD_VERIFICATION_FAILED'})

        token = self.create_jwt({'id': account_id}, self.SECRET_KEY)
        return resp.set_status(201, {'id': account_id, 'token': token})
