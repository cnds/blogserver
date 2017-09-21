import logging

import dendy

from base import BaseHandler
from dendy.request import req
from dendy.response import resp


class UsersHandler(BaseHandler):

    def post(self):
        pass

class UserHandler(BaseHandler):

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
