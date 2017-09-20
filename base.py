import jwt
import json

from jsonschema import Draft4Validator

from storage_engine import StorageEngine


class BaseHandler(object):


    def __init__(self, config):
        self.db = StorageEngine(config)
        self.SECRET_KEY = config['encryption']['key']
        self.ENCRYPTION_ALGORITHM = config['encryption']['algorithm']

    @staticmethod
    def create_jwt(content, secret, algorithm='HS256'):
        token = jwt.encode(content, secret, algorithm)
        return token

    @staticmethod
    def check_jwt(token, secret, algorithms, params):
        payload = jwt.decode(token, secret, algorithms)
        token_content = payload['id']
        if params['user_id'] != token_content:
            return False, None
        return True, token_content

    def validate_body_content(self, schema):
        try:
            data = json.loads(self.request.body)
        except Exception as ex:
            return 400, 'parse json failed: %s' % ex

        try:
            Draft4Validator.check_schema(schema)
        except Exception as ex:
            return 400, 'invalid schema: %s' % ex

        try:
            Draft4Validator(schema).validate(data)
        except Exception as ex:
            return 400, 'parse body failed: %s' % ex
        else:
            return 200, data
