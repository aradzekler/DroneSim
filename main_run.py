import datetime
import pygame
import easygui as eg  # https://github.com/robertlugg/easygui   - easy way to open file dialog and other gui things.
import constants
from drone import Drone
from map import Map
from ui_controls import UiControls
from ui_metrics import UiMetrics
from logger import Logger


clock = pygame.time.Clock()
pygame.init()  # initialize pygame window
pygame.font.init()

class MainRun:
    def __init__(self):
        print("###########~~INIT SIMULATOR WINDOW~~###########")
        self.time = datetime.datetime.min
        self.clock = clock
        self.stopped = False
        self.Main()

    def update_all(self,elements):
        for element in elements:
            element.update()
        
    # TODO: limit movement (drone get stuck in walls)
    # displaying the screen.
    def display_all(self,elements):
        for element in elements:
            element.display()


    def Main(self):
        # TODO: Enable for map selection dialog and remove constant 
        # map_image_path = eg.fileopenbox()  # opens a file choosing dialog.
        game_map = Map(constants.MAP_IMAGE_PATH)  # setting map object, map choosing is inside the object.
        game_map.create_map_from_img()
        main_s = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))  # our main display
        sim_map = pygame.image.load(constants.TMP_MAP_PATH).convert()  # loading the map with the temp name given.

        drone = Drone(100, 300, main_s, game_map)  # drone object, starting from coordinates 100,300
        ui_controls = UiControls(game_map,main_s,drone,self)
        ui_metrics= UiMetrics(main_s,drone,clock,self)
        logger = Logger(self,log_file="log.log")

        while self.stopped == False:
            clock.tick(constants.FPS)
            # Something wrong with time format, see logs
            self.time = pygame.time.get_ticks()/1000

            main_s.fill(constants.YELLOW)  # resets the map every loop.
            main_s.blit(sim_map, (200,0))  # filling screen with map
            # TODO: a method for logging key pressings.
            # TODO: implement autostate
            # need to implement auto state

            self.update_all([drone,ui_metrics,ui_controls])
            self.display_all([drone,ui_metrics,ui_controls])

            # logger.log(drone,clock,time)
            
            logger.log(drone=drone)
            pygame.display.flip()  # show the surface we created on the actual screen.

MainRun()




# running = True  # simulation is running

# TODO: Need to fix quit functionality!!!!!!!!!!!!!!
# def play_game(play):
#     return play



