import datetime
import pygame
import easygui as eg  # https://github.com/robertlugg/easygui   - easy way to open file dialog and other gui things.
import constants
from drone import Drone
from map import Map
from ui_controls import UiControls
from ui_metrics import UiMetrics
from logger import Logger

magenta = (255, 0, 255)
cyan = (0, 255, 255)

clock = pygame.time.Clock()
pygame.init()  # initialize pygame window
pygame.font.init()

class MainRun:
    def __init__(self):
        print("###########~~INIT SIMULATOR WINDOW~~###########")
        self.time = datetime.datetime.min
        self.clock = clock
        self.stopped = False
        self.log_data = False
        self.main_s = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))  # our main display
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

        # Creating game objects
        drone = Drone(100, 300, self.main_s, game_map)  # drone object, starting from coordinates 100,300
        ui_controls = UiControls(self.main_s,drone,self)
        ui_metrics= UiMetrics(self.main_s,drone,clock,self)
        logger = Logger(self,log_file="log.log")


        while self.stopped == False:
            #   # gets a single event from the event queue
            # event = pygame.event.wait()
            #       # if the 'close' button of the window is pressed
            # if event.type == pygame.QUIT:
            #     # stops the application
            #     break
            clock.tick(constants.FPS)
            clock.tick()

            self.time = pygame.time.get_ticks()/1000

            #TODO: we should not fill and blit every loop, we need to create main_s with map once, and blit only changes of
            # the dron.
            self.main_s.fill(constants.YELLOW)  # resets the map every loop.
            self.main_s.blit(game_map.surface, (200,0))  # filling screen with map
            # TODO: a method for logging key pressings.
            # TODO: implement autostate
            # need to implement auto state

            self.update_all([drone,ui_metrics,ui_controls])
            self.display_all([drone,ui_metrics,ui_controls])
            
            if self.log_data:
                logger.log(drone=drone)
                 
            pygame.display.flip()  # show the surface we created on the actual screen.

MainRun()