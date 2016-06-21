import sys
import time
from PySide import QtCore
from PySide.QtSql import *

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("piwood.db")
db.open()

QSqlQuery("DROP TABLE IF EXISTS racers", db)
QSqlQuery("CREATE TABLE IF NOT EXISTS racers (id INTEGER PRIMARY KEY, name TEXT, time_1 INTEGER, time_2 INTEGER, time_3 INTEGER, average INTEGER, scale_speed INTEGER)", db)


