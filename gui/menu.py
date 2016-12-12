from PyQt4 import Qt, QtGui, QtCore

from txt import txt

class MenuBar(QtGui.QMainWindow):
    def menu(self):
        open = QtGui.QAction(QtGui.QIcon(ico.OPEN_PROJECT),
                txt.OPEN_PROJECT, self)
        open.setShortcut("Ctrl+O")
        self.connect(self.open, QtCore.SIGNAL("triggered()"), self.OpenFile)
        self.exit = QtGui.QAction("&Exit", self)
        self.exit.setShortcut("Ctrl+Q")
        self.connect(self.exit, QtCore.SIGNAL("triggered()"), sys.exit)
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(self.open)
        filemenu.addSeparator()
        filemenu.addAction(exit)
