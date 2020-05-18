import tkinter as tk
import pygame
import Drone
import os
from math import copysign

FILE_PATH = './.simu'


class SimulationWindow:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Drone Simulation")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(curr_dir, "drone.png")
        drone_img = pygame.image.load(img_path)
        drone = Drone.Model(0, 0)
        ppu = 32
        while not self.exit:
            dt = self.clock.get_time() / 1000

            for event in pygame.event.get():  # our event que.

                if event.type == pygame.QUIT:
                    self.exit = True

                # getting user input
                key_stroke = pygame.key.get_pressed()

                if key_stroke[pygame.K_UP]:  # the up key
                    if drone.velocity.x < 0:
                        drone.acceleration = Drone.BRAKE_DEACCELERATION
                    drone.acceleration += 1 * dt
                elif key_stroke[pygame.K_DOWN]:
                    if drone.velocity.x > 0:
                        drone.acceleration = -Drone.BRAKE_DEACCELERATION
                elif key_stroke[pygame.K_SPACE]:
                    if abs(drone.velocity.x) > dt * Drone.BRAKE_DEACCELERATION:
                        drone.acceleration = -copysign(Drone.BRAKE_DEACCELERATION, drone.velocity.x)
                    else:
                        drone.acceleration = -drone.velocity.x / dt
                else:
                    if abs(drone.velocity.x) > dt * Drone.FREE_DEACCELERATION:
                        drone.acceleration = -copysign(Drone.FREE_DEACCELERATION, drone.velocity.x)
                    else:
                        if dt != 0:
                            drone.acceleration = -drone.velocity.x / dt
                drone.acceleration = max(-Drone.MAX_VELOCITY, min(drone.acceleration, Drone.MAX_VELOCITY))

                if key_stroke[pygame.K_RIGHT]:
                    drone.steering -= 30 * dt
                elif key_stroke[pygame.K_LEFT]:
                    drone.steering += 30 * dt
                else:
                    drone.steering = 0
                drone.steering = max(-Drone.MAX_STEERING_ANGLE, min(drone.steering, Drone.MAX_STEERING_ANGLE))

                drone.update(dt)
                # Drawing
                self.screen.fill((0, 0, 0))
                map_img = pygame.image.load(r'C:\Users\97254\PyCharmProjects\DroneSim\.maps\sim_20.png') # map location
                self.screen.blit(map_img, (0, 0))
                rotated = pygame.transform.rotate(drone_img, drone.angle)
                rect = rotated.get_rect()
                self.screen.blit(rotated, drone.position * ppu - (rect.width / 2, rect.height / 2))
                pygame.display.flip()

                self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = SimulationWindow()
    game.run()
