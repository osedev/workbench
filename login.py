import FreeCADGui
from utils import path

LoginUI, QDialog = FreeCADGui.PySideUic.loadUiType(path('ui', 'login.ui'))


class LoginDialog(LoginUI, QDialog):

    def __init__(self, parent, service):
        super(LoginDialog, self).__init__(parent)
        self.setupUi(self)
        self.button_box.accepted.connect(self.connect)
        self.button_box.rejected.connect(self.reject)
        self.service = service

    @property
    def username(self):
        return self.username_input.text()

    @property
    def password(self):
        return self.password_input.text()

    @property
    def server(self):
        return self.server_input.text()

    def connect(self):
        self.service.connect(self.username, self.password, self.server)
        self.accept()
