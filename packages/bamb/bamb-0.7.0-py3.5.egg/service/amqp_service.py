from amqp import connection
from bamb import Bamb
from domain import exceptions


class AmqpService(object):

    def __init__(self, app=None):
        if not isinstance(app, Bamb):
            raise exceptions.AppException("can not determine app instance!")
        self.__connection = AmqpConnection(host=app.conf.AMQP_HOST, userid=app.conf.AMQP_USER,
                                           password=app.conf.AMQP_PASSWORD,
                                           virtual_host=app.conf.AMQP_VIRTUAL_HOST)

    @property
    def connection(self):
        if not isinstance(self.__connection, connection.Connection):
            raise exceptions.AppException("connection is not initialized")
        if not self.__connection.connected:
            self.__connection.connect()
        return self.__connection.channel()


class AmqpConnection(connection.Connection):

    def __init__(self, host='localhost:5672', userid='guest', password='guest',
                 login_method=None, login_response=None,
                 authentication=(),
                 virtual_host='/', locale='en_US', client_properties=None,
                 ssl=False, connect_timeout=None, channel_max=None,
                 frame_max=None, heartbeat=0, on_open=None, on_blocked=None,
                 on_unblocked=None, confirm_publish=False,
                 on_tune_ok=None, read_timeout=None, write_timeout=None,
                 socket_settings=None, **kwargs):
        connection.Connection.__init__(self, host, userid, password, login_method,
                                       login_response, authentication, virtual_host, locale,
                                       client_properties, ssl, connect_timeout, channel_max, frame_max,
                                       heartbeat, on_open, on_blocked, on_unblocked, confirm_publish,
                                       on_tune_ok, read_timeout, write_timeout, socket_settings, **kwargs)


