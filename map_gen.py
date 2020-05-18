import os
from PIL import Image
from random import randint


class SplitRectangleError(Exception):
    pass


class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    @property
    def is_leaf(self):
        return self.left is None and self.right is None


class Rect:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self._area = None
        self._room = None

    @property
    def area(self):
        if self._area is None:
            self._area = self.width * self.height
        return self._area

    @property
    def room(self):
        if self._room is None:
            self._room = self.create_room()
        return self._room

    def create_room(self):
        # Room options.
        padding = self.options['padding']
        min_wall_size = self.options['min_wall_size']
        min_walls_ratio = self.options['min_walls_ratio']
        min_area_percent = self.options['min_area_percent']

        x = randint(self.x + padding, self.x + int(self.width / 2))
        y = randint(self.y + padding, self.y + int(self.height / 2))

        width = randint(min_wall_size, self.x + self.width - x) - padding
        height = randint(min_wall_size, self.y + self.height - y) - padding

        if (height / width < min_walls_ratio or width / height < min_walls_ratio or
                width * height < min_area_percent * self.area):
            return self.create_room()

        return Rect(x, y, width, height, self.options)

# map colors.
def rgb(tile_sign):
    if tile_sign == '0':
        return (118, 165, 204)
    if tile_sign == '1':
        return (74, 103, 127)
    if tile_sign == '2':
        return (224, 231, 255)
    return (0, 0, 0)


def create_preview(mappath, width, height, zoom=1):
    im = None
    img_data = []
    im = Image.new('RGB', (width, height))

    with open(mappath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = list(line.strip('\n'))
            img_data = img_data + list(map(rgb, line))

    im.putdata(img_data)
    im = im.resize((int(width * zoom), int(height * zoom)), Image.ANTIALIAS)

    head, ext = os.path.splitext(mappath)
    new_img_path = '{}{}'.format(head, '.png')
    im.save(new_img_path)


def split_rect(rect, options):
    padding = options['padding']
    min_wall_size = options['min_wall_size']
    min_walls_ratio = options['min_walls_ratio']

    min_split_size = 2 * padding + min_wall_size

    # we don't want to split too small reactangle
    if rect.width < 2 * min_split_size or rect.height < 2 * min_split_size:
        raise SplitRectangleError()

    if randint(0, 1) == 0:  # split vertical
        r1 = Rect(
            rect.x, rect.y,
            randint(min_split_size, rect.width), rect.height,
            options
        )
        r2 = Rect(
            rect.x + r1.width, rect.y,
            rect.width - r1.width, rect.height,
            options
        )

        # retry if ratio is too small
        if r1.width / r1.height < min_walls_ratio or r2.width / r2.height < min_walls_ratio:
            return split_rect(rect, options)
    else:  # split horizontal
        r1 = Rect(
            rect.x, rect.y,
            rect.width, randint(min_split_size, rect.height),
            options
        )
        r2 = Rect(
            rect.x, rect.y + r1.height,
            rect.width, rect.height - r1.height,
            options
        )

        # retry if ratio is too small
        if r1.height / r1.width < min_walls_ratio or r2.height / r2.width < min_walls_ratio:
            return split_rect(rect, options)
    return r1, r2


def split_tree_of_rectangles(rect, step, options):
    tree = Node(rect)
    if step != 0:
        split = split_rect(rect, options)
        if split:
            tree.left = split_tree_of_rectangles(split[0], step - 1, options)
            tree.right = split_tree_of_rectangles(split[1], step - 1, options)
    return tree


# Our configuration options
DEFAULT_OPTIONS = {
    'padding': 1,
    'min_wall_size': 2,
    'min_walls_ratio': 0.4,
    'min_area_percent': 0.6
}

MAP_WIDTH = 1000
MAP_HEIGHT = 1000

SPLITS = 5

MAPS_PATH = './.maps'
MAP_FORMAT = 'sim_{}.map'

wrap_rect = Rect(0, 0, MAP_WIDTH, MAP_HEIGHT, DEFAULT_OPTIONS)
tree = None
while tree is None:
    try:
        tree = split_tree_of_rectangles(wrap_rect, SPLITS, DEFAULT_OPTIONS)
    except SplitRectangleError:
        print('.', end='')

MAP_ARRAY = []
for y in range(0, MAP_HEIGHT):
    row = []
    for x in range(0, MAP_WIDTH):
        row.append("0")
    MAP_ARRAY.append(row)


def update_rooms(node):
    if node is None:
        return

    if node.is_leaf:
        room = node.data.room

        for x in range(room.x, room.x + room.width):
            for y in range(room.y, room.y + room.height):
                MAP_ARRAY[y][x] = "1"
    else:
        # create path between leaf's centers (nodes not rooms!)
        l1 = node.left.data
        l2 = node.right.data
        c1 = (l1.x + int(l1.width / 2), l1.y + int(l1.height / 2))
        c2 = (l2.x + int(l2.width / 2), l2.y + int(l2.height / 2))

        if c1[0] == c2[0]:
            x = c1[0]
            for y in range(c1[1], c2[1]):
                MAP_ARRAY[y][x] = "2"

        if c1[1] == c2[1]:
            y = c1[1]
            for x in range(c1[0], c2[0]):
                MAP_ARRAY[y][x] = "2"

        for x in range(c1[0], c2[0]+4):
            for y in range(c1[1], c2[1]+4):
                MAP_ARRAY[y][x] = "2"

    update_rooms(node.left)
    update_rooms(node.right)


update_rooms(tree)

if not os.path.exists(MAPS_PATH):
    os.mkdir(MAPS_PATH)

maps_files = [
    f for f in os.listdir(MAPS_PATH)
    if f.endswith('.map') and os.path.isfile(os.path.join(MAPS_PATH, f))
]
maps_count = len(maps_files)

new_map_path = os.path.join(MAPS_PATH, MAP_FORMAT.format(maps_count + 1))
with open(new_map_path, 'w') as map_file:
    for r in MAP_ARRAY:
        for t in r:
            map_file.write(t)
        map_file.write('\n')

create_preview(new_map_path, MAP_WIDTH, MAP_HEIGHT, 2)

print('\nSuccess: new map ({}x{}): {}'.format(MAP_WIDTH, MAP_HEIGHT, new_map_path))
print('Saved maps: {}'.format(maps_count))
