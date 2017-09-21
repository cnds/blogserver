import jwt
import json
import logging

from jsonschema import Draft4Validator
from dendy.request import req
from dendy.status import HTTPError

from storage_engine import StorageEngine
from json_validate import SCHEMA_INTERNAL


class BaseHandler(object):

    def __init__(self, config):
        self.db = StorageEngine(config)
        self.SECRET_KEY = config['encryption']['key']
        self.ENCRYPTION_ALGORITHM = config['encryption']['algorithm']

    @staticmethod
    def create_jwt(content, secret, algorithm='HS256'):
        token = jwt.encode(content, secret, algorithm).decode('utf-8')
        return token

    @staticmethod
    def decode_token(token, secret, algorithms='HS256'):
        try:
            token_content = jwt.decode(token, secret, algorithms)
        except Exception as ex:
            logging.error('parse jwt failed: %s' % ex)
            return None

        return token_content

    def check_token_content(self, token_content):
        code, data = self.validate_dict_with_schema(
            token_content, SCHEMA_INTERNAL['schema_token'])
        if code != 200:
            return False

        return True

    def check_jwt(self, token, secret):
        token_content = self.decode_token(token, self.SECRET_KEY)
        if token_content is None:
            return False, None

        if not self.check_token_content(token_content):
            return False, None

        return True, token_content

    @staticmethod
    def validate_dict_with_schema(data, schema):
        try:
            Draft4Validator.check_schema(schema)
        except Exception as ex:
            return 400, 'invalid schema: %s' % ex

        try:
            Draft4Validator(schema).validate(data)
        except Exception as ex:
            return 400, 'parse body failed: %s' % ex
        else:
            return 200, None

    def validate_body_content(self, schema):
        try:
            data = json.loads(req.body)
        except Exception as ex:
            return 400, 'parse json failed: %s' % ex

        code, tag = self.validate_dict_with_schema(data, schema)
        if code != 200:
            return 400, tag

        return 200, data

    @staticmethod
    def check_route_id(token_content, params):
        id_from_token = token_content['id']
        route_id = params['user_id']
        if id_from_token != route_id:
            return False

        return True

    def authenticate(self, **params):
        token = req.token
        if not token:
            raise HTTPError(500, {'error': 'AUTHENTICATION_INFO_REQUIRED'})

        flag, token_content = self.check_jwt(token, self.SECRET_KEY)
        if not flag:
            raise HTTPError(400, {'error': 'AUTHENTICATION_INFO_ILLEGAL'})

        if not self.check_route_id(token_content, params):
            raise HTTPError(400, {'error': 'ACCESS_DENIED'})

        return
