import logging

from gevent.pywsgi import WSGIServer

from apps.sessions import Sessions
from apps.users_handle import UserHandler
from dendy import API
from settings import config

app = API()
app.add_route('/login', Sessions(config))
app.add_route('/users/{user_id}', UserHandler(config))


if __name__ == '__main__':
    logging.basicConfig(format=config['log_format'], level=config['log_level'])
    logger = logging.getLogger()
    logger.info('Start listen on %s' % config['api_port'])
    WSGIServer(('', config['api_port']), app, log=logger).serve_forever()
