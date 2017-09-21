from dendy import API
from gevent.pywsgi import WSGIServer
from sessions import Sessions
from settings import config
from users import User


app = API()
app.add_route('/login', Sessions(config))
app.add_route('/users/{user_id}', User(config))


if __name__ == '__main__':
    WSGIServer(('', 8000), app).serve_forever()
