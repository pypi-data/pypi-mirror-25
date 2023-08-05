"""
Copyright 2017 n.io Innovation, LLC | Patent Pending
"""
from tornado import gen, websocket


class ConnectionPool(object):
    def __init__(self):
        self._connections = []
        self._lvc = None

    @gen.coroutine
    def add_socket(self, socket):
        if self._lvc is not None:
            yield socket.write_message(self._lvc['data'], binary=True)

        self._connections.append(socket)

    def del_socket(self, socket):
        if self._lvc is not None and self._lvc['socket'] is socket:
            self.invalidate()

        self._connections.remove(socket)

    def empty(self):
        return len(self._connections) == 0

    def invalidate(self):
        self._lvc = None

    @gen.coroutine
    def publish(self, socket, data, ignore=None):
        self._lvc = {
            'socket': socket,
            'data': data
        }

        for conn in self._connections:
            if ignore is None or ignore is not conn:
                try:
                    yield conn.write_message(data, binary=True)
                except websocket.WebSocketClosedError:
                    # If this connection is dead, remove it
                    self.del_socket(conn)
