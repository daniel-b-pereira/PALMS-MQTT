
import time # timestamp for id generation
from random import randint # random number for id generation


class Arc:

    def __init__(self):
        #generate a unique id
        self.id = ("Arc" + str(time.time())) + str(randint(0, 1000))
        self.source = None # id of the source event of this arc
        self.target = None # id of the target event of this arc
        self.type = 'normal' # id of the type of this arc
        self.inscription = "1" # inscription of this arc
        self.net = None # Reference to net object for label resolution of source an target
        self.a_ij = dict() # Reference to a_ij element -1 for Place -> Transition and 1 for Transition-> Place


    def find_source(self):
        if self.source in self.net.transitions:
            self.matrix = {int(self.source):1}
            return self.net.transitions[self.source]
        else:
            return self.net.places[self.source]


    def find_target(self):
        if self.target in self.net.transitions:
            self.a_ij = {int(self.target):-1}
            return self.net.transitions[self.target]
        else:
            return self.net.places[self.target]

    def find_element(self, place_id, transition_id,):
            if transition_id == self.source and place_id == self.target:
                return 1
            elif transition_id == self.target and place_id ==self.source:
                return -1
            else:
                return 0


    def get_a_ij(self):
        return self.a_ij


    def __str__(self):
        return str(self.find_source()) + "-->" + str(self.find_target()) +"\n"
