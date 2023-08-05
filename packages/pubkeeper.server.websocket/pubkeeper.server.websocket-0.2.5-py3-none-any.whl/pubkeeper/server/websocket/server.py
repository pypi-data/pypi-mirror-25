"""
Copyright 2017 n.io Innovation, LLC | Patent Pending
"""
from tornado import web, websocket, httpserver, ioloop, gen, log
from pubkeeper.server.websocket.pool import ConnectionPool
import ujson as json
import logging
try:
    from signal import signal, SIGINFO
    has_signal = True
except:
    from signal import signal, SIGUSR1
    has_signal = False

(JOIN, LEAVE, PUBLISH, INVALIDATE) = (0, 1, 2, 3)
packet_names = ['JOIN', 'LEAVE', 'PUBLISH', 'INVALIDATE']


class ConnectionHandler(websocket.WebSocketHandler):
    pools = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logging.getLogger('pubkeeper.server.websocket')
        self._in_pools = []
        self._message_handlers = {
            JOIN: self._on_join,
            LEAVE: self._on_leave,
            PUBLISH: self._on_publish,
            INVALIDATE: self._on_invalidate
        }

    def check_origin(self, origin):  # pragma: no cover
        return True

    def on_close(self):
        for pool in self._in_pools:
            pool.del_socket(self)

    @gen.coroutine
    def on_message(self, message):
        message = json.loads(message)
        frame = int(message[0])
        topic = message[1]
        try:
            data = message[2]
        except IndexError:
            data = None

        if frame in self._message_handlers:
            self._message_handlers[frame](topic, data)

    @classmethod
    def _get_pool(cls, topic=None, create=True):
        if topic is not None:
            if topic not in cls.pools:
                if create:
                    cls.pools[topic] = ConnectionPool()
                else:
                    return None

            return cls.pools[topic]

    @classmethod
    def _del_pool(cls, topic=None):
        if topic is not None:
            if topic in cls.pools:
                del(cls.pools[topic])

    def _on_join(self, topic, *args):
        pool = self._get_pool(topic)
        pool.add_socket(self)
        self._in_pools.append(pool)
        self._logger.info("Client Joined {}".format(topic))

    def _on_leave(self, topic, *args):
        pool = self._get_pool(topic)
        pool.del_socket(self)
        self._in_pools.remove(pool)

        if pool.empty() and not pool._lvc:
            self._del_pool(topic)

        self._logger.info("Client Left {}".format(topic))

    def _on_publish(self, topic, data):
        pool = self._get_pool(topic)
        pool.publish(self, data, ignore=self)
        self._logger.debug("Client Publishes to {} : {}".format(topic, data))

    def _on_invalidate(self, topic, *args):
        pool = self._get_pool(topic)
        if pool:
            pool.invalidate()
            self._logger.debug("Invalidating LVC : {}".format(topic))


def start_server():
    app = web.Application([
        (r"/", ConnectionHandler),
    ], websocket_ping_interval=10)

    http_server = httpserver.HTTPServer(app)
    http_server.listen(8000)

    def print_network(self, *args, **kwargs):
        for topic, pool in ConnectionHandler.pools.items():
            print("Topic: {}".format(topic))
            for conn in pool._connections:
                print("Has {}".format(conn))

    if has_signal:
        signal(SIGINFO, print_network)
    else:
        signal(SIGUSR1, print_network)

    try:
        logging.getLogger('pubkeeper.server.websocket').info(
            "Websocket Server Started")
        ioloop.IOLoop.current().start()
        ioloop.IOLoop.current().close()
    except KeyboardInterrupt:
        stop_server()


def stop_server():
    ioloop.IOLoop.current().stop()
    logging.getLogger('pubkeeper.server.websocket').info(
        "Websocket Server Stopped")


if __name__ == "__main__":
    log.enable_pretty_logging()
    logging.getLogger().setLevel(logging.INFO)
    start_server()
