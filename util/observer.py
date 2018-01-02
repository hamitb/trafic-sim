class Observed(object):
    def __init__(self):
        self._observers = []

    def register(self, f):
        self._observers.append(f)

    def unregister(self, f):
        try:
            self._observers.remove(f)
        except:
            print("Couldn't unregister observer")

    def notify(self, socket=None):
        for f in self._observers:
            f(self, socket)
