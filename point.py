#################
#               #
#  Point Class  #
#               #
#################

class Point:
    "Create an object of type Point from two integers"
    def __init__(self, x, y, radius=4):
        self.x = x
        self.y = y
        self.radius = radius

    def move(self,dx,dy):
        "Move point by dx and dy"
        self.x += dx
        self.y += dy

    def place(self, x, y):
        "Place the point at a new center (x, y)"
        self.x = x
        self.y = y

    def draw(self, canvas, **opt):
        opt.setdefault('width', 0)
        opt.setdefault('fill', 'blue')
        opt.setdefault('tags', ['POINT'])
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        id = canvas.create_rectangle(x1, y1, x2, y2, **opt)
        self.id = id
        return id

    def text(self, canvas, t, **opt):
        dx = opt.pop('dx', 0)
        dy = opt.pop('dy', -4)
        opt.setdefault('anchor', 's')
        opt.setdefault('font', 'Consolas 12')
        opt.setdefault('tags', ['TEXT', 'POINT'])
        opt['text'] = t
        id = canvas.create_text(self.x + dx, self.y + dy, **opt)
        return id

    # this is how a Point object will be printed with the Python print statement:
    def __str__(self):
        return "Point(%d,%d)"  %  (self.x, self.y)

#-----------------------------------------

def test1():
    print("\n===== Testing The Point Class =====")
    p1 = Point(20,20)
    p2 = Point(50,60)
    print("Testing the Python print statement on Point p1:")
    print(p1)
    print("Testing the Python print statement on Point p2:")
    print(p2)
    print("Test 1: PASSED")

def test2():
    p1 = Point(20,20)
    p2 = Point(50,60)
    assert p1.x == 20 and p1.y == 20
    assert p2.x == 50 and p2.y == 60
    p1.move(100, 200)
    p2.move(100, 200)
    assert p1.x == 120 and p1.y == 220
    assert p2.x == 150 and p2.y == 260
    print("Test 2: PASSED")

def test3():
    from eda_canvas import eda_canvas
    app = eda_canvas()
    canvas = app.canvas
    p1 = Point(20,30)
    p2 = Point(70,80, 8)
    p3 = Point(130, 150, 24)
    print(p1, p2, p3)
    print("Testing the Point draw method:")
    p1.draw(canvas)
    p2.draw(canvas, fill="blue")
    p3.draw(canvas, fill='tan', outline='brown', width=4)
    p3.place(200, 120)
    p3.draw(canvas, fill='yellow', outline='green', width=4)
    p3.place(300, 220)
    p3.radius = 30
    p3.draw(canvas, fill='cyan', outline='blue', width=10)
    app.mainloop()

if __name__ == "__main__":
    #test1()
    #test2()
    test3()

