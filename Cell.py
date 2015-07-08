


class Cell:
    def __init__(self, *args, **kwargs):
        if args and args[0] == 0:
            self.top = 0
            self.right = 0
            self.bottom = 0
            self.left = 0
        else:
            self.top = 1
            self.right = 1
            self.bottom = 1
            self.left = 1
