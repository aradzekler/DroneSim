import pygame
import constants
from PIL import Image

# Main class for dealing with out map.
class Map:
    def __init__(self,map_image_path:str):
        self.map_image_path = map_image_path
        self.map_width = 0
        self.map_height = 0
        self.collide_list = []  # a list full of all the 'black spots'/walls
        self.surface = []  # a list full of all the 'black spots'/walls



    def create_map_from_img(self):
        """
        Take png image and create proper black and white image
        Also generate collision list
        The collision list is used for proper wall detection
        """
        
        map_array = []
        count_white_b = 0  # for counting amount of blocks
        count_black_b = 0
        with Image.open(self.map_image_path) as img:  # open the chosen map file as image.
            self.map_width, self.map_height = img.size  # size of map.
            rgb_image = img.convert("RGB")

            # map_array = (self.map_height,self.map_width)
            # np.zeros(map_array)
            # TODO convert to numpy if possible
            for i in range(self.map_width):
                map_array.append([])
                for j in range(self.map_height):
                    map_array[i].append(0)
            
            for x in range(self.map_width):
                for y in range(self.map_height):
                    rgb_pixel_value = rgb_image.getpixel((x, y))
                    if rgb_pixel_value != constants.WHITE:  # if not completly white
                        img.putpixel((x, y), constants.BLACK)  # turn black (colored - walls, white - path)
                        map_array[x][y] = constants.BLACK  # add black block to map array
                        count_black_b += 1
                    else:
                        img.putpixel((x, y), constants.WHITE)
                        map_array[x][y] = constants.WHITE
                        count_white_b += 1
            print('Wall (black) blocks: ' + str(count_black_b),
                  'Path (white) blocks: ' + str(count_white_b))
            for x in range(self.map_width - 1):
                for y in range(
                        self.map_height - 1):  # for every black pixel, if there is a white pixel in his near
                    # environment, add to collide_list. if not, pass.
                    if ((map_array[x - 1][y - 1] == constants.WHITE or map_array[x][y - 1] == constants.WHITE or
                         map_array[x + 1][y - 1] == constants.WHITE or
                         map_array[x - 1][y] == constants.WHITE or map_array[x + 1][y + 1] == constants.WHITE or
                         map_array[x + 1][y] == constants.WHITE or map_array[x - 1][y + 1] == constants.WHITE or
                         map_array[x][y + 1] == constants.WHITE) and map_array[x][y] == constants.BLACK):
                        block = pygame.Rect(x, y, 1, 1)
                        self.collide_list.append(block)  # add black block to our collide list
                    else:
                        continue
                        
            print('Wall (black) blocks added to collision list: ' + str(len(self.collide_list)))
            img.save(constants.TMP_MAP_PATH)
            #TODO need to dinf a way to create surface form img and not loading it again
            self.surface = pygame.image.load(constants.TMP_MAP_PATH).convert()
