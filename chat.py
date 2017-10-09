from os.path import join, dirname

import FreeCADGui
from PySide.QtGui import QDockWidget


class ChatWindow(QDockWidget):
    def __init__(self, *args, **kwargs):
        super(ChatWindow, self).__init__(*args, **kwargs)
        widget = FreeCADGui.PySideUic.loadUi(join(dirname(__file__), 'ui/login.ui'))
        widget.setParent(self)
        self.setWidget(widget)
