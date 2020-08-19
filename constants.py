import pygame
import enum 

# Original image
MAP_IMAGE_PATH:str = "/home/ron/Desktop/ROBOTICA_SOP/DroneSim/.maps/p15.png"
# Image after we remove all execpt BLACK and WHITE pixels
TMP_MAP_PATH:str  = ".maps/mew_map.png"

#window
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 719
#global
WHITE:tuple = (255, 255, 255)
BLACK:tuple = (0, 0, 0)
YELLOW:tuple = (255, 255, 0)

def FONT_SIZE_BIG():
    return  pygame.font.Font(None, 30)

def FONT_SIZE_NORMAL():
    return  pygame.font.Font(None, 20)

# Main
FPS = 80

# enums 
class MouseButton(enum.Enum): 
    left = 1
    middle = 2
    right = 3


# enums 
class Fonts(): 
    def __init__(self):
        self.font_size_big = pygame.font.Font(None, 30)
        self.font_size_normal = pygame.font.Font(None, 20)