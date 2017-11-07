from PySide.QtCore import Qt
from PySide.QtGui import QStandardItemModel, QStandardItem
import FreeCADGui
from utils import path

ChatUI, QDockWidget = FreeCADGui.PySideUic.loadUiType(path('ui', 'chat.ui'))


class Room(QStandardItem):

    def __init__(self, data):
        super(Room, self).__init__(data[1])
        self.id = data[0]
        self.name = data[1]
        self.description = data[2]
        self.joined = data[3]


class ChatDock(ChatUI, QDockWidget):

    def __init__(self, parent, streams):
        super(ChatDock, self).__init__(parent)
        self.setupUi(self)
        self.stream = streams['chat']
        self.stream.received.connect(self.accept_stream_event)
        self.current_room = None
        self.room_list.setModel(QStandardItemModel(self.room_list))
        self.room_list.clicked.connect(self.view_room)
        self.room_list.activated.connect(self.join_room)
        self.chat_input.returnPressed.connect(self.send_message)

    def accept_stream_event(self, event):
        if 'rooms' in event:
            self.on_rooms(event['rooms'])
        if 'text' in event:
            self.on_message(event)

    def on_rooms(self, rooms):
        model = self.room_list.model()
        model.clear()
        for data in rooms:
            model.appendRow(Room(data))

    def on_message(self, message):
        self.chat_view.insertPlainText("{sender}: {text}\n".format(**message))

    def view_room(self, idx):
        room = self.room_list.model().itemFromIndex(idx)
        self.open_room(room)

    def join_room(self, idx):
        room = self.room_list.model().itemFromIndex(idx)
        if not room.joined:
            self.stream.send({'join': room.id})
            print('room joined {}'.format(room.data(Qt.UserRole+1)))

    def open_room(self, room):
        self.current_room = None
        if room.joined:
            self.current_room = room
            self.chat_view.clear()
        else:
            self.chat_view.setHtml(room.description)

    def send_message(self):
        if self.current_room is not None:
            self.stream.send({'room': self.current_room.id, 'message': self.chat_input.text()})
            self.chat_input.clear()
