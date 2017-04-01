from base import BaseHandler

class LoginHandler(BaseHandler):

    def get(self):
        self.write('Hello World')

