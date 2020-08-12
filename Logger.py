
class Logger:
    def __init__(self):
        self.update_list = []

    def log(self,drone,clock,time):
        return [str("%.0f" % clock.get_fps()),  # our telemetry window.
                str("%.2f" % drone.angle), str("%.2f" % drone.current_speed), str("%.2f" % drone.move_x),
                str("%.2f" % drone.move_y), str(drone.forward), str(drone.left), str(drone.right), str(drone.backward),
                str(drone.is_colliding), str(drone.front_detect), str('{0:%H:%M:%S}'.format(time))]


    # def write_log(self):
    # # HANDLING CSV LOGGING
    #     line = ""
    #     for text in scene_metrics:
    #         line += text + ","
    #     line = line[:-1]
    #     line += "\n"
    #     log_file += line