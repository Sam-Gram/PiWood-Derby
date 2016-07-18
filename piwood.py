#!/usr/bin/python

import sys
from sqlQueries import dropQuery, createQuery, insertEmptyRacerQuery, createRaceQuery, dropRaceQuery, incrementRaceQuery, getRaceNumQuery, getNumberOfRacersQuery
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

        startRaceButton = QPushButton("Start Race")
        startRaceButton.clicked.connect(self.startRace)

        goBackOneRaceButton = QPushButton("Go Back One Race")
        goBackOneRaceButton.clicked.connect(self.goBackOneRace)

        stopRaceButton = QPushButton("Stop Race")
        stopRaceButton.clicked.connect(self.stopRace)

        controlsLayout.addWidget(testButton)
        controlsLayout.addWidget(insertButton)
        controlsLayout.addWidget(clearButton)
        controlsLayout.addWidget(startRaceButton)
        controlsLayout.addWidget(goBackOneRaceButton)
        controlsLayout.addWidget(stopRaceButton)

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

    def startRace(self):
        QSqlQuery(incrementRaceQuery)
        raceNum = QSqlQuery(getRaceNumQuery)
        raceNum.first()
        raceNum = raceNum.record().field(0).value()
        numCars = QSqlQuery(getNumberOfRacersQuery)
        numCars.first()
        numCars = numCars.record().field(0).value()
        self.racers = racerCalculator(raceNum, numCars)
        msgBox = QMessageBox()
        msgBox.setText("Place car numbered: " +
                       str(self.racers[0] + 1) + " " +
                       str(self.racers[1] + 1) + " " +
                       str(self.racers[2] + 1))
        msgBox.exec_()
        self.track.startRace()

    def goBackOneRace(self):
        QSqlQuery("UPDATE race_num SET num = num - 1;")
        
    def stopRace(self):
        times = self.track.stopRace()
        print(times)
        print("racers " + str(self.racers))
        whichRace = self.getWhichRace(self.racers[0] + 1)
        QSqlQuery("UPDATE racers SET time_" + str(whichRace) + " = " + str(times[0]) + " WHERE id = " + str(self.racers[0] + 1))

        whichRace = self.getWhichRace(self.racers[1] + 1)
        QSqlQuery("UPDATE racers SET time_" + str(whichRace) + " = " + str(times[1]) + " WHERE id = " + str(self.racers[1] + 1))

        whichRace = self.getWhichRace(self.racers[2] + 1)
        QSqlQuery("UPDATE racers SET time_" + str(whichRace) + " = " + str(times[2]) + " WHERE id = " + str(self.racers[2] + 1))
        self.model.select()

    def getWhichRace(self, id):
        times = QSqlQuery("SELECT (time_1, time_2, time_3) FROM racers WHERE id = " + str(id))
        times.first()
        print(times.record().field(0).value())
        if times.record().field(0).value() is None:
            return 1
        if times.record().field(1).value() is None:
            return 2
        if times.record().field(2).value() is None:
            return 3

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
