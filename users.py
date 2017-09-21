from base import BaseHandler
from dendy.request import req
from dendy.response import resp


class Users(BaseHandler):

    def post(self):
        pass

class User(BaseHandler):

    def get(self, user_id):
        flag, user = self.db.search_by_id('users', user_id)
        if not flag:
            return resp.set_status(500)

        if not user:
            return resp.set_status(400, {'error': 'USER_NOT_FOUND'})

        return user

    def put(self, user_id):
        body = req.body
        result = self.db.update('users', user_id, body)
        return result

    def delete(self, user_id):
        pass
