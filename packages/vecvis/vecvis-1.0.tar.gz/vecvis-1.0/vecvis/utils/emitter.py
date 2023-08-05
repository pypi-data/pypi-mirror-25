class Emitter:
    """doc
    """
    def __init__(self):
        self.__listeners = {}

    def add_listener(self, event_name, callback):
        if not callable(callback):
            return

        if event_name not in self.__listeners:
            self.__listeners[event_name] = []
        self.__listeners[event_name].append(callback)

    def remove_listener(self, event_name, callback):
        if event_name not in self.__listeners:
            return
        if callback in self.__listeners[event_name]:
            self.__listeners[event_name].remove(callback)

    def _emit(self, event_name, event_object = None):
        if event_name not in self.__listeners:
            return
        for listener in self.__listeners[event_name]:
            listener(event_object)
