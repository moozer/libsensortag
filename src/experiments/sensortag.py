from random import randint

class Sensortag():

    def __init__(self):
        pass

    def getTemp(self):
        self.__temp = randint(0,100)
        return self.__temp

