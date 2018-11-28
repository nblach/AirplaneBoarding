import pygame


class Animation:

    def __init__(self, sim):

        self.simulation = sim

        #initialize constants
        self.PIXELS_PER_UNIT = 0.05
        self.SPACE_HORIZONTAL = 20
        self.SPACE_VERTICAL = 20
        self.WIDTH_AISLE = 40
        self.WIDTH_SEAT = 30
        self.WIDTH_WALL = 10
        self.WIDTH_PLANE = 2*self.WIDTH_WALL+self.WIDTH_AISLE+ (sim.plane.seatsLeft + sim.plane.seatsRight)*self.WIDTH_SEAT
        self.V_OFFSET_AISLE = self.SPACE_VERTICAL + self.WIDTH_WALL +  self.WIDTH_SEAT*sim.plane.seatsRight
        self.LENGTH_ROW = self.units_to_pixels(self.simulation.plane.length_of_row)
        #TODO calculate length seat properly
        self.LENGTH_SEAT = self.LENGTH_ROW - 10 # should be shorter than row length
        self.LENGTH_NOSE = 90
        self.LENGTH_TAIL = 80
        self.H_OFFSET_FIRST_ROW = self.SPACE_HORIZONTAL + self.LENGTH_NOSE
        self.WIDTH_COMPARTMENT = 35
        self.LENGTH_COMPARTMENT = self.units_to_pixels(self.simulation.plane.compartment_length)


        # initialize window and load images
        pygame.init()
        self.nose = pygame.image.load('img/nose.png')
        self.tail = pygame.image.load('img/tail.png')
        self.seat_empty = pygame.image.load('img/seat_empty.png')
        self.seat_occupied = pygame.image.load('img/seat_occupied.png')
        self.aisle = pygame.image.load('img/aisle.png')
        self.passenger_walk = pygame.image.load('img/passenger_walk.png')
        self.passenger_store = pygame.image.load('img/passenger_store.png')
        self.passenger_wait = pygame.image.load('img/passenger_wait.png')
        self.wall = pygame.image.load('img/wall.png')
        self.luggage_1 = pygame.image.load('img/luggage_1.png')
        self.luggage_2 = pygame.image.load('img/luggage_2.png')
        self.luggage_3 = pygame.image.load('img/luggage_3.png')
        self.switch_overlay = pygame.image.load('img/switch_overlay.png')
        self.compartment_0 = pygame.image.load('img/compartment_0.png')
        self.compartment_1 = pygame.image.load('img/compartment_1.png')
        self.compartment_2 = pygame.image.load('img/compartment_2.png')
        self.compartment_3 = pygame.image.load('img/compartment_3.png')
        self.compartment_4 = pygame.image.load('img/compartment_4.png')
        self.compartment_5 = pygame.image.load('img/compartment_5.png')
        self.compartment_6 = pygame.image.load('img/compartment_6.png')
        self.compartment_7 = pygame.image.load('img/compartment_7.png')
        self.compartment_8 = pygame.image.load('img/compartment_8.png')
        self.compartment_9 = pygame.image.load('img/compartment_9.png')
        self.compartment_10 = pygame.image.load('img/compartment_10.png')
        self.compartment_delete = pygame.image.load('img/compartment_delete.png')

        # adjust image sizes
        self.wall = pygame.transform.scale(self.wall, (sim.plane.rows * self.LENGTH_ROW, self.WIDTH_WALL))
        self.nose = pygame.transform.scale(self.nose, (self.LENGTH_NOSE, self.WIDTH_PLANE))
        self.tail = pygame.transform.scale(self.tail, (self.LENGTH_TAIL, self.WIDTH_PLANE))
        self.seat_empty = pygame.transform.scale(self.seat_empty, (self.LENGTH_SEAT, self.WIDTH_SEAT-1))
        self.seat_occupied = pygame.transform.scale(self.seat_occupied, (self.LENGTH_SEAT, self.WIDTH_SEAT-1))
        self.aisle = pygame.transform.scale(self.aisle, (self.LENGTH_ROW, self.WIDTH_AISLE))
        self.compartment_0 = pygame.transform.scale(self.compartment_0, (self.LENGTH_COMPARTMENT, self.WIDTH_COMPARTMENT))
        self.compartment_1 = pygame.transform.scale(self.compartment_1, (self.LENGTH_COMPARTMENT, self.WIDTH_COMPARTMENT))
        self.compartment_2 = pygame.transform.scale(self.compartment_2, (self.LENGTH_COMPARTMENT, self.WIDTH_COMPARTMENT))
        self.compartment_3 = pygame.transform.scale(self.compartment_3, (self.LENGTH_COMPARTMENT, self.WIDTH_COMPARTMENT))
        self.compartment_4 = pygame.transform.scale(self.compartment_4, (self.LENGTH_COMPARTMENT, self.WIDTH_COMPARTMENT))
        self.compartment_5 = pygame.transform.scale(self.compartment_5, (self.LENGTH_COMPARTMENT, self.WIDTH_COMPARTMENT))
        self.compartment_6 = pygame.transform.scale(self.compartment_6, (self.LENGTH_COMPARTMENT, self.WIDTH_COMPARTMENT))
        self.compartment_7 = pygame.transform.scale(self.compartment_7, (self.LENGTH_COMPARTMENT, self.WIDTH_COMPARTMENT))
        self.compartment_8 = pygame.transform.scale(self.compartment_8, (self.LENGTH_COMPARTMENT, self.WIDTH_COMPARTMENT))
        self.compartment_9 = pygame.transform.scale(self.compartment_9, (self.LENGTH_COMPARTMENT, self.WIDTH_COMPARTMENT))
        self.compartment_10 = pygame.transform.scale(self.compartment_10, (self.LENGTH_COMPARTMENT, self.WIDTH_COMPARTMENT))
        self.compartment_delete = pygame.transform.scale(self.compartment_delete, (self.LENGTH_COMPARTMENT, self.WIDTH_COMPARTMENT))

        # initialize window
        self.size = (self.H_OFFSET_FIRST_ROW+self.LENGTH_TAIL+self.SPACE_HORIZONTAL*2 + sim.plane.rows * self.LENGTH_ROW, 2*self.SPACE_VERTICAL + self.WIDTH_PLANE + self.WIDTH_COMPARTMENT)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Airplane Boarding Model")
        self.screen.fill([255,255,255])
        self.print_empty_plane()
        pygame.display.flip()






    def animate(self, speed):
        self.print_empty_plane()
        pygame.display.flip()

        clock = pygame.time.Clock()

        # wait for signal to start
        start = False
        while(not start):
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        start = True
                if e.type == pygame.QUIT:
                    self.exit()
                    return

        pause = False
        for i in range(0, int(len(self.simulation.simulation)/speed)):
            # check if quit/pause
            for e in pygame.event.get():
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_SPACE:
                            pause = not pause
                        if e.key == pygame.K_ESCAPE:
                            self.exit()
                            return
                    if e.type == pygame.QUIT:
                        self.exit()
                        return
            while pause:
                for e in pygame.event.get():
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_SPACE:
                            pause = not pause
                        if e.key == pygame.K_ESCAPE:
                            self.exit()
                            return
                    if e.type == pygame.QUIT:
                        self.exit()
                        return

            clock.tick(10)
            index = i*speed
            self.display_frame(index)

        self.display_frame(len(self.simulation.simulation) -1)
        print('done')

        #free aisle
        for i in range(0, self.simulation.plane.rows):
            x = self.H_OFFSET_FIRST_ROW+i*self.LENGTH_ROW
            self.screen.blit(self.aisle, (x, self.V_OFFSET_AISLE))
        pygame.display.flip()



        # wait for signal to end
        end = False
        while(not end):
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.exit()
                    return
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    end = True


    def display_frame(self, index):
        #free aisle
        for i in range(0, self.simulation.plane.rows):
            x = self.H_OFFSET_FIRST_ROW+i*self.LENGTH_ROW
            self.screen.blit(self.aisle, (x, self.V_OFFSET_AISLE))


        # display all actors
        for a in range(0, self.simulation.number_of_actors):
            arr = self.simulation.simulation[index][0][a]
            # if actor not in plane, do not display them
            if arr[0] == -1:
                continue
            self.display_passenger(arr[0], arr[1], arr[2], self.units_to_pixels(self.simulation.plane.actors[a].passenger_type.size) ,arr[3], a)



        for c in range(0, self.simulation.plane.nr_compartments):
            self.display_compartment(self.simulation.simulation[index][1][c], c)

        pygame.display.flip()




    def exit(self):
        pygame.display.quit()
        pygame.quit()



    def print_empty_plane(self):
        # display nose, tail and wall
        self.screen.blit(self.nose, (self.SPACE_HORIZONTAL, self.SPACE_VERTICAL))
        self.screen.blit(self.tail, (self.H_OFFSET_FIRST_ROW + self.simulation.plane.rows * self.LENGTH_ROW, self.SPACE_VERTICAL))
        self.screen.blit(self.wall, (self.H_OFFSET_FIRST_ROW, self.SPACE_VERTICAL))
        self.screen.blit(self.wall, (self.H_OFFSET_FIRST_ROW + self.simulation.plane.rows * self.LENGTH_ROW, self.SPACE_VERTICAL))

        #display rows and aisle
        for i in range(0, self.simulation.plane.rows):
            x = self.H_OFFSET_FIRST_ROW+i*self.LENGTH_ROW
            y_top = self.SPACE_VERTICAL + self.WIDTH_WALL

            for j in range(0, self.simulation.plane.seatsRight):
                self.screen.blit(self.seat_empty, (x, y_top + j*self.WIDTH_SEAT))
            self.screen.blit(self.aisle, (x, self.V_OFFSET_AISLE))
            for j in range(0, self.simulation.plane.seatsLeft):
                self.screen.blit(self.seat_empty, (x, y_top + (j+self.simulation.plane.seatsRight)*self.WIDTH_SEAT + self.WIDTH_AISLE))

        #display compartments
        for c in range(0, self.simulation.plane.nr_compartments):
                self.display_compartment(self.simulation.simulation[0][1][c], c)




    def units_to_pixels(self, x):
        return int(self.PIXELS_PER_UNIT*x)


    def display_passenger(self, position, action, luggage, length, switching, id):

        size = (length, self.WIDTH_AISLE)
       #check if seated
        if action == 0:
           return
        elif action == 5:
           #passenger is seated
           self.display_occ_seat(id)
           return
        elif action == 2:
            p = pygame.transform.scale(self.passenger_store, size)
        elif action == 4:
            p = pygame.transform.scale(self.passenger_wait, size)
        else:
            p = pygame.transform.scale(self.passenger_walk, size)

        self.screen.blit(p, (self.H_OFFSET_FIRST_ROW + self.units_to_pixels(position), self.V_OFFSET_AISLE))

        if luggage > 0:
            if luggage == 1:
                l = pygame.transform.scale(self.luggage_1, size)
            elif luggage == 2:
                l = pygame.transform.scale(self.luggage_2, size)
            elif luggage == 3:
                l = pygame.transform.scale(self.luggage_3, size)
            self.screen.blit(l, (self.H_OFFSET_FIRST_ROW + self.units_to_pixels(position), self.V_OFFSET_AISLE))
        if switching:
            s = pygame.transform.scale(self.switch_overlay, size)
            self.screen.blit(s, (self.H_OFFSET_FIRST_ROW + self.units_to_pixels(position), self.V_OFFSET_AISLE))


    def display_compartment(self, capacity, i):
        y  = self.V_OFFSET_AISLE + self.WIDTH_AISLE + self.simulation.plane.seatsLeft * self.WIDTH_SEAT + self.WIDTH_WALL
        x = self.H_OFFSET_FIRST_ROW + i*self.LENGTH_COMPARTMENT
        self.screen.blit(self.compartment_delete, (x,y))
        if capacity == 0:
            self.screen.blit(self.compartment_0, (x, y))
        elif capacity == 1:
            self.screen.blit(self.compartment_1, (x, y))
        elif capacity == 2:
            self.screen.blit(self.compartment_2, (x, y))
        elif capacity == 3:
            self.screen.blit(self.compartment_3, (x, y))
        elif capacity == 4:
            self.screen.blit(self.compartment_4, (x, y))
        elif capacity == 5:
            self.screen.blit(self.compartment_5, (x, y))
        elif capacity == 6:
            self.screen.blit(self.compartment_6, (x, y))
        elif capacity == 7:
            self.screen.blit(self.compartment_7, (x, y))
        elif capacity == 8:
            self.screen.blit(self.compartment_8, (x, y))
        elif capacity == 9:
            self.screen.blit(self.compartment_9, (x, y))
        elif capacity == 10:
            self.screen.blit(self.compartment_10, (x, y))



    def display_occ_seat(self, id):
        x = self.H_OFFSET_FIRST_ROW + self.simulation.actors[id].seat.row_number*self.LENGTH_ROW

        col_nr = self.simulation.actors[id].seat.col_number

        if col_nr < self.simulation.plane.seatsLeft:
            y = self.V_OFFSET_AISLE + self.WIDTH_AISLE + (self.simulation.plane.seatsLeft-1-col_nr) * self.WIDTH_SEAT
        else:
            y = self.V_OFFSET_AISLE - (1+col_nr-self.simulation.plane.seatsLeft) * self.WIDTH_SEAT

        self.screen.blit(self.seat_occupied, (x,y))
