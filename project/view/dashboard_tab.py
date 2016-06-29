from PySide import QtGui, QtCore


class DashboardTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DashboardTab, self).__init__(parent)

        grid = QtGui.QGridLayout()
        grid.addWidget(QtGui.QGroupBox("Top 7 to die"), 0, 0)
        grid.addWidget(QtGui.QGroupBox("Top 7 to survive"), 0, 1)
        grid.addWidget(QtGui.QGroupBox("Something else"), 1, 0)
        grid.addWidget(QtGui.QGroupBox("Houses"), 1, 1)
        self.setLayout(grid)