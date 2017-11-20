import json
from websocket import WebSocketApp
from threading import Thread
from utils import Command
from PySide.QtCore import Qt, QObject, Signal

from plm import PLMDock
from chat import ChatDock
from login import LoginDialog


class Stream(QObject):

    connected = Signal()
    disconnected = Signal()
    received = Signal(dict)

    def __init__(self, service, name):
        super(Stream, self).__init__()
        self.service = service
        self.name = name

    def send(self, payload):
        self.service.connection.send(json.dumps({
            'stream': self.name, 'payload': payload
        }))

    def receive(self, message):
        if message['stream'].startswith(self.name):
            self.received.emit(message['payload'])


class OSEDevService(QObject):

    def __init__(self, window):
        QObject.__init__(self)
        self.window = window
        self.connection = None
        self.streams = {
            'chat': Stream(self, 'chat'),
            'plm': Stream(self, 'plm'),
        }
        self.chat_dock = ChatDock(self.window, self.streams)
        self.window.addDockWidget(Qt.BottomDockWidgetArea, self.chat_dock)
        self.plm_dock = PLMDock(self.window, self.streams)
        self.window.addDockWidget(Qt.RightDockWidgetArea, self.plm_dock)
        self.login_dialog = LoginDialog(self.window, self)
        self.commands = [
            Command(self, self.show_login_dialog, 'Connect', 'connect.svg', 'Connect to osedev.'),
            Command(self, self.disconnect, 'Disconnect', 'disconnect.svg', 'Disconnect from osedev.'),
            Command(self, self.plm_dock.toggleViewAction().trigger, 'Part Catalog', 'plm.svg', 'Open part catalog panel.'),
            Command(self, self.chat_dock.toggleViewAction().trigger, 'Chat', 'chat.svg', 'Open chat panel.'),
        ]

    @property
    def command_names(self):
        return [c.id for c in self.commands]

    @property
    def is_connected(self):
        return self.connection is not None and self.connection.is_connected

    def show_login_dialog(self):
        self.login_dialog.show()

    def connect(self, username, password, server):
        if self.connection is not None:
            self.connection.disconnect()
        self.connection = Connection(username, password, server, self)
        self.connection.start()

    def disconnect(self):
        if self.connection is not None:
            self.connection.disconnect()
            self.connection = None


class Connection(Thread):

    def __init__(self, username, password, server, service):
        super(Connection, self).__init__()
        self.username = username
        self.password = password
        self.server = server
        self.websocket = WebSocketApp(
            'ws://'+server, ['X-Username: '+username, 'X-Password: '+password],
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.service = service

    def run(self):
        print("Connecting to {}...".format(self.server))
        self.websocket.run_forever()

    def on_open(self, ws):
        for stream in self.service.streams.values():
            stream.connected.emit()

    def on_message(self, ws, message):
        data = json.loads(message)
        for stream in self.service.streams.values():
            stream.receive(data)

    def on_error(self, ws, error):
        print('error: {}'.format(error))

    def send(self, msg):
        self.websocket.send(msg)

    def on_close(self, ws):
        print("Disconnecting from {}...".format(self.server))
        for stream in self.service.streams.values():
            stream.disconnected.emit()

    def disconnect(self):
        self.websocket.close()

    @property
    def is_connected(self):
        return self.websocket.sock.connected
