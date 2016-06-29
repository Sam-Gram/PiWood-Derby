#!/usr/bin/python

import sys
import time
from sqlQueries import dropQuery, createQuery, insertEmptyRacerQuery
from PySide import QtCore
from PySide.QtSql import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView

def stubFunction():
    print("Stub Function Executed")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("piwood.db")
        self.db.open()

        # Show if there is a problem with the database connection
        print("Database Connection", self.db.isValid())

        self.model = QSqlTableModel(None, self.db)
        self.model.setTable("racers")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        # Populates the table, needed to show data
        self.model.select()

        projectView = QTableView()
        projectView.setModel(self.model)

        # TODO: Throw into seperate loop and test
        controls = QWidget()
        controlsLayout = QVBoxLayout()

        testButton = QPushButton("Test Sensors and Displays")
        testButton.setToolTip("Run a test on the track's sensors and displays")
        testButton.clicked.connect(stubFunction)

        insertButton = QPushButton("Insert Racer")
        insertButton.setToolTip("Adds racer to table")
        insertButton.clicked.connect(self.insertRacer)

        saveButton = QPushButton("Save the table")
        saveButton.setToolTip("Save the table to the database.")
        saveButton.clicked.connect(self.saveTable)

        clearButton = QPushButton("Clear the table")
        clearButton.setToolTip("Clear the table")
        clearButton.clicked.connect(stubFunction)

        controlsLayout.addWidget(testButton)
        controlsLayout.addWidget(insertButton)
        controlsLayout.addWidget(saveButton)
        controlsLayout.addWidget(saveButton)

        controls.setLayout(controlsLayout)

        rightDockWidget = QDockWidget()
        rightDockWidget.setWidget(controls)
        rightDockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.setCentralWidget(projectView)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
                           rightDockWidget)

        # &E allows users to use Alt E
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)


        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.statusBar().showMessage('Ready')

        # In case the windows is shrunk
        self.setGeometry(300,300,250,150)
        self.showMaximized()
        self.setWindowTitle('PiWood-Derby')
        self.show()

    def insertRacer(self):
        # -1 Puts the record at the end of the database
        if QSqlQuery(insertEmptyRacerQuery, self.db) == False:
            print(self.model.lastError())
        # Populates the table, needed to show data
        self.model.select()


    # Save all changes to the table
    def saveTable(self):
        if self.model.submitAll() == False:
            print(self.model.lastError())

    def clearTable(self):
        QSqlQuery(dropQuery, self.db)
        QSqlQuery(createQuery, self.db)

    def close(self):
        self.db.close()
        print("DB connection closed")
        super(MainWindow, self).close()

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
