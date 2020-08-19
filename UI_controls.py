
import pygame
import constants
from interfaces.pygame_object_interface import PyGameObjectInterface

ACTIVE_BUTTON_COLOR = pygame.Color('dodgerblue1')
INACTIVE_BUTTON_COLOR = pygame.Color('dodgerblue4')

class UiControls(PyGameObjectInterface):
    def __init__(self,main):
        self.main = main
        self.scene_metrics = []
        self.fonts = constants.Fonts()

        self.init_buttons()

        # pygame.time.set_timer(pygame.USEREVENT, 1000)


    def update(self):
        self.trigger_event_listeners()


    def display(self):
        """Draw the button rect and the text surface."""
        for button in self.button_list:
            pygame.draw.rect(self.main.surface, button['color'], button['rect'])
            self.main.surface.blit(button['text'], button['text rect'])


    def trigger_event_listeners(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.stopped = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == constants.MouseButton.left.value:
                    for button in self.button_list:
                        # `event.pos` is the mouse position.
                        if button['rect'].collidepoint(event.pos):
                            # execute function in the state machine
                            # drone.state = drone.state.on_event('switch_state')
                            if button == self.button_list[0]:  # manual/auto button
                                if self.main.map.drone.event == 'manual_control':  # switch states
                                    self.main.map.drone.event = 'auto_control'
                                    self.main.map.drone.on_event('auto_control')
                                else:
                                    self.main.map.drone.event = 'manual_control'
                                    self.main.map.drone.on_event('manual_control')
                            if button == self.button_list[1]:  # tracking on/off button
                                if self.main.map.drone.tracking:
                                    self.main.map.drone.tracking = False
                                else:
                                    self.main.map.drone.tracking = True
                            if button == self.button_list[2]:  # quit button
                                self.main.stopped = True
                            if button == self.button_list[3]: # log data button
                                if self.main.log_data:
                                    self.main.log_data = False
                                else:
                                    self.main.log_data = True
            elif event.type == pygame.MOUSEMOTION:
                # When the mouse gets moved, change the color of the
                # buttons if they collide with the mouse.
                for button in self.button_list:
                    if button['rect'].collidepoint(event.pos):
                        button['color'] = ACTIVE_BUTTON_COLOR
                    else:
                        button['color'] = INACTIVE_BUTTON_COLOR
        if self.main.map.drone.event == 'manual_control':  # if we are in manual control
            self.main.map.drone.on_event('manual_control')


    def init_buttons(self):
        """Init buttons list"""
        buttonsWidthLocation = self.main.surface.get_width() - 190
        buttonHeight = 50
        #TODO: find out how to add border to button
        auto_manual_button = self.create_button(buttonsWidthLocation, 0, 'Manual/Auto')
        track_button = self.create_button(buttonsWidthLocation, buttonHeight ,'Track')
        pause_button = self.create_button(buttonsWidthLocation, buttonHeight*2, 'Quit')
        log_button = self.create_button(buttonsWidthLocation, buttonHeight*3, 'Toggle CsvLogging')
  
        self.button_list = [auto_manual_button, track_button, pause_button, log_button]  # a list containing all butto


    def create_button(self,x, y,text, width=180, height=50):
        # The button is a dictionary consisting of the rect, text,
        # text rect, color and the callback function.
        text_surf = self.fonts.font_size_big.render(text, True, constants.WHITE)
        button_rect = pygame.Rect(x, y, width, height)
        text_rect = text_surf.get_rect(center=button_rect.center)
     

        button = {
            'rect': button_rect,
            'text': text_surf,
            'text rect': text_rect,
            'color': INACTIVE_BUTTON_COLOR,
        }
        return button
