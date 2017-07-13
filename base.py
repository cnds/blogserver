import binascii
import hashlib
import jwt
import json

from hashlib import pbkdf2_hmac
from tornado.web import RequestHandler
from jsonschema import Draft4Validator

from storage_engine import StorageEngine


class BaseHandler(RequestHandler):


    def initialize(self, config):
        self.db = StorageEngine(config)
        self.SECRET_KEY = config['encryption']['key']
        self.ENCRYPTION_ALGORITHM = config['encryption']['algorithm']

    def set_default_headers(self):
        self.set_header('content-type', 'application/json')


    @classmethod
    def create_hash_key(cls, content, secret_key, round_times=10000):
        hashed_content = pbkdf2_hmac(
            'sha256',
            content.encode('ascii'),
            secret_key.encode('ascii'),
            round_times)
        hashed_content_hex = str(binascii.hexlify(hashed_content))

        return hashed_content_hex


    @classmethod
    def validate_hash_key(
            cls, key, hashed_key, secret_key, round_times=10000):
        derived_key = cls.create_hash_key(key, secret_key, round_times)
        if derived_key == hashed_key:
            return True

        return False

    @staticmethod
    def create_md5_key(content):
        md5 = hashlib.md5()
        md5.update(content.encode('ascii'))
        md5_content = md5.hexdigest()
        return md5_content

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
