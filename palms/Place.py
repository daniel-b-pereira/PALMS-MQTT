
import time # timestamp for id generation
from random import randint # random number for id generation

class Place:
   
    def __init__(self):
        self.label = "Place" # default label of event
        #generate a unique id
        self.id = ("Place" + str(time.time())) + str(randint(0, 1000))
        self.offset = [0, 0]
        self.position = [0, 0]
        self.marking = 0


    def set_marking(self,marking):
          self.marking = marking
    def __str__(self):
        return self.label