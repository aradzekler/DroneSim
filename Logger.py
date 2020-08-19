# https://gist.github.com/robdmc/d78d48467e3daea22fe6
import logging
import datetime
import os
from itertools import islice
import sys


class Logger(object):  # pragma: no cover
    def __init__(self,main, name="", log_file=None, level='info'):
        # create logger on the current module and set its level
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.setLevel(getattr(logging, level.upper()))
        self.needs_header = True
        self.main = main
        # create a formatter that creates a single line of json with a comma at the end
        self.formatter = logging.Formatter(
            (
                '%(time)s,"%(fps)s","%(curent_speed)s","%(move_x)s","%(move_y)s","%(is_forward)s","%(is_left)s","%(is_right)s","%(is_backward)s","%(is_colliding)s","%(front_detect)s"'
            )
        )
   
        self.log_file = log_file
        if self.log_file:
            # create a channel for handling the logger (stderr) and set its format
            ch = logging.FileHandler(log_file)
        else:
            # create a channel for handling the logger (stderr) and set its format
            ch = logging.StreamHandler()
        ch.setFormatter(self.formatter)

        # connect the logger to the channel
        self.logger.addHandler(ch)

    def log(self,level='info'):
        HEADER = 'time,fps,curent_speed,move_x,move_y,is_forward,is_left,is_right,is_backward,is_colliding,front_detect\n'
        if self.needs_header:
            if self.log_file and os.path.isfile(self.log_file):
                with open(self.log_file) as file_obj:
                    if len(list(islice(file_obj, 2))) > 0:
                        self.needs_header = False
                if self.needs_header:
                    with open(self.log_file, 'a') as file_obj:
                        file_obj.write(HEADER)
            else:
                if self.needs_header:
                    sys.stderr.write(HEADER)
            self.needs_header = False

        extra = {
            'time': str(self.main.time),
            'fps': "%.0f" % self.main.clock.get_fps(),
            'angle': "%.2f" % self.main.map.drone.angle,
            'curent_speed': "%.2f" % self.main.map.drone.current_speed,
            'move_x': "%.2f" % self.main.map.drone.move_x,
            'move_y': "%.2f" % self.main.map.drone.move_y,
            'is_forward': self.main.map.drone.forward,
            'is_left': self.main.map.drone.left,
            'is_right': self.main.map.drone.right,
            'is_backward': self.main.map.drone.backward,
            'is_colliding': self.main.map.drone.is_colliding,
            'front_detect': self.main.map.drone.front_detect,
        }
        func = getattr(self.logger, level)
        func(msg="",extra=extra)