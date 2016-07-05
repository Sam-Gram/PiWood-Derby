#!/usr/bin/python

import sys
from sqlQueries import dropQuery, createQuery, insertEmptyRacerQuery
from PySide import QtCore
from PySide.QtSql import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView
from track import Track
from racerCalculator import racerCalculator

class MainWindow(QMainWindow):
    def __init__(self, track):
        super(MainWindow, self).__init__()
        self.track = track
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
        # TODO: Remove ID row
        # self.model.removeColumn(0)

        self.model.setHeaderData(0, QtCore.Qt.Orientation.Horizontal, "ID")
        self.model.setHeaderData(1, QtCore.Qt.Orientation.Horizontal, "Name")
        self.model.setHeaderData(2, QtCore.Qt.Orientation.Horizontal, "Race 1")
        self.model.setHeaderData(3, QtCore.Qt.Orientation.Horizontal, "Race 2")
        self.model.setHeaderData(4, QtCore.Qt.Orientation.Horizontal, "Race 3")
        self.model.setHeaderData(5, QtCore.Qt.Orientation.Horizontal, "Average")
        self.model.setHeaderData(6, QtCore.Qt.Orientation.Horizontal, "Scale Speed")

        # Populates the table, needed to show data
        self.model.select()

        projectView = QTableView()
        projectView.setModel(self.model)

        # TODO: Throw into seperate loop and test
        controls = QWidget()
        controlsLayout = QVBoxLayout()

        testButton = QPushButton("Test Gate, Sensors and Displays")
        testButton.setToolTip("Run a test on the track's gate, displays and sensors. After the displays clear waivin your hand under the sensors will change the displays for about ten seconds, then the test is done.")
        testButton.clicked.connect(self.track.test)

        insertButton = QPushButton("&Insert Racer")
        insertButton.setToolTip("Adds racer to table")
        insertButton.clicked.connect(self.insertRacer)

        clearButton = QPushButton("Clear the table")
        clearButton.setToolTip("Clear the table")
        # TODO: Make it kill the whole table.
        clearButton.clicked.connect(lambda _: None)

        controlsLayout.addWidget(testButton)
        controlsLayout.addWidget(insertButton)
        controlsLayout.addWidget(clearButton)

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
        self.track = Track()
        self.setUpGui(self.track)

        print('Setting up displays')

        sys.exit(self.app.exec_())

    def setUpGui(self, track):
        self.mw = MainWindow(track)


if __name__ == '__main__':
    PiWood()
