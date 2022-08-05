
import time # timestamp for id generation
from random import randint # random number for id generation

class Transition:
 
    def __init__(self):
        self.label = "Transition" # default label of event
        #generate a unique id
        self.id = ("Transition" + str(time.time())) + str(randint(0, 1000))
        self.offset = [0, 0]
        self.position = [0, 0]

    def __str__(self):
        return self.label

