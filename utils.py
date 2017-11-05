import os


def path(*args):
    return os.path.join(os.path.dirname(__file__), *args)


class Command:

    def __init__(self, service, method, label, icon, help):
        self.service = service
        self.method = method
        self.id = 'osedev-{}'.format(label.lower())
        self.label = label
        self.icon = icon
        self.help = help

    def GetResources(self):
        return {
            'Group': 'File',
            'Pixmap': path('icons', self.icon),
            'MenuText': self.label,
            'ToolTip': self.help
        }

    def Activated(self):
        self.method()

    def IsActive(self):
        return True
