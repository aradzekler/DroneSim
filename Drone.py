import numpy as np
from pygame.math import Vector2
import pygame
import math as math
from PIL import Image

# TODO: ADD LIDARS, ADD AI, GENERICS
# TODO: SET UP GUI BUTTONS.
# lidar idea: translate map to black and white (did that) and draw a straight lines from out drone..

MAX_VELOCITY = 20
BRAKE_DEACCELERATION = 10
FREE_DEACCELERATION = 2
MAX_STEERING_ANGLE = 30


# https://www.pygame.org/project-Rect+Collision+Response-1061-.html


# UNUSED CLASS FOR NOW.
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
                turn_radius = self.length / math.tan(math.radians(self.steer))
                angular_velocity = self.velocity.x / turn_radius
            else:
                angular_velocity = 0

            self.position += self.velocity.rotate(-self.angle) * dt
            self.angle += math.degrees(angular_velocity) * dt

    # method for computing change based on state and user input if exists.
    # def omega(self, state, inp):


# collision detection function. receives the player rectangle and a collision blocks list
def collide(player_rect, collide_list):
    for block in collide_list:
        if player_rect.colliderect(block):
            return True


def deg_to_rad(deg):
    return deg / 180.0 * math.pi


class SimpleDrone:
    def __init__(self, x, y):
        self.body = pygame.image.load("Images//Body//Grey.png")
        self.rotors = pygame.image.load("Images//Wheels//Black.png")
        self.rect = self.body.get_rect()  # get rectangle the size of the body. our hitbox
        self.rect.x = x  # x location
        self.rect.y = y
        self.rect.center = self.rect.x, self.rect.y
        self.game_map = Map("future path here")
        self.lidar_sensor_range = 50
        self.front_detect_rect = self.rect
        self.front_detect_rect.x += self.lidar_sensor_range

        # sensors
        self.front_detection_lidar = False  # forward LIDAR

        # movement states for easy movement capturing.
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        self.angle = 0
        self.is_colliding = False

        # navigation variables.
        self.turn_speed = 0.5
        self.top_speed = 3
        self.acceleration = 0.1
        self.deceleration = 0.05
        self.current_speed = 0
        self.move_x = 0
        self.move_y = 0

    # setter method
    def set_rectx(self, x):
        self.rect.x = x

    def set_recty(self, y):
        self.rect.y = y

    def reset_data(self):
        self.left = False
        self.right = False
        self.forward = False
        self.backward = False
        self.front_detection_lidar = False

    # Rotation movement.
    def rotate(self):
        if self.angle > 360:
            self.angle = 0
        else:
            if self.angle < 0:
                self.angle = 360
        if self.left:
            self.angle += self.turn_speed * self.current_speed
        if self.right:
            self.angle -= self.turn_speed * self.current_speed

    def move(self):
        if self.forward:
            if self.current_speed < self.top_speed:
                self.current_speed += self.acceleration
        else:
            if self.current_speed > 0:
                self.current_speed -= self.deceleration
            else:
                self.current_speed = 0
        angle_rad = deg_to_rad(self.angle)
        self.move_x = -(float(self.current_speed * math.sin(angle_rad)))
        self.move_y = -(float(self.current_speed * math.cos(angle_rad)))
        self.rect.x += self.move_x
        self.rect.y += self.move_y

    def display(self, main_surface):
        temp_image = pygame.transform.rotate(self.body, self.angle)
        main_surface.blit(temp_image, (self.rect.x, self.rect.y))
        temp_image = pygame.transform.rotate(self.rotors, self.angle)
        main_surface.blit(temp_image, (self.rect.x, self.rect.y))

    def update(self):
        self.move_x = 0
        self.move_y = 0
        if collide(self.rect, self.game_map.collidelist):
            self.is_colliding = True

        self.rotate()
        self.move()
        self.reset_data()


# Main class for dealing with out map.
class Map:
    def __init__(self, path):
        self.path = path
        self.map_width = 0
        self.map_height = 0
        self.collidelist = []

        # self.map_array = array([self.map_width][self.map_height])
        with Image.open("Images//p15.png") as img:
            self.map_width, self.map_height = img.size
            rgb_image = img.convert("RGB")

            self.map_array = []
            for i in range(self.map_width):
                self.map_array.append([])
                for j in range(self.map_height):
                    self.map_array[i].append(0)
            for x in range(self.map_width):
                for y in range(self.map_height):
                    rgb_pixel_value = rgb_image.getpixel((x, y))
                    if rgb_pixel_value != (255, 255, 255):  # if not completly white, turn black
                        img.putpixel((x, y), (0, 0, 0))
                        self.block = pygame.Rect(x, y, 1, 1)
                        self.collidelist.append(self.block)
                        self.map_array[x][y] = (0, 0, 0)
                    self.map_array[x][y] = (255, 255, 255)
            img.save("new_map.png")
