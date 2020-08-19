
import pygame
import constants
from interfaces.pygame_object_interface import PyGameObjectInterface

ACTIVE_BUTTON_COLOR = pygame.Color('dodgerblue1')
INACTIVE_BUTTON_COLOR = pygame.Color('dodgerblue4')

class UiMetrics(PyGameObjectInterface):
    def __init__(self,main):
        self.main = main
        self.scene_metrics = []
        self.fonts = constants.Fonts()

    def update(self):
        self.scene_metrics = ["FPS: " + str("%.0f" % self.main.clock.get_fps()),  # our telemetry window.
                    "Drone angle: " + str("%.2f" % self.main.map.drone.angle),
                    "Current speed: " + str("%.2f" % self.main.map.drone.current_speed),
                    "X Axis Movement: " + str("%.2f" % self.main.map.drone.move_x),
                    "Y Axis movement: " + str("%.2f" % self.main.map.drone.move_y),
                    "F key" + str(self.main.map.drone.forward),
                    "L key" + str(self.main.map.drone.left),
                    "R key" + str(self.main.map.drone.right),
                    "B key" + str(self.main.map.drone.backward),
                    "Collided: " + str(self.main.map.drone.is_colliding),
                    "Collision Detected: " + str(self.main.map.drone.front_detect),
                    "Time: " + str(self.main.time)]


    def display(self):
        for element_val in range(0, len(self.scene_metrics)):  # adding text in the side of the screen
            self.main.surface.blit(self.fonts.font_size_normal.render(str(self.scene_metrics[element_val]),True,constants.BLACK), (10, 10 + (20 * element_val)))

