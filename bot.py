

class bot(object):
    def __init__(self, canvas, x, y, *args, **kwargs):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(x, y, *args, **kwargs)
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.move(self.id, dx, dy)

