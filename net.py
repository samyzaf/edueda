from line import Line
from point import Point
from unit import Unit

class Net:
    def __init__(self, name, elements, drivers):
        self.name = name
        self.elements = elements
        self.drivers = drivers
        self.receivers = [e for e in elements if not e in drivers]

    def length(self):
        "Half perimeter length estimation"
        length = 0
        for drv in self.drivers:
            x1, y1 = drv.center_coords()
            for elem in self.elements:
                if elem in self.drivers:
                    continue
                x2, y2 = elem.center_coords() 
                length += abs(x1 - x2) + abs(y1 - y2)

        return length

    def draw(self, canvas, **opt):
        opt.setdefault('width', 1)
        opt.setdefault('fill', 'blue')
        opt.setdefault('arrow', 'last')
        opt.setdefault('dash', [])
        opt.setdefault('arrowshape', [8, 12, 3])
        for d in self.drivers:
            x1, y1 = d.center_coords()
            for e in self.elements:
                if e in self.drivers: continue
                x2, y2 = e.center_coords() 
                l = Line.from_coords(x1, y1, x2, y2)
                opt['tags'] = ['eda', 'net', self.name]
                l.draw(canvas, **opt)

    def __str__(self):
        drivers = [u.name for u in self.drivers]
        receivers = [u.name for u in set(self.elements).difference(self.drivers)]
        #receivers = list(set(self.elements).difference(self.drivers))
        return "Net(%s, %s, %s)" % (self.name, drivers, receivers)

    def __repr__(self):
        return self.__str__()


#--------------------------------------------


def test1():
    from eda_canvas import eda_canvas
    app = eda_canvas()
    canvas = app.canvas
    u1 = Unit('foo1', 50, 30 ,80, 70)
    u2 = Unit('foo1', 50, 130 ,80, 170)
    u3 = Unit('bar1', 160, 100, 200, 140)
    u4 = Unit('bar2', 260, 370 ,320, 420)
    u5 = Unit('bar3', 260, 470 ,320, 520)
    elements = [u1, u2, u3, u4, u5]
    drivers = [u1, u2]
    net = Net('kuku', elements, drivers)
    print("Net length =", net.length())
    for u in elements:
        u.draw(canvas)
    print(net)
    net.draw(canvas)
    app.mainloop()

if __name__ == "__main__":
    test1()
