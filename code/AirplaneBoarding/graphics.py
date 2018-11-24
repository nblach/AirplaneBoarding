from simulation import Simulation
import simulation
import pygame
import numpy as np


class Animation:

    def __init__(self, sim):

        self.simulation = sim

        #initialize constants
        self.PIXELS_PER_UNIT = 0.025
        self.SPACE_HORIZONTAL = 20
        self.SPACE_VERTICAL = 20
        self.WIDTH_AISLE = 40
        self.WIDTH_SEAT = 30
        self.WIDTH_WALL = 10
        self.WIDTH_PLANE = 2*self.WIDTH_WALL+self.WIDTH_AISLE+ (sim.plane.seatsLeft + sim.plane.seatsRight)*self.WIDTH_SEAT
        self.V_OFFSET_AISLE = self.SPACE_VERTICAL + self.WIDTH_WALL +  self.WIDTH_SEAT*sim.plane.seatsRight
        self.LENGTH_ROW = self.units_to_pixels(self.simulation.plane.length_of_row)
        self.LENGTH_SEAT = 10 # should be shorter than row length
        self.LENGTH_NOSE = 90
        self.LENGTH_TAIL = 80
        self.H_OFFSET_FIRST_ROW = self.SPACE_HORIZONTAL + self.LENGTH_NOSE
        self.WIDTH_COMPARTMENT = 35
        self.LENGTH_COMPARTMENT = self.units_to_pixels(self.simulation.plane.compartment_length)


        # initialize window and load images
        pygame.init()
        self.nose = pygame.image.load('nose.png')
        self.tail = pygame.image.load('tail.png')
        self.seat_empty = pygame.image.load('seat_empty.png')
        self.seat_occupied = pygame.image.load('seat_occupied.png')
        self.aisle = pygame.image.load('aisle.png')
        self.passenger_walk = pygame.image.load('passenger_walk.png')
        self.passenger_store = pygame.image.load('passenger_store.png')
        self.passenger_wait = pygame.image.load('passenger_wait.png')
        self.wall = pygame.image.load('wall.png')
        self.luggage_1 = pygame.image.load('luggage_1.png')
        self.luggage_2 = pygame.image.load('luggage_2.png')
        self.luggage_3 = pygame.image.load('luggage_3.png')
        self.switch_overlay = pygame.image.load('switch_overlay.png')
        self.compartment_0 = pygame.image.load('compartment_0.png')
        self.compartment_1 = pygame.image.load('compartment_1.png')
        self.compartment_2 = pygame.image.load('compartment_2.png')
        self.compartment_3 = pygame.image.load('compartment_3.png')
        self.compartment_4 = pygame.image.load('compartment_4.png')
        self.compartment_5 = pygame.image.load('compartment_5.png')
        self.compartment_6 = pygame.image.load('compartment_6.png')
        self.compartment_7 = pygame.image.load('compartment_7.png')
        self.compartment_8 = pygame.image.load('compartment_8.png')
        self.compartment_9 = pygame.image.load('compartment_9.png')
        self.compartment_10 = pygame.image.load('compartment_10.png')

        # adjust image sizes
        self.wall = pygame.transform.scale(self.wall, (sim.plane.rows * self.LENGTH_ROW, self.WIDTH_WALL))
        self.nose = pygame.transform.scale(self.nose, (self.LENGTH_NOSE, self.WIDTH_PLANE))
        self.tail = pygame.transform.scale(self.tail, (self.LENGTH_TAIL, self.WIDTH_PLANE))
        self.seat_empty = pygame.transform.scale(self.seat_empty, (self.LENGTH_SEAT, self.WIDTH_SEAT))
        self.seat_occupied = pygame.transform.scale(self.seat_occupied, (self.LENGTH_SEAT, self.WIDTH_SEAT))
        self.aisle = pygame.transform.scale(self.aisle, (self.LENGTH_ROW, self.WIDTH_AISLE))


        # initialize window
        self.size = (self.H_OFFSET_FIRST_ROW+self.LENGTH_TAIL+self.SPACE_HORIZONTAL*2 + sim.plane.rows * self.LENGTH_ROW, 2*self.SPACE_VERTICAL + self.WIDTH_PLANE + self.WIDTH_COMPARTMENT)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Airplane Boarding Model")

        self.print_empty_plane()






    def animate(self, speed):
        self.print_empty_plane()
        pygame.display.flip()

        clock = pygame.time.Clock()

        # TODO wait for signal to start

        for i in range(0, int(len(simulation.simulation)/speed)):
            # TODO display every actor
            # TODO display every compartment


        # TODO wait for signal to end








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
            for j in range(0, self.simulation.plane.seatsRight):
                self.screen.blit(self.seat_empty, (x, y_top + (j+self.simulation.plane.seatsRight)*self.WIDTH_SEAT + self.WIDTH_AISLE))

        #display compartments
        # TODO





    def units_to_pixels(self, x):
        return int(self.PIXELS_PER_UNIT*x)


    def display_passenger(self, position, action, luggage, length, switching):
        size = (length, self.WIDTH_AISLE)
        if action == 2:
            p = pygame.transform.scale(self.passenger_store, size)
        elif action == 4:
            p = pygame.transform.scale(self.passenger_wait, size)
        else:
            p = pygame.transform.scale(self.passenger_walk, size)

        self.screen.blit(p, (self.H_OFFSET_FIRST_ROW + self.units_to_pixels(position), self.V_OFFSET_AISLE))


    def display_compartment(self, capacity, i):
        y  = self.V_OFFSET_AISLE + self.WIDTH_AISLE + self.simulation.plane.seatsLeft * self.WIDTH_PLANE + self.WIDTH_WALL
        x = self.H_OFFSET_FIRST_ROW + i*self.LENGTH_COMPARTMENT
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