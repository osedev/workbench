import sys; sys.path.append('websocket-client')
from websocket import WebSocketApp
from threading import Thread


class Connection(Thread):

    def __init__(self, username, password, server):
        super(Connection, self).__init__()
        self.username = username
        self.password = password
        self.server = server
        self.websocket = WebSocketApp(
            'ws://{}/streams'.format(server),
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

    def run(self):
        print ("Connecting to {}...".format(self.server))
        self.websocket.run_forever()

    def on_open(self):
        print('opened')

    def on_message(self, message):
        print('message: {}'.format(message))

    def on_error(self, error):
        print('error: {}'.format(error))

    def on_close(self):
        print('closed')
