from Drone import *


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
def create_button(x, y, w, h, text, callback):
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
        'callback': callback,
    }
    return button


# A callback function for the button. changes model states.
def switch_manual_auto(model):
    if model.state == Model_States.ManualState:
        model.state = Model_States.AutoState
        print("auto")
        return
    elif model.state == Model_States.AutoState:
        model.state = Model_States.ManualState
        print("manual")
        return


pygame.font.init()
WHITE = (255, 255, 255)
ACTIVE_BUTT_COLOR = pygame.Color('dodgerblue1')
INACTIVE_BUTT_COLOR = pygame.Color('dodgerblue4')
FONT = pygame.font.Font(None, 30)
clock = pygame.time.Clock()
font = pygame.font.SysFont("", 20)
pygame.init()  # initialize pygame window
print("init")
game_map = Map()  # setting map object, map choosing is inside the object.
main_s = pygame.display.set_mode((game_map.map_width, game_map.map_height))  # our main display
drone = SimpleDrone(100, 300, main_s, game_map)  # drone object, starting from coordinates 100,300
sim_map = pygame.image.load('new_map.png').convert()  # loading the map with the temp name given.
button1 = create_button(game_map.map_width - 150, game_map.map_height - 50, 150, 50, 'Manual/Auto',
                        switch_manual_auto(drone))
# button in the right-down corner.
button_list = [button1]  # a list containing all buttons
running = True  # simulation is running

while running:
    clock.tick(60)
    main_s.fill((0, 0, 0))
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
                        # execute function in the callback button list
                        # button['callback'](drone)
                        switch_manual_auto(drone)
        elif event.type == pygame.MOUSEMOTION:
            # When the mouse gets moved, change the color of the
            # buttons if they collide with the mouse.
            for button in button_list:
                if button['rect'].collidepoint(event.pos):
                    button['color'] = ACTIVE_BUTT_COLOR
                else:
                    button['color'] = INACTIVE_BUTT_COLOR

    if drone.state == Model_States.ManualState:  # if we are in manual
        # TODO: a method for logging key pressings.
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            drone.left = True
        if key[pygame.K_RIGHT]:
            drone.right = True
        if key[pygame.K_UP]:
            drone.forward = True
        if key[pygame.K_DOWN]:
            drone.backward = True
        if key[pygame.K_r]:
            drone.start_loc_x = 500
            drone.start_loc_y = 300
            drone.angle = 0
    # elif drone.state == Model_States.AutoState:
    # TODO: implement autostate
    # need to implement auto state

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
               "Collided: " + str(drone.is_colliding)]

    for button in button_list:
        draw_button(button, main_s)
    update_all(to_update)
    display_all(main_s, to_display, to_text)
    pygame.display.flip()  # show the surface we created on the actual screen.
