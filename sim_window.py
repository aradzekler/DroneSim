
import datetime

import pygame
import easygui as eg  # https://github.com/robertlugg/easygui   - easy way to open file dialog and other gui things.

import constants
from Drone import Drone
from Map import Map
from UI_controls import UI_Controls
from Logger import Logger


# TODO: limit movement (drone get stuck in walls)
# displaying the screen.
def display_all(main_surface, display_list, scene_metrics,ui_control):
    for element in display_list:
        element.display(main_surface)

    ui_control.display_all(scene_metrics)


# creating a simple button in pygame
clock = pygame.time.Clock()

pygame.init()  # initialize pygame window
print("###########~~INIT SIMULATOR WINDOW~~###########")


# TODO: Enable for map selection dialog and remove constant 
# map_image_path = eg.fileopenbox()  # opens a file choosing dialog.
map_image_path = constants.MAP_IMAGE_PATH

game_map = Map(map_image_path)  # setting map object, map choosing is inside the object.

game_map.create_map_from_img()
main_s = pygame.display.set_mode((game_map.map_width, game_map.map_height))  # our main display
drone = Drone(100, 300, main_s, game_map)  # drone object, starting from coordinates 100,300
sim_map = pygame.image.load(constants.TMP_MAP_PATH).convert()  # loading the map with the temp name given.


pygame.time.set_timer(pygame.USEREVENT, 1000)
time = datetime.datetime.min
running = True  # simulation is running

ui_controls = UI_Controls(game_map,main_s,drone)
logger = Logger()

while running:
    clock.tick(constants.FPS)
    time += datetime.timedelta(0, (constants.FPS / 10))

    main_s.fill(constants.BLACK)  # resets the map every loop.
    main_s.blit(sim_map, (0, 0))  # filling screen with map

    ui_controls.set_event_listeners(drone)
    
    # TODO: a method for logging key pressings.
    # TODO: implement autostate
    # need to implement auto state

    to_update = [drone]  # update drone variables
    to_display = [drone]  # update drone displaying on map.

    scene_metrics = ui_controls.set_metrics(drone,clock,time)
    log_line = logger.log(drone,clock,time)
    ui_controls.update_all(to_update)

    display_all(main_s, to_display, scene_metrics,ui_controls)
    pygame.display.flip()  # show the surface we created on the actual screen.



