import Helpers

"""
PID Controller class.
"""


class PID:
    """
    Initialization with 3 parameters:
    kp = Proportional gain value in seconds.
    ki = Integral gain value in seconds.
    kd = Derivative gain value in seconds.
    update_t = Time it takes between every PID update in seconds.
    set_point = The value we try to reach, starting in 0.
    output_limits = limits that the output will not go below or above, output_limits=(Lower_limit, Higher_limit)
    auto_mode = boolean, True if automatic, False if manual
    """

    def __init__(self, kp=0.0, ki=0.0, kd=0.0, update_t=0.1, set_point=0, output_limits=(None, None), auto_mode=True):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.update_t = update_t
        self.set_point = set_point
        self.auto_mode = auto_mode
        self._min_output, self._max_output = output_limits
        self._proportional = 0
        self._integral = 0
        self._derivative = 0
        self._last_time = Helpers.get_current_time()
        self._last_output = None
        self._last_input = None

    """
    Updating the controller with _input, calculate and return output if enough
    time has passed (or None if no value was calculated)
    dt: If set, uses this value for time jumps instead of real time. (for simulations).
    """

    def __call__(self, _input, dt=None):
        if not self.auto_mode:  # if we are in manual mode, dont calculate.
            return self._last_output

        now = Helpers.get_current_time()  # getting current time.

        if dt is None:
            dt = now - self._last_time if now - self._last_time else 1e-16
        elif dt <= 0:
            raise ValueError('dt has a non-positive value {}. Value Must be non-negative.'.format(dt))

        if self.update_t is not None and dt < self.update_t and self._last_output is not None:
            # only update every update_t seconds
            return self._last_output

        # COMPUTING ERROR TERM, reducing from the setpoint our current input (how far are we from the setpoint).
        error = self.set_point - _input
        d_input = _input - (self._last_input if self._last_input is not None else _input)

        # COMPUTING PROPORTIONAL TERM.
        self._proportional = self.kp * error

        # COMPUTING INTEGRAL TERM.
        self._integral += self.ki * error * dt
        self._integral = Helpers.clamp(self._integral, self.output_limits)

        # COMPUTING DERIVATIVE TERM.
        self._derivative = -self.kd * d_input / dt

        # final output, summing all values together.
        output = self._proportional + self._integral + self._derivative
        output = Helpers.clamp(output, self.output_limits)

        # keep track of state
        self._last_output = output
        self._last_input = _input
        self._last_time = now

        return output

    # Method for representing the process in string form.
    def __repr__(self):
        return (
            '{self.__class__.__name__}('
            'Kp={self.Kp!r}, Ki={self.Ki!r}, Kd={self.Kd!r}, '
            'setpoint={self.setpoint!r}, update_t={self.update_t!r}, '
            'output_limits={self.output_limits!r}, auto_mode={self.auto_mode!r}, '
            'proportional_on_measurement={self.proportional_on_measurement!r}'
            ')'
        ).format(self=self)

    def set_auto_mode(self, enabled, last_output=None):
        """
        Enable or disable the PID controller, optionally setting the last output value.
        This is useful if some system has been manually controlled and if the PID should take over.
        In that case, pass the last output variable (the control variable) and it will be set as
        the starting I-term when the PID is set to auto mode.
        :param enabled: Whether auto mode should be enabled, True or False
        :param last_output: The last output, or the control variable, that the PID should start
            from when going from manual mode to auto mode
        """
        if enabled and not self.auto_mode:
            # switching from manual mode to auto, reset
            self.reset()

            self._integral = last_output if last_output is not None else 0
            self._integral = Helpers.clamp(self._integral, self.output_limits)

        self.auto_mode = enabled

    # Method for resetting the controller
    def reset(self):
        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self._last_time = Helpers.get_current_time()
        self._last_output = None
        self._last_input = None


    '''
    getters and setters.
    '''
    @property
    def components(self):
        return self._proportional, self._integral, self._derivative

    @property
    def tunings(self):
        return self.kp, self.ki, self.kd

    @tunings.setter
    def tunings(self, tunings):
        """Set the PID tunings."""
        self.kp, self.ki, self.kd = tunings

    @property
    def auto_mode(self):
        """Whether the controller is currently enabled (in auto mode) or not."""
        return self.auto_mode

    @auto_mode.setter
    def auto_mode(self, enabled):
        """Enable or disable the PID controller."""
        self.set_auto_mode(enabled)

    @property
    def output_limits(self):
        """Outputs limits."""
        return self._min_output, self._max_output

    @output_limits.setter
    def output_limits(self, limits):
        if limits is None:
            self._min_output, self._max_output = None, None
            return

        min_output, max_output = limits

        if None not in limits and max_output < min_output:
            raise ValueError('lower limit must be less than upper limit')

        self._min_output = min_output
        self._max_output = max_output

        self._integral = Helpers.clamp(self._integral, self.output_limits)
        self._last_output = Helpers.clamp(self._last_output, self.output_limits)
