class State(object):
    """
    We define a state object which provides some utility functions for the
    individual states within the state machine.
    This is just an interface for our states to use.
    """

    def __init__(self):
        print('Current state:', str(self))

    def on_event(self, event):
        """
        Handle events that are delegated to this State.
        """
        pass

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__