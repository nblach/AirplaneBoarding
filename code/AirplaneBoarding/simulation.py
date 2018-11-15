import numpy
from passenger_type import Passenger_Type
from actor import Actor


PASSENGER_SIZE = 10;

class Simulation:


    def __init__(self, number_of_actors, plane, seat_assignment_id):

        #TODO
        #generate seat_assingment

        self.actors = []
        self.plane = plane
        self.number_of_actors = number_of_actors

        #fill actors[] with random actors
        for i in range(0, self.number_of_actors):
            actor = Actor(i, self.get_random_passenger(), seat_assignment[i], 0, plane)
            self.actors.append(actor)


        #simulation[] will contain all states observed during simulation (in order)
        self.simulation = []
        # TODO

    """
    Passenger moving speed data is given in from of a triangular distribution (it was recoded for Short Haul airplanes):
        passing_one_row_seconds = [1.8, 2.4, 3.0]
        install_in_seat_seconds = [6.0, 9.0, 30.0]
        exit_from_seat_into_aisle = [3.0, 3.6, 4.2]
    Passenger luggage load is chosen by us, so we can have different set ups. 
    In the paper they had two options normal and high load. 
    """

    @staticmethod
    def get_random_passenger():
        moving_speed = [numpy.random.triangular(1.8, 2.4, 3.0), numpy.random.triangular(6.0, 9.0, 30.0),
                        numpy.random.triangular(3.0, 3.6, 4.2)]
        number_of_bags_possibilities = [1, 2, 3]
        load_probabilities = [[0.6, 0.3, 0.1], [0.2, 0.6, 0.2]]
        number_of_bags = numpy.random.choice(number_of_bags_possibilities, p=load_probabilities[0])
        return Passenger_Type(number_of_bags, moving_speed, PASSENGER_SIZE)

    def get_seat(self):
        return

    def simulate(self):
        done = 0;
        i = 0;

        while (not done):
            j = 0;
            for a in self.actors:
               a.act()
               self.simulation[i][j] = [a.position, a.action]
               j += 1

            i += 1




