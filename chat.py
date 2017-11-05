import FreeCADGui
from utils import path

ChatUI, QDockWidget = FreeCADGui.PySideUic.loadUiType(path('ui', 'chat.ui'))


class ChatDock(ChatUI, QDockWidget):

    def __init__(self, parent, service):
        super(ChatDock, self).__init__(parent)
        self.setupUi(self)
        self.service = service


