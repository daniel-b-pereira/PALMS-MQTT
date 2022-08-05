
import time # timestamp for id generation
from random import randint # random number for id generation


class PetriNet:

    def __init__(self):
        #generate a unique id
        self.id = ("PetriNet" + str(time.time())) + str(randint(0, 1000))
        self.arcs = [] # List or arcs
        self.transitions = {} # Map of transitions. Key: transition id, Value: event
        self.places = {} # Map of places. Key: place id, Value: place
        self.name =''
        self.len_places = 0
        self.len_transitions = 0

        self.marking = list()
        self._marking = list()
        self._matrix= list()



    def incidence_matrix(self):
        if self.len_places==0 or self.len_transitions ==0:
            return None
        self._matrix = list()
        for place in self.places.values():
            _row = list()
            self._marking.append(place.marking)
            for transition in self.transitions.values():
                a_ij = 0
                for arc in self.arcs:
                    a_ij = arc.find_element(place.id,transition.id)
                    if a_ij==1 or a_ij==-1:
                        break
                _row.append(a_ij)
            self._matrix.append(_row)     
        return self._marking, self._matrix                
                

    def mount_marking(self, marking_vector):
        count = 0
        if len(marking_vector) ==self.len_places :
            for place in self.places.values():
                place.set_marking( marking_vector[count])
                count+=1


    def set_len_place(self):
        self.len_places+=1


    def set_len_transition(self):
        self.len_transitions+=1


    def reset_len(self):
        self.len_places = 0
        self.len_transitions = 0


    def __str__(self):
        text = '--- Net: ' + self.name + '\nTransitions: '
        for transition in self.transitions.values():
            text += str(transition) + ' '
        text += '\nPlaces: '
        for place in self.places.values():
            text += str(place) + ' '
        text += '\n'
        for arc in self.arcs:
                text += str(arc) + '\n'
        text += '---'
        return text

