# This utility function comes up with which racers to use in the next race

def racerCalculator(raceNum, numCars):
    f = lambda x : (raceNum*3+x) % numCars
    return f(0),f(1),f(2)
