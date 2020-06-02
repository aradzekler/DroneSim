import numpy as np
from pygame.math import Vector2
import pygame
from pygame.color import THECOLORS
import math as math
from PIL import Image
import easygui as eg  # https://github.com/robertlugg/easygui   - easy way to open file dialog and other gui things.
import Model_States

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
        self.state = Model_States.ManualState()  # the drone state, 0 is manual
        self.type = "QUAD"  # drone type.
        self.steer = 0.0
        self.acceleration = 0.0

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



# collision detection function. receives the player rectangle and a collision blocks list
def collide(player_rect, collide_list):
    for block in collide_list:
        if player_rect.colliderect(block):
            return True


# function for converting degrees to radians.
def deg_to_rad(deg):
    return deg / 180.0 * math.pi


# adding a "sonar arm", which will detect movement in a straight line from origin
def make_sonar_arm(x, y):
    spread = 10  # Default spread.
    sensor_distance = 15  # Gap before first sensor.
    arm_points = []
    for i in range(1, sensor_distance):
        arm_points.append((x + (spread * i), y))

    return arm_points


# reads if the current reading is a wall or not.
def get_track_or_not(reading):
    if reading == THECOLORS['black']:
        return 0
    else:
        return 1


# our main drone class for now., getting a starting x and y coordinations, screen - pygame.display (our game
# 'canvas'), gamemap - our Map object
class SimpleDrone:
    def __init__(self, x, y, screen, game_map):
        self.body = pygame.image.load("Images//Body//Grey.png").convert()  # images for the model itself.
        self.rotors = pygame.image.load("Images//Wheels//Black.png").convert()
        self.rect = self.body.get_rect()  # get rectangle the size of the body. our hitbox
        self.rect.x = x  # x location
        self.rect.y = y
        self.game_map = game_map
        self.screen = screen
        self.rect.center = self.rect.x, self.rect.y  # center point of our drone
        self.state = Model_States.ManualState  # the drone state, 0 is manual

        self.front_detect_rect = self.rect  # drone front

        # self.driving_direction = Vec2d(1, 0).rotated(self.angle)

        # sensors
        self.front_detection_lidar = False  # forward LIDAR
        self.show_sensors = True
        self.lidar_sensor_range = 50
        self.front_detect_rect.x += self.lidar_sensor_range

        # movement states for easy movement capturing.
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        self.angle = 0
        self.is_colliding = False  # collision detection param

        # navigation variables.
        # TODO: determine actual speed ( in meters/sec or something, not in arbitrary values
        self.turn_speed = 0.5
        self.top_speed = 3
        self.acceleration = 0.1
        self.deceleration = 0.05
        self.current_speed = 0
        self.move_x = 0
        self.move_y = 0

    def on_event(self, event):
        """
        This is the bread and butter of the state machine. Incoming events are
        delegated to the given states which then handle the event. The result is
        then assigned as the new state (implementation in Model_States.py.
        """

        # The next state will be the result of the on_event function.
        self.state = self.state.on_event(event)

    # setter methods for rectx and recty
    def set_rect_x(self, x):
        self.rect.x = x

    def set_rect_y(self, y):
        self.rect.y = y

    # resetting variables.
    def reset_data(self):
        self.left = False
        self.right = False
        self.forward = False
        self.backward = False
        self.front_detection_lidar = False

    # Rotation movement angle.
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

    # actual movement
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

    # display the drone on the map.
    def display(self, main_surface):
        temp_image = pygame.transform.rotate(self.body, self.angle)
        main_surface.blit(temp_image, (self.rect.x, self.rect.y))
        temp_image = pygame.transform.rotate(self.rotors, self.angle)
        main_surface.blit(temp_image, (self.rect.x, self.rect.y))
        readings = self.get_sonar_readings(self.rect.x, self.rect.y, main_surface)

    # updating function for movement
    def update(self):
        self.move_x = 0  # no momentum
        self.move_y = 0
        if collide(self.rect, self.game_map.collide_list):
            self.is_colliding = True

        self.rotate()
        self.move()
        self.reset_data()

    # not ready
    def front_det(self):
        if self.game_map[self.rect.x + 50][self.rect.y] == (0, 0, 0):
            fuck = 0

    # TODO: PROBLEM! something isnt right in the formula for calculating the angle
    # TODO: ALSO, 2 arms arent showing when switching x_change and y_change to radians
    def get_rotated_point(self, x_1, y_1, x_2, y_2, angle):
        radians = math.radians(angle)
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(angle) + (y_2 - y_1) * math.sin(angle)
        y_change = (y_1 - y_2) * math.cos(angle) - (x_1 - x_2) * math.sin(angle)
        new_x = x_change + x_1
        new_y = y_change + y_1
        return int(new_x), int(new_y)

    # sonar detection function
    def get_arm_distance(self, arm, x, y, offset, screen):
        # Used to count the distance.
        i = 0

        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1

            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], self.angle + offset)

            # Check if we've hit something. Return the current i (distance) if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= self.game_map.map_width or rotated_p[1] >= self.game_map.map_height:
                print(i)
                return i  # Sensor is off the screen.
            else:
                obs = screen.get_at(rotated_p)
                if get_track_or_not(obs) != 0:
                    return i

            if self.show_sensors:
                pygame.draw.circle(screen, (255, 0, 255), rotated_p, 2)

        # Return the distance for the arm.
        return i

    # display arms on map
    def get_sonar_readings(self, x, y, screen):
        readings = []

        # Make our arms.
        arm_left = make_sonar_arm(x, y)
        arm_middle = arm_left
        arm_right = arm_left

        # Rotate them and get readings.
        readings.append(self.get_arm_distance(arm_left, x, y, 0.75, screen))
        readings.append(self.get_arm_distance(arm_middle, x, y, 0, screen))
        readings.append(self.get_arm_distance(arm_right, x, y, -0.75, screen))

        if self.show_sensors:
            pygame.display.update()

        return readings


# Main class for dealing with out map.
class Map:
    def __init__(self):
        self.map_width = 0
        self.map_height = 0
        self.collide_list = []  # a list full of all the 'black spots'/walls
        map_path = eg.fileopenbox()  # opens a file choosing dialog.

        # self.map_array = array([self.map_width][self.map_height])
        with Image.open(map_path) as self.img:  # open the chosen map file as image.
            self.map_width, self.map_height = self.img.size  # size of map.
            rgb_image = self.img.convert("RGB")

            self.map_array = []
            for i in range(self.map_width):
                self.map_array.append([])
                for j in range(self.map_height):
                    self.map_array[i].append(0)
            for x in range(self.map_width):
                for y in range(self.map_height):
                    rgb_pixel_value = rgb_image.getpixel((x, y))
                    if rgb_pixel_value != (
                            255, 255, 255):  # if not completly white, turn black (colored - walls, white - path)
                        self.img.putpixel((x, y), (0, 0, 0))
                        self.block = pygame.Rect(x, y, 1, 1)
                        self.collide_list.append(self.block)
                        self.map_array[x][y] = (0, 0, 0)
                    self.map_array[x][y] = (255, 255, 255)
            self.img.save("new_map.png")
