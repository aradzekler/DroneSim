import pygame
import Model_States
import math as math

RED = (255, 0, 0)

class Sensor(object):
    
    def __init__(self, surface, wire_pos_start, wire_width,angle):
        self.wire_pos_start = wire_pos_start
        self.wire_width = wire_width
        self.surface = surface
        self.angle = angle
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        manual_state = Model_States.ManualState()
        self.state = manual_state  # the drone state
        self.event = 'manual_control'

    def draw(self):
        self.rotate()
        radians = math.radians(self.angle)
        # Rotate x_2, y_2 around x_1, y_1 by angle.
  
        # radar = (100,100)
        radar_len = 100
        x = self.wire_pos_start[0] + math.sin(math.radians(self.angle)) * radar_len
        y = self.wire_pos_start[1] + math.cos(math.radians(self.angle)) * radar_len

        x1 = self.wire_pos_start[0] + math.sin(math.radians(self.angle+45)) * radar_len
        y1 = self.wire_pos_start[1] + math.cos(math.radians(self.angle+45)) * radar_len

        x2 = self.wire_pos_start[0] + math.sin(math.radians(self.angle -45)) * radar_len
        y2 = self.wire_pos_start[1] + math.cos(math.radians(self.angle -45)) * radar_len
        print(f'orx:{self.wire_pos_start[0]}, ory:{self.wire_pos_start[1]}, x:{x}, y:{y}, angle:{self.angle}')
        pygame.draw.line(self.surface, RED, self.wire_pos_start, (x,y))
        pygame.draw.line(self.surface, RED, self.wire_pos_start, (x1,y1))
        pygame.draw.line(self.surface, RED, self.wire_pos_start, (x2,y2))

    def reset_data(self):
        self.left = False
        self.right = False
        self.forward = False
        self.backward = False
        self.front_detection_lidar = False

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

    def on_event(self, event):
        """
        This is the bread and butter of the state machine. Incoming events are
        delegated to the given states which then handle the event. The result is
        then assigned as the new state (inteface in Model_States.py.)
        """
        # The next state will be the result of the on_event function.

        if event == 'manual_control':  # if we are in manual
            key = pygame.key.get_pressed()
            self.manual_press(key)
        elif event == 'auto_control':  # if we are in auto state
            print("")

        self.state = self.state.on_event(event)

    def rotate(self):
        if self.angle > 360:
            self.angle = 0
        else:
            if self.angle < 0:
                self.angle = 360
        if self.left:
            self.angle += 5
        if self.right:
            self.angle -= 5
           

    def update(self):
        # self.move_x = 0  # no momentum
        # self.move_y = 0
        self.rotate()
        self.draw()
        self.reset_data()