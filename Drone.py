import math as math

import pygame

import Model_States

# TODO: ADD LIDARS, ADD AI, GENERICS
# TODO: SET UP GUI BUTTONS.

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
D_BLACK = (0, 0, 0, 255)
SENSOR_RANGE = 10


# https://www.pygame.org/project-Rect+Collision+Response-1061-.html


# function for converting degrees to radians.
def deg_to_rad(deg):
    return deg / 180.0 * math.pi


def get_rotated_point(x_1, y_1, x_2, y_2, angle):
    radians = deg_to_rad(angle)
    # Rotate x_2, y_2 around x_1, y_1 by angle.
    x_change = (x_2 - x_1) * math.sin(radians) + (y_2 - y_1) * math.sin(radians)
    y_change = (y_1 - y_2) * math.cos(radians) - (x_1 - x_2) * math.cos(radians)
    new_x = x_change + x_1
    new_y = y_change + y_1

    return int(new_x), int(new_y)


class SimpleDrone:
    def __init__(self, x, y, screen, game_map):
        self.body = pygame.image.load("Images//Body//Grey.png").convert()  # images for the model itself.
        self.rotors = pygame.image.load("Images//Wheels//Black.png").convert()
        self.rect = self.body.get_rect()  # get rectangle the size of the body. our hitbox
        self.rect.x = self.body.get_rect().width / 2 + x  # x location
        self.rect.y = self.body.get_rect().height / 2 + y
        self.game_map = game_map
        self.screen = screen
        manual_state = Model_States.ManualState()
        auto_state = Model_States.AutoState()
        self.state = manual_state  # the drone state
        self.event = 'manual_control'

        # sensors
        self.show_sensors = True
        self.front_detect = False  # drone front.
        self.tracking = True
        self.sensor_x_relative = self.body.get_rect().width / 2  # the relative location of the sensor.
        self.sensor_y_relative = self.body.get_rect().height / 2
        self.drone_track = {(self.rect.x + int(self.sensor_x_relative), self.rect.y + int(self.sensor_y_relative),
                             BLUE)}  # a set for tracking our drones coordinates around the map.

        # movement states for easy movement capturing.
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
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
        self.angle = 0

    def on_event(self, event):
        """
        This is the bread and butter of the state machine. Incoming events are
        delegated to the given states which then handle the event. The result is
        then assigned as the new state (interface in Model_States.py.)
        """

        # The next state will be the result of the on_event function.

        if event == 'manual_control':  # if we are in manual
            key = pygame.key.get_pressed()
            self.manual_press(key)
        elif event == 'auto_control':  # if we are in auto state
            print("")

        self.state = self.state.on_event(event)

    # setter methods for rectx and recty
    def set_rect_x(self, x):
        self.rect.x = x

    def set_rect_y(self, y):
        self.rect.y = y

    # function for moving around with mouse clicks.
    def manual_press(self, key):
        if key[pygame.K_LEFT]:
            self.left = True
        if key[pygame.K_RIGHT]:
            self.right = True
        if key[pygame.K_UP]:
            self.forward = True
        if key[pygame.K_DOWN]:
            self.backward = True
        if key[pygame.K_r]:
            self.angle = 0

    # resetting variables.
    def reset_data(self):
        self.left = False
        self.right = False
        self.forward = False
        self.backward = False
        self.front_detect = False

    # Rotation movement angle.
    def rotate(self):
        if self.angle > 360:
            self.angle = 0
        else:
            if self.angle <= 0:
                self.angle = 360
        if self.current_speed == 0:  # rotate in spot.
            if self.left:
                self.angle += self.turn_speed
            if self.right:
                self.angle -= self.turn_speed
        else:
            if self.left:
                self.angle += self.turn_speed * self.current_speed
            if self.right:
                self.angle -= self.turn_speed * self.current_speed

    # actual movement
    def move(self):
        if self.forward:
            if self.current_speed < self.top_speed:
                self.current_speed += self.acceleration
        elif self.backward:
            if self.top_speed > self.current_speed > 0:
                self.current_speed -= self.deceleration
            elif -self.top_speed < self.current_speed < 0:
                self.current_speed -= self.acceleration
            elif self.current_speed == 0:
                self.current_speed -= self.acceleration
        else:
            if self.current_speed > 0:
                if self.current_speed < 0.5:
                    self.current_speed = 0
                self.current_speed -= self.deceleration
            elif self.current_speed < 0:
                self.current_speed += self.deceleration

        angle_rad = deg_to_rad(self.angle)
        self.move_x = (float(self.current_speed * math.sin(angle_rad)))  # actual movement
        self.move_y = (float(self.current_speed * math.cos(angle_rad)))
        self.rect.x += self.move_x
        self.rect.y += self.move_y

        # self.get_sonar_readings(self.screen)

    # display the drone on the map.
    def display(self, main_surface):
        body_image = pygame.transform.rotate(self.body, self.angle)
        main_surface.blit(body_image, (self.rect.x, self.rect.y))

        rotor_image = pygame.transform.rotate(self.rotors, self.angle)
        main_surface.blit(rotor_image, (self.rect.x, self.rect.y))

        self.get_sonar_readings(main_surface)
        self.rect.x, self.rect.y = self.rect.center
        self.rect.center = (self.rect.x, self.rect.y)

    # updating function for movement
    def update(self):
        self.move_x = 0  # no momentum
        self.move_y = 0
        for block in self.game_map.collide_list:  # check for collisions
            if self.rect.colliderect(block):
                self.is_colliding = True

        if self.tracking and self.is_colliding:  # if tracking in on
            self.drone_track.add((self.rect.x + int(self.sensor_x_relative), self.rect.y + int(self.sensor_y_relative),
                                  RED))  # if collided add red track
        elif self.tracking:
            self.drone_track.add(
                (self.rect.x + int(self.sensor_x_relative), self.rect.y + int(self.sensor_y_relative),
                 BLUE))  # if not, add blue
        for coordinate in self.drone_track:  # painting our tracking
            pygame.draw.circle(self.screen, coordinate[2], (coordinate[0], coordinate[1]), 1)  # draw the circle in
            # the coordinates with the coordinates color
        self.rotate()
        self.move()
        self.reset_data()

    # sonar detection function
    def get_arm_distance(self, arm, offset, screen):
        i = 0  # Used to count the distance.
        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1
            # Move the point to the right spot.
            rotated_p = get_rotated_point(
                self.rect.x + self.sensor_x_relative, self.rect.y + self.sensor_y_relative, point[0], point[1],
                self.angle + offset)
            pygame.draw.circle(screen, (255, 0, 255), rotated_p, 1)  # drawing sonar arms.
            rotated_list_p = list(rotated_p)
            rotated_list_p[0] += 1  # nasty workaround to change the tuple rotated_p value in order to 'see' the white
            # and not purple.
            rotated_p = tuple(rotated_list_p)
            # Check if we've hit something.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= self.game_map.map_width or rotated_p[1] >= self.game_map.map_height:
                self.front_detect = True  # Sensor is off the screen.
                return i
            else:  # if we are not offscrean.
                obs = screen.get_at(rotated_p)
                if obs == D_BLACK and self.show_sensors:
                    self.front_detect = True

        return i  # Return the distance for the arm.

    # display arms on map
    def get_sonar_readings(self, screen):
        readings = []

        # Make our sensor 'arms;'.
        arm_left = self.make_sonar_arm()
        arm_middle = self.make_sonar_arm()
        arm_right = self.make_sonar_arm()

        # Rotate them and get readings. (3 different sonar arms.)
        readings.append(self.get_arm_distance(arm_left, 10.75, screen))
        readings.append(self.get_arm_distance(arm_middle, 0, screen))
        readings.append(self.get_arm_distance(arm_right, -10.75, screen))

        return readings

    # adding a "sonar arm", which will detect movement in a straight line from origin
    def make_sonar_arm(self):
        spread = 10  # Default spread (distance between every sonar arm)
        arm_points = []
        for i in range(0, SENSOR_RANGE):
            arm_points.append(  # painting the 'dots' of the arm relative to our drone location
                (self.rect.x + self.sensor_x_relative + (spread * i), self.rect.y + self.sensor_y_relative))

        return arm_points

    # our main drone class for now., getting a starting x and y coordinations, screen - pygame.display (our game
    # 'canvas'), gamemap - our Map object
