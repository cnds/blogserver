import binascii
import hashlib
from hashlib import pbkdf2_hmac
from tornado.web import RequestHandler

class BaseHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header('content-type', 'application/json')

    def initialize(self, db):
        self.db = db

    @staticmethod
    def create_hash_key(content, secret_key, round_times=10000):
        hashed_content = pbkdf2_hmac('sha256', content.encode('ascii'), secret_key.encode('ascii'), round_times)
        hashed_content_hex = binascii.hexlify(hashed_content)

        return hashed_content_hex


    @staticmethod
    def validate_hash_key(key, hashed_key, secret_key, round_times=10000):
        derived_key = BaseHandler.create_hash_key(key, secret_key, round_times)
        if derived_key == hashed_key.encode('ascii'):
            return True

        return False

    @staticmethod
    def create_md5_key(content):
        md5 = hashlib.md5()
        md5.update(content.encode('ascii'))
        md5_content = md5.hexdigest()

        return md5_content