
import math as math
import pygame
import constants
from helpers import deg_to_rad
from interfaces.pygame_object_interface import PyGameObjectInterface

SENSOR_RANGE = 10
D_BLACK = (0, 0, 0, 255)

# Our lidar sensor
class TofSensor():
    def __init__(self,drone,offset):
        self.drone=drone
        self.arm_points = []
        self.offset = offset


     # adding a "sonar arm", which will detect movement in a straight line from origin
    def update(self):
        spread = 10  # Default spread (distance between every sonar arm)
        arm_points = []
        for i in range(0, SENSOR_RANGE):
            arm_points.append(  # painting the 'dots' of the arm relative to our drone location
                (self.drone.rect.x + self.drone.sensor_x_relative + (spread * i), self.drone.rect.y + self.drone.sensor_y_relative))

        self.arm_points = arm_points


    # sonar detection function
    # TODO draw must be separated from logic!!!
    def display(self):
        i = 0  # Used to count the distance.
        # Look at each point and see if we've hit something.
        for point in self.arm_points:
            i += 1
            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                self.drone.rect.x + self.drone.sensor_x_relative, self.drone.rect.y + self.drone.sensor_y_relative, point[0], point[1],
                self.drone.angle + self.offset)
            #TODO remove dependency to main, drone must be surface too
            pygame.draw.circle(self.drone.main.main_s, (255, 0, 255), rotated_p, 1)  # drawing sonar arms.
            rotated_list_p = list(rotated_p)
            rotated_list_p[0] += 1  # nasty workaround to change the tuple rotated_p value in order to 'see' the white
            # and not purple.
            rotated_p = tuple(rotated_list_p)
            # Check if we've hit something.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= self.drone.game_map.map_width or rotated_p[1] >= self.drone.game_map.map_height:
                self.front_detect = True  # Sensor is off the screen.
                return i
            else:  # if we are not offscrean.
                #TODO remove dependency to main, drone must be surface too
                obs = self.drone.main.main_s.get_at(rotated_p)
                if obs == D_BLACK and self.drone.show_sensors:
                    self.front_detect = True

        return i  # Return the distance for the arm.


    def get_rotated_point(self,x_1, y_1, x_2, y_2, angle):
        radians = deg_to_rad(angle)
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.sin(radians) + (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - (x_1 - x_2) * math.cos(radians)
        new_x = x_change + x_1
        new_y = y_change + y_1

        return int(new_x), int(new_y)
