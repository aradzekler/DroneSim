
import pygame
import constants

ACTIVE_BUTTON_COLOR = pygame.Color('dodgerblue1')
INACTIVE_BUTTON_COLOR = pygame.Color('dodgerblue4')

class UiMetrics:
    def __init__(self,main,drone,clock):
        self.drone = drone
        self.clock = clock
        self.main = main
        self.scene_metrics = []
        self.fonts = constants.Fonts()

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
            self.main.main_s.blit(self.fonts.font_size_normal.render(str(self.scene_metrics[element_val]),True,constants.BLACK), (10, 10 + (20 * element_val)))

