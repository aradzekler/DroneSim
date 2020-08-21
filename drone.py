import pygame
import math as math
from model_states import ManualState,AutoState
from interfaces.pygame_object_interface import PyGameObjectInterface
from boards.tof_sensor import TofSensor
from helpers import deg_to_rad

# TODO: ADD LIDARS, ADD AI, GENERICS

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



# https://www.pygame.org/project-Rect+Collision+Response-1061-.html



class Drone(PyGameObjectInterface):
    def __init__(self,map, x, y):
        self.map = map
        self.body = pygame.image.load("Images//Body//Grey.png").convert()  # images for the model itself.
        self.rotors = pygame.image.load("Images//Wheels//Black.png").convert()
        self.rect = self.body.get_rect()  # get rectangle the size of the body. our hitbox
        self.rect.x = self.body.get_rect().width / 2 + x  # x location
        self.rect.y = self.body.get_rect().height / 2 + y
        manual_state = ManualState()
        auto_state = AutoState()
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


        #create tof sensor visuals
        self.tof_sensors = []
        sensorLeft = TofSensor(self,45); 
        sensorMiddle = TofSensor(self,0); 
        sensorRight= TofSensor(self,-45); 

        self.tof_sensors.extend((sensorLeft, sensorMiddle, sensorRight))


    # updating function for movement
    def update(self):
        self.move_x = 0  # no momentum
        self.move_y = 0
        for block in self.map.collide_list:  # check for collisions
            if self.rect.colliderect(block):
                self.is_colliding = True

        if self.tracking and self.is_colliding:  # if tracking in on
            self.drone_track.add((self.rect.x + int(self.sensor_x_relative), self.rect.y + int(self.sensor_y_relative),
                                  RED))  # if collided add red track
        elif self.tracking:
            self.drone_track.add(
                (self.rect.x + int(self.sensor_x_relative), self.rect.y + int(self.sensor_y_relative),
                 BLUE))  # if not, add blue
       
        
        self.rotate()
        self.move()
        self.reset_data()


    # display the drone on the map.
    def display(self):

        # self.blitRotate(main_surface,self.body,(self.rect.x, self.rect.y),(self.rect.x, self.rect.y),self.angle)
        for coordinate in self.drone_track:  # painting our tracking
            pygame.draw.circle(self.map.surface, coordinate[2], (coordinate[0], coordinate[1]), 1)  # draw the circle in
            # the coordinates with the coordinates color
            
        # loc = self.body.get_rect().center  #rot_image is not defined 
        # rot_sprite = pygame.transform.rotate(self.body, self.angle)
        # rot_sprite.get_rect().center = loc
        # main_surface.blit(rot_sprite, (self.rect.x, self.rect.y))

        # rotor_image = pygame.transform.rotate(self.rotors, self.angle)
        # main_surface.blit(rotor_image, (self.rect.x, self.rect.y))
        
        # self.rect.x, self.rect.y = self.rect.center
        # self.rect.center = (self.rect.x, self.rect.y)
        
        self.update_all(self.tof_sensors)
        self.display_all(self.tof_sensors)  

        body_image = pygame.transform.rotate(self.body, self.angle)
        self.map.surface.blit(body_image, (self.rect.x, self.rect.y))
     

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


    # our main drone class for now., getting a starting x and y coordinations, screen - pygame.display (our game
    # 'canvas'), gamemap - our Map object
