class Callback:
    def __init__(self, path, sufix):
        self.path = path
        self.sufix = sufix

    def __repr__(self):
        return self.path + "=" + self.sufix
