from PySide.QtCore import *
import operator


class ResultTableModel(QAbstractTableModel):
    def __init__(self, parent, data, headers, *args):
        QAbstractTableModel.__init__(self, parent, *args)

        self.my_data = data
        self.headers = headers

    def rowCount(self, parent):
        return len(self.my_data)

    def columnCount(self, parent):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.my_data[index.row()][index.column() + 1]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[col]
        return None

    def changeData(self, data):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.my_data = data
        self.emit(SIGNAL('dataChanged()'))
        self.emit(SIGNAL("layoutChanged()"))

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.my_data = sorted(self.my_data,
                              key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.my_data.reverse()
        self.emit(SIGNAL("layoutChanged()"))
