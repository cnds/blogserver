from base import BaseHandler


class Users(BaseHandler):

    def get(self):
        users = self.db.search_by_condition('guardians', {})
        if users:
            return self.write({'users': users})
        else:
            return self.write({'error': 'INTERNAL_ERROR'})