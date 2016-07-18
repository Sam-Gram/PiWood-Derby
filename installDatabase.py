#!/usr/bin/python

import sys
import time
from sqlQueries import dropQuery, createQuery, createRaceQuery, dropRaceQuery
from PySide import QtCore
from PySide.QtSql import *

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("piwood.db")
db.open()

QSqlQuery(dropQuery, db)
QSqlQuery(createQuery, db)
QSqlQuery(dropRaceQuery, db)
QSqlQuery(createRaceQuery, db)

db.close()


