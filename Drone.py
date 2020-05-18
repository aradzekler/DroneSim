import numpy as np
from pygame.math import Vector2
import math as math
'''
class for defining a model.

'''

MAX_VELOCITY = 20
BRAKE_DEACCELERATION = 10
FREE_DEACCELERATION = 2
MAX_STEERING_ANGLE = 30


class Model:

    def __init__(self, x, y):  # pos -> an [x,y] array of numbers
        self.mass = 1.0  # total mass [kg]
        self.air_dens = 1.2  # air density [kgm^-3], can defined how aerodynamic the drone is.
        self.power_pre = 1.0  # battery power [power/100]
        self.angle = 0.0  # angle of drone. in deg.
        self.velocity = Vector2(0.0, 0.0)  # vertical , horizontal speed.
        self.ro_rad = 0.20  # rotor radius [m]
        self.length = 0.5  # drone have a diameter of 0.5m
        self.ro_area = np.pi * self.ro_rad ** 2  # rotor total area [m^2]
        self.position = Vector2(x, y)
        self.state = 0  # the drone state, 0 is manual
        self.type = "QUAD"  # drone type.
        self.steer = 0.0
        self.acceleration = 0.0
        # self.sensors =

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-MAX_VELOCITY, min(self.velocity.x, MAX_VELOCITY))

        if self.state == 0:
            if self.steer:
                turn_radius = self.length/math.tan(math.radians(self.steer))
                angular_velocity = self.velocity.x / turn_radius
            else:
                angular_velocity = 0

            self.position += self.velocity.rotate(-self.angle) * dt
            self.angle += math.degrees(angular_velocity) * dt


    # method for computing change based on state and user input if exists.
    # def omega(self, state, inp):
