from PySide.QtCore import Qt, QObject, Signal, Slot
from websocket import WebSocketApp
from threading import Thread
from utils import Command

from chat import ChatDock
from login import LoginDialog


class OSEDevService(QObject):

    connected = Signal()
    disconnected = Signal()

    messaging = Signal(dict)

    def __init__(self, window):
        QObject.__init__(self)
        self.window = window
        self.connection = None
        self.chat_dock = ChatDock(self.window, self)
        self.login_dialog = LoginDialog(self.window, self)
        self.window.addDockWidget(Qt.BottomDockWidgetArea, self.chat_dock)
        self.commands = [
            Command(self, self.show_login_dialog, 'Connect', 'connect.svg', 'Connect to osedev.'),
            Command(self, self.disconnect, 'Disconnect', 'disconnect.svg', 'Disconnect from osedev.'),
            Command(self, self.chat_dock.toggleViewAction().trigger, 'Chat', 'chat.svg', 'Open chat panel.'),
        ]

    @property
    def command_names(self):
        return [c.id for c in self.commands]

    @property
    def is_connected(self):
        return False

    def show_login_dialog(self):
        self.login_dialog.show()

    def connect(self, username, password, server):
        if self.connection is not None:
            self.connection.disconnect()
        self.connection = Connection(username, password, server)
        self.connection.start()

    def disconnect(self):
        if self.connection is not None:
            self.connection.disconnect()
            self.connection = None


class Connection(Thread):

    def __init__(self, username, password, server):
        super(Connection, self).__init__()
        self.username = username
        self.password = password
        self.server = server
        self.websocket = WebSocketApp(
            'ws://'+server, ['X-Username: '+username, 'X-Password: '+password],
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

    def run(self):
        print("Connecting to {}...".format(self.server))
        self.websocket.run_forever()

    def disconnect(self):
        print("Disconnecting from {}...".format(self.server))
        self.websocket.close()

    def on_open(self, ws):
        print('opened')

    def on_message(self, ws, message):
        print('message: {}'.format(message))

    def on_error(self, ws, error):
        print('error: {}'.format(error))

    def on_close(self, ws, *args):
        print('closed')
