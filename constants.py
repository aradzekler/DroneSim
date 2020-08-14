import pygame
import enum 

# Original image
MAP_IMAGE_PATH:str = r"E:/Repos/DroneSim/.maps/p15.png"
# Image after we create only constants.BLACK and constants.WHITE pixels
TMP_MAP_PATH:str  = r".maps/mew_map.png"

#window
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 719
#global
WHITE:tuple = (255, 255, 255)
BLACK:tuple = (0, 0, 0)
YELLOW:tuple = (255, 255, 0)

# Main loop
FPS = 30

def FONT_SIZE_BIG():
    return  pygame.font.Font(None, 30)

def FONT_SIZE_NORMAL():
    return  pygame.font.Font(None, 20)


# creating enumerations using class 
class MouseButton(enum.Enum): 
    left = 1
    middle = 2
    right = 3