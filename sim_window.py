import pygame
import math as math

from Drone import SimpleDrone,deg_to_rad
from Sensor import Sensor
from Map import Map
from constants import BLACK ,WHITE ,RED

FPS = 30
ACTIVE_BUTT_COLOR = pygame.Color('dodgerblue1')
INACTIVE_BUTT_COLOR = pygame.Color('dodgerblue4')
RED1 = pygame.Color('red')
pygame.font.init()
FONT = pygame.font.Font(None, 30)

# TODO: limit movement (drone get stuck in walls) - Done
# displaying the screen.
def display_all(main_surface, display_list, text_list):
    for element in display_list:
        element.display(main_surface)
    for element_val in range(0, len(text_list)):  # adding text in the side of the screen
        main_surface.blit(font.render(str(text_list[element_val]), True, (0, 255, 0)), (10, 10 + (20 * element_val)))


# update all elements in list.
def update_all(update_list):
    for element in update_list:
        element.update()


# drawing the button on pygame canvas.
def draw_button(button, screen):
    """Draw the button rect and the text surface."""
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


# creating a simple button in pygame
def create_button(x, y, w, h, text):
    # The button is a dictionary consisting of the rect, text,
    # text rect, color and the callback function.
    text_surf = FONT.render(text, True, WHITE)
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': INACTIVE_BUTT_COLOR,
    }
    return button


clock = pygame.time.Clock()
font = pygame.font.SysFont("", 20)
pygame.init()  # initialize pygame window
print("###########~~INIT SIMULATOR WINDOW~~###########")
game_map = Map()  # setting map object, map choosing is inside the object.
main_s = pygame.display.set_mode((game_map.map_width, game_map.map_height))  # our main display
drone = SimpleDrone(100, 300, main_s, game_map)  # drone object, starting from coordinates 100,300
sim_map = pygame.image.load('new_map.png').convert()  # loading the map with the temp name given.
auto_manual_button = create_button(game_map.map_width - 150, game_map.map_height - 50, 150, 50, 'Manual/Auto')
# button in the right-down corner.
button_list = [auto_manual_button]  # a list containing all buttons
running = True  # simulation is running
size = width, sensorLength = (1, 100)
line_surface = pygame.Surface([100,100], pygame.SRCALPHA, 32)
# line_surface = line_surface.convert_alpha()


while running:
     
    clock.tick(FPS)
    main_s.fill(BLACK)
    main_s.blit(sim_map, (0, 0))  # filling screen with map
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 1 is the left mouse button, 2 is middle, 3 is right.
            if event.button == 1:
                for button in button_list:
                    # `event.pos` is the mouse position.
                    if button['rect'].collidepoint(event.pos):
                        # execute function in the state machine
                        # drone.state = drone.state.on_event('switch_state')
                        if drone.event == 'manual_control':  # switch states
                            drone.event = 'auto_control'
                            drone.on_event('auto_control')
                        else:
                            drone.event = 'manual_control'
                            drone.on_event('manual_control')
        elif event.type == pygame.MOUSEMOTION:
            # When the mouse gets moved, change the color of the
            # buttons if they collide with the mouse.
            for button in button_list:
                if button['rect'].collidepoint(event.pos):
                    button['color'] = ACTIVE_BUTT_COLOR
                else:
                    button['color'] = INACTIVE_BUTT_COLOR
    if drone.event == 'manual_control':  # if we are in manual control
        drone.on_event('manual_control')
    # TODO: a method for logging key pressings.
    # TODO: implement autostate
    # need to implement auto state

    
    # line_surface.fill(INACTIVE_BUTT_COLOR)
  

    to_update = [drone]  # update drone variables
    to_display = [drone]  # update drone displaying on map.

    to_text = ["FPS: " + str("%.0f" % clock.get_fps()),  # our telemetry window.
            "Drone angle: " + str("%.2f" % drone.angle),
            "Current speed: " + str("%.2f" % drone.current_speed),
            "X Axis Movement: " + str("%.2f" % drone.move_x),
            "Y Axis movement: " + str("%.2f" % drone.move_y),
            "F key" + str(drone.forward),
            "L key" + str(drone.left),
            "R key" + str(drone.right),
            "B key" + str(drone.backward),
            "Collided: " + str(drone.is_colliding)]

    for button in button_list:
        draw_button(button, main_s)
    # If drone is collided stop all updates
    # if not drone.is_colliding:
    #     update_all(to_update)

    update_all(to_update)
    display_all(main_s, to_display, to_text)

    #draw sensors
    sensor = Sensor(main_s, drone.rect.center, 1,drone.angle)
    sensor.update()



    angle_rad = deg_to_rad(drone.angle)
    x = drone.rect.center[0] - (sensorLength * float(math.cos(angle_rad)))
    y = drone.rect.center[1] - (sensorLength * float(math.sin(angle_rad)))
    
    drawStartPoint = (x,y)
    # line_surface.fill((255,0,0))
    # pygame.draw.line(line_surface, (255,0,0), drawStartPoint, drone.rect.center,4)  # Start at topleft and ends at bottomright.
    # main_s.blit(line_surface, (drone.rect.center[0] - line_surface.get_width() // 2, drone.rect.center[1] - line_surface.get_height() // 2 - 50)) 

    # drawStartPoint = (drone.rect.center[0] , drone.rect.center[1] - sensorLength)
    # pygame.draw.line(line_surface, RED, drawStartPoint, drone.rect.center)  # Start at topleft and ends at bottomright.
    # main_s.blit(line_surface, drawStartPoint )


    pygame.display.flip()  # show the surface we created on the actual screen.
