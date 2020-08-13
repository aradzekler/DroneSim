
import pygame
import constants

ACTIVE_BUTTON_COLOR = pygame.Color('dodgerblue1')
INACTIVE_BUTTON_COLOR = pygame.Color('dodgerblue4')

class UiMetrics:
    def __init__(self,main_s,drone,clock,main):
        self.main_s = main_s
        self.drone = drone
        self.clock = clock
        self.main = main
        self.scene_metrics = []
       
        pygame.font.init()
        self.font = pygame.font.SysFont("", 20)
        self.FONT = pygame.font.Font(None, 30)
  

    def update(self):
        self.scene_metrics = ["FPS: " + str("%.0f" % self.clock.get_fps()),  # our telemetry window.
                    "Drone angle: " + str("%.2f" % self.drone.angle),
                    "Current speed: " + str("%.2f" % self.drone.current_speed),
                    "X Axis Movement: " + str("%.2f" % self.drone.move_x),
                    "Y Axis movement: " + str("%.2f" % self.drone.move_y),
                    "F key" + str(self.drone.forward),
                    "L key" + str(self.drone.left),
                    "R key" + str(self.drone.right),
                    "B key" + str(self.drone.backward),
                    "Collided: " + str(self.drone.is_colliding),
                    "Collision Detected: " + str(self.drone.front_detect),
                    "Time: " + str(self.main.time)]


    def display(self):
        for element_val in range(0, len(self.scene_metrics)):  # adding text in the side of the screen
            self.main_s.blit(self.font.render(str(self.scene_metrics[element_val]), True, (0, 255, 0)), (10, 10 + (20 * element_val)))

