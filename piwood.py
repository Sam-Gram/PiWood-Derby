#!/usr/bin/python

import sys
import time
from PySide import QtCore
from PySide.QtSql import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView

def stubFunction():
    print("Hello")

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
        testButton.setToolTip("Run a test on the <b>track's</b> displays")
        testButton.clicked.connect(stubFunction)
        
        rightDockWidget = QDockWidget()
        rightDockWidget.setWidget(testButton)
        rightDockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        self.setCentralWidget(projectView)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
                           rightDockWidget)

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



class PiWood:    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.setUpGui()
        
        print('Setting up displays')

        sys.exit(self.app.exec_())

    def setUpGui(self):
        self.mw = MainWindow()
        
        

if __name__ == '__main__':
    PiWood()
