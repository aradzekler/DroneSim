import numpy as np

'''
class for defining a model.

'''


class Model:

    def __init__(self, pos):  # pos -> an [x,y] array of numbers
        self.mass = 1.0  # total mass [kg]
        self.air_dens = 1.2  # air density [kgm^-3], can defined how aerodynamic the drone is.
        self.power_pre = 1.0  # battery power [power/100]
        self.ro_rad = 0.20  # rotor radius [m]
        self.ro_area = np.pi * self.ro_rad ** 2  # rotor total area [m^2]
        self.x = pos[0]  # x coordinate
        self.y = pos[1]  # y coordinate
        self.state = 0  # the drone state, UNDEFINED
        self.type = "QUAD"  # drone type.
        # self.sensors =

    def update(self, u):
        self.u = u

    # method for computing change based on state and user input if exists.
    # def omega(self, state, inp):
