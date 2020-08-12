import easygui as eg  # https://github.com/robertlugg/easygui   - easy way to open file dialog and other gui things.
from PIL import Image

from Drone import *


# Main class for dealing with out map.
class Map:
    def __init__(self):
        self.map_width = 0
        self.map_height = 0
        self.collide_list = []  # a list full of all the 'black spots'/walls
        self.count_white_b = 0  # for counting amount of blocks
        self.count_black_b = 0
        self.map_path = eg.fileopenbox()  # opens a file choosing dialog.
        self.map_array = []

    def create_map_from_img(self):
        with Image.open(self.map_path) as img:  # open the chosen map file as image.
            self.map_width, self.map_height = img.size  # size of map.
            rgb_image = img.convert("RGB")

            for i in range(self.map_width):
                self.map_array.append([])
                for j in range(self.map_height):
                    self.map_array[i].append(0)
            for x in range(self.map_width):
                for y in range(self.map_height):
                    rgb_pixel_value = rgb_image.getpixel((x, y))
                    if rgb_pixel_value != WHITE:  # if not completly white
                        img.putpixel((x, y), BLACK)  # turn black (colored - walls, white - path)
                        self.map_array[x][y] = BLACK  # add black block to map array
                        self.count_black_b += 1
                    else:
                        img.putpixel((x, y), WHITE)
                        self.map_array[x][y] = WHITE
                        self.count_white_b += 1
            print('Wall (black) blocks: ' + str(self.count_black_b),
                  'Path (white) blocks: ' + str(self.count_white_b))
            for x in range(self.map_width - 1):
                for y in range(
                        self.map_height - 1):  # for every black pixel, if there is a white pixel in his near
                    # environment, add to collide_list. if not, pass.
                    if ((self.map_array[x - 1][y - 1] == WHITE or self.map_array[x][y - 1] == WHITE or
                         self.map_array[x + 1][y - 1] == WHITE or
                         self.map_array[x - 1][y] == WHITE or self.map_array[x + 1][y + 1] == WHITE or
                         self.map_array[x + 1][y] == WHITE or self.map_array[x - 1][y + 1] == WHITE or
                         self.map_array[x][y + 1] == WHITE) and self.map_array[x][y] == BLACK):
                        block = pygame.Rect(x, y, 1, 1)
                        self.collide_list.append(block)  # add black block to our collide list
                    else:
                        continue
                        
            print('Wall (black) blocks added to collision list: ' + str(len(self.collide_list)))
            img.save(".img/new_map.png")
