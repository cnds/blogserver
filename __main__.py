import tornado.ioloop
import tornado.web

from login import LoginHandler

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/login", LoginHandler)
    ])
    application.listen(8080)
    tornado.ioloop.IOLoop.current().start()
