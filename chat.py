from os.path import join, dirname
import FreeCADGui

ChatUI, QDockWidget = FreeCADGui.PySideUic.loadUiType(join(dirname(__file__), 'ui/chat.ui'))


class ChatDock(ChatUI, QDockWidget):

    def __init__(self, *args, **kwargs):
        super(ChatDock, self).__init__(*args, **kwargs)
        self.setupUi(self)
