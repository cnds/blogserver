from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from storage_engine import db

from sessions import Sessions

def make_app():
    return Application([
        (r"/sessions", Sessions, dict(db=db))
    ])

app = make_app()

if __name__ == '__main__':
    server = HTTPServer(app)
    server.listen(8888)
    print('start listening on 8888')
    IOLoop.current().start()