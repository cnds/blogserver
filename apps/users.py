import logging

import dendy
from apps.base import BaseHandler
from apps.json_validate import SCHEMA
from dendy.request import req
from dendy.response import resp
from dendy.utils.encryption_base import create_hash_key, create_md5_key


class Users(BaseHandler):

    def post(self):
        body = req.body
        is_valid = self.validate_schema_with_dict(
            body, SCHEMA['schema_users_post'])
        if not is_valid:
            return resp.set_status(400, {'error': 'INVALID_BODY_CONTENT'})

        name = body['name']
        password = body['password']
        flag, user = self.db.search_by_condition('users', {'name': name})
        if not flag:
            logging.error('get user by name failed')
            return resp.set_status(500)

        if user:
            return resp.set_status(400, {'error': 'USER_EXISTS'})

        secret_key = create_md5_key(self.SECRET_KEY)
        hashed_password = create_hash_key(password, secret_key)
        data_to_insert = {
            'name': name,
            'password': hashed_password
        }
        result = self.db.create('users', data_to_insert)
        if result:
            return resp.set_status(201, result)
        else:
            logging.error('create user internal error')
            return resp.set_status(500)

class User(BaseHandler):

    @dendy.before(BaseHandler.authenticate)
    def get(self, user_id):
        flag, user = self.db.search_by_id('users', user_id)
        if not flag:
            return resp.set_status(500)

        if not user:
            return resp.set_status(400, {'error': 'USER_NOT_FOUND'})

        return user

    @dendy.before(BaseHandler.authenticate)
    def put(self, user_id):
        body = req.body
        result = self.db.update_by_id('users', user_id, body)
        if not result:
            logging.error('update user internal error')
            return resp.set_status(500)

        return result

    @dendy.before(BaseHandler.authenticate)
    def delete(self, user_id):
        result = self.db.remove_by_id('users', user_id)
        if not result:
            logging.error('remove user internal error')
            return resp.set_status(500)

        return result