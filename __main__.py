from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from sessions import Sessions
from users import Users, User
from settings import config

def make_app():
    return Application([
        (r"/sessions", Sessions, dict(config=config)),
        (r"/users", Users, dict(config=config)),
        (r"/users/([0-9]+)", User, dict(config=config))
    ], debug=True)

app = make_app()

if __name__ == '__main__':
    server = HTTPServer(app)
    server.listen(8888)
    print('start listening on 8888')
    IOLoop.current().start()