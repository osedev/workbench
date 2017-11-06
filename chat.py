from PySide.QtGui import QStandardItemModel, QStandardItem
import FreeCADGui
from utils import path

ChatUI, QDockWidget = FreeCADGui.PySideUic.loadUiType(path('ui', 'chat.ui'))


class ChatDock(ChatUI, QDockWidget):

    def __init__(self, parent, service):
        super(ChatDock, self).__init__(parent)
        self.setupUi(self)
        self.service = service
        self.room_list.setModel(QStandardItemModel(self.room_list))
        self.room_list.clicked.connect(self.on_enter_room)
        self.on_connect()

    def on_connect(self):
        model = self.room_list.model()
        item = QStandardItem('#General')
        model.appendRow(item)

    def on_enter_room(self, room):
        print('room clicked {}'.format(room.data()))
