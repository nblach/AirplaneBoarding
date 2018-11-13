class Simulation:

    def __init__(self):
        self.actors = []
        self.simulation = []
        # TODO



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




