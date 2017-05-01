# The Rectangle Class ADT implementation

from point import *

class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.id = -1  # Canvas id after draw

    def move(self, dx, dy):
        "Move rectangle by dx and dy"
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def area(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1)

    def width(self):
        return self.x2 - self.x1

    def height(self):
        return self.y2 - self.y1

    def coords(self):
        return [self.x1, self.y1, self.x2, self.y2]

    def center(self):
        "Get the center point"
        x = (self.x1 + self.x2) / 2
        y = (self.y1 + self.y2) / 2
        return Point(x,y)

    def center_coords(self):
        "Get the center coordinates"
        x = (self.x1 + self.x2) / 2
        y = (self.y1 + self.y2) / 2
        return x,y

    def place(self, x, y):
        "Place the rectangle at a new origin (x1=x, y1=y)"
        w = self.width()
        h = self.height()
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def draw(self, canvas, **kwargs):
        id = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, **kwargs)
        self.id = id
        return id

    def config(self, **kwargs):
        canvas.itemconfig(self.id, **kwargs)

    # this is how a Rectangle object will be printed with the Python print statement:
    def __str__(self):
        return "Rectangle(%d,%d,%d,%d)"  %  (self.x1, self.y1, self.x2, self.y2)


#--------------------------------------------------

def test1():
    r = Rectangle(30, 20 ,80, 70)
    print(r)
    print("Area =", r.area())
    print("Width =", r.width())
    print("Height =", r.height())
    r.move(15,25)
    print(r)
    print("Area =", r.area())
    print("Width =", r.width())
    print("Height =", r.height())

def test2():
    r = Rectangle(30, 20 ,80, 70)
    print(r)
    assert r.area() == 2500
    assert r.width() == 50
    assert r.height() == 50
    r.move(15,25)
    assert r.x1 == 45
    assert r.y2 == 95
    assert r.area() == 2500
    print("Test PASSED")

# This is the solution to problem 10 in project #3, so please don't read it before you try it!
def test3():
    r = Rectangle(10, 10 ,160, 130)
    for i in range(25):
        r.move(9,6)
        r.draw(canvas, fill="gray97")

    app.mainloop()

# This is the solution to problem 10 in project #3, in slow motion ...
def test4():
    import time
    r = Rectangle(10, 10 ,160, 130)
    for i in range(25):
        r.move(9,6)
        time.sleep(0.08)
        r.draw(canvas, fill="gray97")
        canvas.update()
    app.mainloop()

if __name__ == "__main__":
    from eda_canvas import eda_canvas
    app = eda_canvas()
    canvas = app.canvas
    test4()


