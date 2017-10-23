from os.path import join, dirname
import FreeCADGui

LoginUI, QDialog = FreeCADGui.PySideUic.loadUiType(join(dirname(__file__), 'ui/login.ui'))


class LoginDialog(LoginUI, QDialog):

    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    @property
    def username(self):
        return self.username_input.text()

    @property
    def password(self):
        return self.password_input.text()

    @property
    def server(self):
        return self.server_input.text()
