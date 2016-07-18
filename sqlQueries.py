# This file contains all the needed SQL queries that run the PiWood Derby

dropQuery = "DROP TABLE IF EXISTS racers;"
createQuery = "CREATE TABLE IF NOT EXISTS racers (id INTEGER PRIMARY KEY, name TEXT, time_1 REAL, time_2 REAL, time_3 REAL, average INTEGER, scale_speed INTEGER);"
insertEmptyRacerQuery = "INSERT INTO racers (name, time_1, time_2, time_3, average, scale_speed) VALUES (NULL, NULL, NULL, NULL, NULL, NULL);"

createRaceQuery = "CREATE TABLE IF NOT EXISTS race_num (num INTEGER); INSERT INTO race_num (num) VALUES (-1);"
dropRaceQuery = "DROP TABLE IF EXISTS race_num;"
incrementRaceQuery = "UPDATE race_num SET num = num + 1;"
getRaceNumQuery = "SELECT num FROM race_num;"
getNumberOfRacersQuery = "SELECT COUNT(*) FROM racers;"
