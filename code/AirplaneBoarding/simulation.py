class Simulation:
    NUMBER_OF_ACTORS = 256

    def __init__(self):
        self.actors = []
        for i in range(0,256):
            actor = actor()
            actor.id = i
            self.actors.append(actor)
        self.simulation = []
        # TODO


    def get_random_passenger(self):
        new_passenger = passengertypt

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




