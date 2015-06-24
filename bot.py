

class bot(object):
    def __init__(self, canvas, minr, minc, maxr, maxc, x, y, *args, **kwargs):
        self.canvas = canvas
        self.minr = minr
        self.minc = minc
        self.maxr = maxr
        self.maxc = maxc
        self.id = self.canvas.create_rectangle(x, y, *args, **kwargs)
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.move(self.id, dx, dy)

