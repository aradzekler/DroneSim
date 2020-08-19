import datetime
import pygame
import easygui as eg  # https://github.com/robertlugg/easygui   - easy way to open file dialog and other gui things.
import constants
from map import Map
from ui_controls import UiControls
from ui_metrics import UiMetrics
from logger import Logger
from interfaces.pygame_object_interface import PyGameObjectInterface

magenta = (255, 0, 255)
cyan = (0, 255, 255)

clock = pygame.time.Clock()
pygame.init()  # initialize pygame window
pygame.font.init()

class MainRun(PyGameObjectInterface):
    def __init__(self):
        print("###########~~INIT SIMULATOR WINDOW~~###########")
        self.time = datetime.datetime.min
        self.clock = clock
        self.stopped = False
        self.log_data = False
        self.surface = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))  # our main display
        # TODO: Enable for map selection dialog and remove constant 
        # map_image_path = eg.fileopenbox()  # opens a file choosing dialog.
        self.map = Map(self,constants.MAP_IMAGE_PATH)  # setting map object, map choosing is inside the object.
        
        self.Main()


    def Main(self):

   
        self.map.create_map_from_img()

        # Creating game objects
        ui_controls = UiControls(self)
        ui_metrics= UiMetrics(self)
        logger = Logger(self,log_file="log.log")


        while self.stopped == False:
            # clock.tick(constants.FPS)
            clock.tick()

            self.time = pygame.time.get_ticks()/1000

            #TODO: we should not fill and blit every loop, we need to create main_s with map once, and blit only changes of
            # the dron.
            self.surface.fill(constants.YELLOW)  # resets the map every loop.
            # TODO: a method for logging key pressings.
            # TODO: implement autostate

            # THE ORDER IN THIS ARRAY IS IMPORTANT
            self.update_all([self.map,ui_metrics,ui_controls])
            self.display_all([self.map,ui_metrics,ui_controls])
            
            if self.log_data:
                logger.log()
                 
            pygame.display.flip()  # show the surface we created on the actual screen.

MainRun()