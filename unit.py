from rectangle import Rectangle
from eda_app import EdaApp

class Unit(Rectangle):
    def __init__(self, name, x1, y1, x2, y2):
        Rectangle.__init__(self, x1, y1, x2, y2)
        self.name = name

    def draw(self, canvas, **opt):
        opt.setdefault('fill', 'gray50')
        opt.setdefault('stipple', 'gray12')
        xtags = opt.get('tags', [])
        tags = ['eda', 'unit', 'shape', self.name]
        for tag in xtags:
            if tag in tags:
                continue
            else:
                tags.append(tag)
        opt['tags'] = tags
        id = Rectangle.draw(self, canvas, **opt)
        p = self.center()
        tags = ['eda', 'unit', 'text', self.name]
        for tag in xtags:
            if tag in tags:
                continue
            else:
                tags.append(tag)
        canvas.create_text(p.x, p.y, text=self.name, font="Consolas 7 bold", tags=tags)

    def split(self, direction, d):
        "split to two sub units ; direction=0 means horizontally, direction=1 vertically d=split point"
        if direction == 0:
            u1 = Unit(self.name, self.x1, self.y1, self.x2, self.y1 + d)
            u2 = Unit(self.name, self.x1, self.y1 + d, self.x2, self.y2)
        else:
            u1 = Unit(self.name, self.x1, self.y1, self.x1 + d, self.y2)
            u2 = Unit(self.name, self.x1 + d, self.y1, self.x2, self.y2)
        return u1,u2

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s(%d,%d,%d,%d)" % (self.name, self.x1, self.y1, self.x2, self.y2)



#--------------------------------------------


def test():
    from eda_canvas import eda_canvas
    app = eda_canvas()
    canvas = app.canvas
    u = Unit('foo', 50, 30 ,430, 370)
    u1, u2 = u.split(0,80)
    print(u1, u1.name)
    print(u2, u2.name)
    u1.name = 'foo1'
    u2.name = 'foo2'
    u1.draw(canvas)
    u2.draw(canvas)
    app.mainloop()

if __name__ == "__main__":
    test()

