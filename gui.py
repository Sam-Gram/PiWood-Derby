# TODO: Move code to GUI class

import sys
import time
from PySide import QtCore
from PySide.QtSql import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("piwood.db")
        db.open()

        model = QSqlQueryModel()
        model.setQuery("select * from racers", db)

        projectView = QTableView()
        projectView.setModel(model)

        testButton = QPushButton("Test")
        rightDockWidget = QDockWidget()
        rightDockWidget.setWidget(testButton)
        rightDockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        self.setCentralWidget(projectView)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
                           rightDockWidget)
        

        

        #self.setLayout(grid)
        
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        self.statusBar().showMessage('Ready')
        
        self.setGeometry(300,300,250,150)
        self.showMaximized()
        self.setWindowTitle('PiWood-Derby')
        self.show()

    def updateStatusBar(self, string):
        self.statusBar().showMessage(string)

class Gui():
    def __init__(self):
        app = QApplication(sys.argv)
        mw = MainWindow()
        sys.exit(app.exec_())

    
    





# TODO: Old
# # Create Qt application and the QDeclarative view
# app = QApplication(sys.argv)
# view = QDeclarativeView()
# # Create an URL to the QML file
# url = QUrl('view.qml')
# # Set the QML file and show
# view.setSource(url)
# view.show()
# # Enter Qt main loop
# sys.exit(app.exec_())

