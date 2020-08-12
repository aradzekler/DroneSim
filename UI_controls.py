
import pygame
import constants

ACTIVE_BUTTON_COLOR = pygame.Color('dodgerblue1')
INACTIVE_BUTTON_COLOR = pygame.Color('dodgerblue4')

class UI_Controls:
    def __init__(self,game_map,main_s,drone):
        self.update_list = []
        self.game_map = game_map
        self.main_s = main_s
        self.drone = drone
       
        pygame.font.init()
        self.font = pygame.font.SysFont("", 20)
        self.FONT = pygame.font.Font(None, 30)
        # button creation
        auto_manual_button = self.create_button(self.game_map.map_width - 180, self.game_map.map_height - 50, 180, 50, 'Manual/Auto')
        track_button = self.create_button(self.game_map.map_width - 180, self.game_map.map_height - (100 + 1), 180, 50, 'Track')
        pause_button = self.create_button(self.game_map.map_width - 180, self.game_map.map_height - (150 + 2), 180, 50, 'Quit')
        log_button = self.create_button(self.game_map.map_width - 180, self.game_map.map_height - (200 + 3), 180, 50, 'Toggle CsvLogging')
        # button in the right-down corner.

        self.button_list = [auto_manual_button, track_button, pause_button, log_button]  # a list containing all butto
     
        for button in self.button_list:
            self.draw_button(button, self.main_s)

        self.set_event_listeners(self.drone)


    # drawing the button on pygame canvas.
    def draw_button(self,button, screen):
        """Draw the button rect and the text surface."""
        pygame.draw.rect(screen, button['color'], button['rect'])
        screen.blit(button['text'], button['text rect'])


    # update all elements in list.
    def update_all(self,to_update ):
        for element in to_update  :
            element.update()


    def display_all(self,scene_metrics):
        for element_val in range(0, len(scene_metrics)):  # adding text in the side of the screen
            self.main_s.blit(self.font.render(str(scene_metrics[element_val]), True, (0, 255, 0)), (10, 10 + (20 * element_val)))


    def set_event_listeners(self,drone):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    for button in self.button_list:
                        # `event.pos` is the mouse position.
                        if button['rect'].collidepoint(event.pos):
                            # execute function in the state machine
                            # drone.state = drone.state.on_event('switch_state')
                            if button == self.button_list[0]:  # manual/auto button
                                if drone.event == 'manual_control':  # switch states
                                    drone.event = 'auto_control'
                                    drone.on_event('auto_control')
                                else:
                                    drone.event = 'manual_control'
                                    drone.on_event('manual_control')
                            if button == self.button_list[1]:  # tracking on/off button
                                if drone.tracking:
                                    drone.tracking = False
                                else:
                                    drone.tracking = True
                            if button == self.button_list[2]:  # quit button
                                if running:
                                    csv_f = open('csvfile.csv', 'w')  # handling logging to csv file before closing.
                                    csv_f.write(log_file)
                                    csv_f.close()
                                    running = False
                            if button == self.button_list[3]:
                                if not logging:
                                    logging = True
            elif event.type == pygame.MOUSEMOTION:
                # When the mouse gets moved, change the color of the
                # buttons if they collide with the mouse.
                for button in self.button_list:
                    if button['rect'].collidepoint(event.pos):
                        button['color'] = ACTIVE_BUTTON_COLOR
                    else:
                        button['color'] = INACTIVE_BUTTON_COLOR
        if drone.event == 'manual_control':  # if we are in manual control
            drone.on_event('manual_control')

    def create_button(self,x, y, w, h, text):
        # The button is a dictionary consisting of the rect, text,
        # text rect, color and the callback function.
        text_surf = self.FONT.render(text, True, constants.WHITE)
        button_rect = pygame.Rect(x, y, w, h)
        text_rect = text_surf.get_rect(center=button_rect.center)
        button = {
            'rect': button_rect,
            'text': text_surf,
            'text rect': text_rect,
            'color': INACTIVE_BUTTON_COLOR,
        }
        return button

    def set_metrics(self,drone,clock,time):
        return ["FPS: " + str("%.0f" % clock.get_fps()),  # our telemetry window.
                    "Drone angle: " + str("%.2f" % drone.angle),
                    "Current speed: " + str("%.2f" % drone.current_speed),
                    "X Axis Movement: " + str("%.2f" % drone.move_x),
                    "Y Axis movement: " + str("%.2f" % drone.move_y),
                    "F key" + str(drone.forward),
                    "L key" + str(drone.left),
                    "R key" + str(drone.right),
                    "B key" + str(drone.backward),
                    "Collided: " + str(drone.is_colliding),
                    "Collision Detected: " + str(drone.front_detect),
                    "Time: " + str('{0:%H:%M:%S}'.format(time))]


