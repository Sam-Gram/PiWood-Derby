# This file contains all the needed SQL queries that run the PiWood Derby

dropQuery = "DROP TABLE IF EXISTS racers;"
createQuery = "CREATE TABLE IF NOT EXISTS racers (id INTEGER PRIMARY KEY, name TEXT, time_1 INTEGER, time_2 INTEGER, time_3 INTEGER, average INTEGER, scale_speed INTEGER);"
insertEmptyRacerQuery = "INSERT INTO racers (name, time_1, time_2, time_3, average, scale_speed) VALUES (NULL, NULL, NULL, NULL, NULL, NULL);"

