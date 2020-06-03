from State import State


class ManualState(State):
    """
    The state which indicates drone is in manual control
    """

    def on_event(self, event):
        if event == 'manual_control':
            return ManualState
        if event == 'switch_state':
            return AutoState()
        return self


class AutoState(State):
    """
    The state which indicates that the drone is in autonomous state
    """

    def on_event(self, event):
        if event == 'auto_control':
            return AutoState
        if event == 'switch_state':
            return ManualState()
        return self
# End of our states.
