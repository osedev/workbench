import operator
from PySide.QtCore import Qt, QAbstractTableModel
from PySide.QtGui import QIcon, QAbstractItemView
import FreeCADGui
from utils import path

ChatUI, QDockWidget = FreeCADGui.PySideUic.loadUiType(path('ui', 'plm.ui'))


class Icon:
    lock = QIcon(path('icons', 'lock.svg')).pixmap(16)
    locked = QIcon(path('icons', 'locked.svg')).pixmap(16)


class PartsTableModel(QAbstractTableModel):

    header = (
        {'key': 'id', 'label': 'ID', 'align': Qt.AlignLeft},
        {'key': 'locked', 'icon': Icon.lock},
        {'key': 'name', 'label': 'Name'},
    )

    def __init__(self):
        self.rows = [
            {'name': 'MicroTrac', 'locked': True, 'id': 99, 'description': 'A small tracked utility tractor similar to the Dingo.'},
            {'name': 'Shopaid', 'locked': False, 'id': 98, 'description': 'Mobile robot to help you in the workshop.'},
        ]
        QAbstractTableModel.__init__(self)

    def setModelData(self, data):
        self.beginResetModel()
        self.rows = data
        self.endResetModel()

    def columnCount(self, parent):
        return len(self.header)

    def rowCount(self, parent):
        return len(self.rows)

    def data(self, index, role):
        if not index.isValid():
            return None
        row = self.rows[index.row()]
        col = self.header[index.column()]
        cell = row[col['key']]
        if col['key'] == 'locked':
            if role == Qt.DecorationRole and cell:
                return Icon.locked
        elif role == Qt.DisplayRole:
            return cell

    def headerData(self, idx, orientation, role):
        if orientation == Qt.Horizontal:
            col = self.header[idx]
            if role == Qt.DecorationRole:
                return col.get('icon')
            elif role == Qt.DisplayRole:
                return col.get('label')
            elif role == Qt.TextAlignmentRole:
                return col.get('align')

    #def sort(self, col, order):
    #    parts = sorted(self.rows, key=operator.itemgetter(col))
    #    if order == Qt.DescendingOrder:
    #        parts.reverse()
    #    self.setModelData(parts)


class PLMDock(ChatUI, QDockWidget):

    def __init__(self, parent, streams):
        super(PLMDock, self).__init__(parent)
        self.setupUi(self)
        self.stream = streams['plm']
        self.stream.received.connect(self.accept_stream_event)

        self.parts_model = PartsTableModel()
        self.parts_table.setModel(self.parts_model)
        self.parts_table.setColumnWidth(0, 48)
        self.parts_table.setColumnWidth(1, 23)
        self.parts_table.horizontalHeader().setStretchLastSection(True)
        self.parts_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.parts_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.parts_table.clicked.connect(self.select_part)
        self.parts_table.activated.connect(self.open_part)

    def accept_stream_event(self, event):
        print(event)
        if event['model'] == 'plm.part':
            if event['action'] == 'list':
                self.parts_model.setModelData(event['data'])

    def select_part(self, idx):
        part = self.parts_model.rows[idx.row()]
        self.description_input.setText(part['description'])

    def open_part(self, idx):
        part = self.parts_model.rows[idx.row()]
        print(part['name'])
