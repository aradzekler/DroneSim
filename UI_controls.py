
import pygame
import constants

ACTIVE_BUTTON_COLOR = pygame.Color('dodgerblue1')
INACTIVE_BUTTON_COLOR = pygame.Color('dodgerblue4')

class UiControls:
    def __init__(self,game_map,main_s,drone):
        self.update_list = []
        self.game_map = game_map
        self.main_s = main_s
        self.drone = drone
        # self.play_game_callback = play_game_callback
        self.scene_metrics = []
       
       
        pygame.time.set_timer(pygame.USEREVENT, 1000)
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


    # drawing the button on pygame canvas.
    def draw_button(self,button, screen):
        """Draw the button rect and the text surface."""
        pygame.draw.rect(screen, button['color'], button['rect'])
        screen.blit(button['text'], button['text rect'])

    def update(self):
        self.trigger_event_listeners()

    def display(self):
        for button in self.button_list:
            self.draw_button(button, self.main_s)


    def trigger_event_listeners(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a = True
                # self.play_game_callback(False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    for button in self.button_list:
                        # `event.pos` is the mouse position.
                        if button['rect'].collidepoint(event.pos):
                            # execute function in the state machine
                            # drone.state = drone.state.on_event('switch_state')
                            if button == self.button_list[0]:  # manual/auto button
                                if self.drone.event == 'manual_control':  # switch states
                                    self.drone.event = 'auto_control'
                                    self.drone.on_event('auto_control')
                                else:
                                    self.drone.event = 'manual_control'
                                    self.drone.on_event('manual_control')
                            if button == self.button_list[1]:  # tracking on/off button
                                if self.drone.tracking:
                                    self.drone.tracking = False
                                else:
                                    self.drone.tracking = True
                            if button == self.button_list[2]:  # quit button
                                a = True
                                # self.play_game_callback(False)
                                # if running:
                                #     csv_f = open('csvfile.csv', 'w')  # handling logging to csv file before closing.
                                #     csv_f.write(log_file)
                                #     csv_f.close()
                                #     running = False
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
        if self.drone.event == 'manual_control':  # if we are in manual control
            self.drone.on_event('manual_control')

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
