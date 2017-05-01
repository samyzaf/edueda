# Utilities for:
#   - creating random lists of cells (units)
#   - random split of cells for generating random floorplans
import sys
import time
import tkinter as tk
from unit import Unit
from net import Net

def read_units(file):
    units = []
    f = open(file, 'r')
    for line in f:
        name, x1, y1, x2, y2 = line.strip().split()
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        u = Unit(name, x1, y1, x2, y2)
        units.append(u)
    f.close()
    return units

def units_area(units):
    a = 0
    for u in units:
        a += u.area()
    return a

# Sort the list of units by width from smalles to largest
def sort_units_by_width(units):
    return sorted(units, key=lambda u: u.width(), reverse=True)

# Sort the list of units by width from smalles to largest
def sort_units_by_height(units):
    return sorted(units, key=lambda u: u.height(), reverse=True)

def read_nets(netlist_file, udict):
    nets = []
    f = open(netlist_file)
    for line in f:
        _net, _elems, _dirvers = line.split(",")
        name = _net.split(":")[1].strip()
        element_names = _elems.split(":")[1].strip().split()
        driver_names = _dirvers.split(":")[1].strip().split()
        elements = [udict[e] for e in element_names]
        drivers = [udict[e] for e in driver_names]
        n = Net(name, elements, drivers)
        nets.append(n)
    f.close()
    return nets

def save_units(units, file):
    f = open(file, 'w')
    for u in units:
        f.write("%s %d %d %d %d\n" % (u.name, u.x1, u.y1, u.x2, u.y2))
    f.close()


# Technology file contains parameters related to
# an EDA/VLSI design project like chip width, chip height, etc.
# We build and return a dictionary containing all these parameters
def read_technology_file(filename):
    d = dict()
    f = open(filename, 'r')
    for line in f:
        line = line.strip()
        if line == "":
            continue
        key,value = line.split('=')
        key = key.strip()
        d[key] = int(value)
    return d


#------------ test utils ----------------------------

def create_random_units(units, max_depth):
    depth = 0
    while depth < max_depth:
        nunits = list()
        while units:
            u = units.pop()
            ntries = 20
            ok = False
            while random.randint(0,2) and ntries:
                ntries -= 1
                u1, u2 = random_split(u)
                if u1.width()>9 and u1.height()>9 and u2.width()>9 and u2.height()>9:
                    nunits.append(u1)
                    nunits.append(u2)
                    ok = True
                    break
            if not ok:
                nunits.append(u)
        units = nunits
        depth += 1

    ctr = 1
    for u in units:
        u.name = "u" + str(ctr)
        ctr += 1

    return units

def random_split(unit, a=0.2, b=0.4):
    a = random.uniform(0.1,0.4)
    b = random.uniform(0.1,0.4)
    w = unit.x2-unit.x1
    h = unit.y2-unit.y1
    asp = float(h)/float(w)
    if asp<a:
        dir = 1
    elif asp>1-a:
        dir = 0
    else:
        dir = random.randint(0,1)
    if dir:
        d = random.randint(int(b*w), int((1-b)*w))
    else:
        d = random.randint(int(b*h), int((1-b)*h))
    u1, u2 = unit.split(dir,d)
    return u1, u2

def random_move(unit):
    X1 = 10
    Y1 = 10
    X2 = canvas.winfo_width()
    Y2 = canvas.winfo_height()
    x1 = unit.x1
    x2 = unit.x2
    y1 = unit.y1
    y2 = unit.y2

    #print(X1, Y1, X2, Y2)

    if x1<200:
        dx = random.randint(50,100)
    elif x2>800:
        dx = random.randint(-100, -50)
    elif random.randint(0,1) == 0:
        dx = random.randint(50,100)
    else:
        dx = random.randint(-100, -50)

    if y1<200:
        dy = random.randint(50,100)
    elif y2>600:
        dy = random.randint(-100, -50)
    elif random.randint(0,1) == 0:
        dy = random.randint(50,100)
    else:
        dy = random.randint(-100, -50)

    print(unit, dx, dy)
    #raw_input("Press Enter> ")
    unit.move(0.5*dx, 0.4*dy)

def random_move2(unit):
    X1, Y1, X2, Y2 = canvas.coords('chip')
    X1 += 10
    Y1 += 10
    X2 -= 10
    Y2 -= 10
    x1 = unit.x1
    x2 = unit.x2
    y1 = unit.y1
    y2 = unit.y2

    print(X1, Y1, X2, Y2)
    print(x1, y1, x2, y2)
    W = int(0.8*(X2-X1))
    H = int(0.8*(Y2-Y1))
    while True:
        dx = random.randint(-W,W)
        dy = random.randint(-H,H)
        nx1 = x1 +dx
        nx2 = x2 +dx
        ny1 = y1 +dy
        ny2 = y2 +dy
        if X1 < nx1 < X2 and X1<nx2<X2 and Y1<ny1<Y2 and Y1<ny2<Y2:
            unit.move(dx, dy)
            break

def random_cell_list(xlow, ylow, xhigh, yhigh, ncells, area_limit=False, ldiv=7, hdiv=14):
    w1 = (xhigh-xlow)/hdiv
    w2 = (xhigh-xlow)/ldiv
    h1 = (yhigh-ylow)/hdiv
    h2 = (yhigh-ylow)/ldiv
    chip_area = (xhigh - xlow) * (yhigh - ylow)
    total_area = 0
    units = list()
    for i in range(1, ncells+1):
        name = 'u' + str(i)
        w = random.randint(w1,w2)
        x = random.randint(xlow, xhigh-w)
        h = random.randint(h1,h2)
        y = random.randint(ylow, yhigh-h)
        unit = Unit(name, x, y, x+w, y+h)
        if area_limit and total_area + unit.area() > chip_area:
            break
        total_area += unit.area()
        units.append(unit)
    print("Chip area =", chip_area)
    print("Total units area =", total_area)
    return units

def make_random_locfile(base_units=None, file=None):
    from PIL import ImageGrab
    root = Unit("chip", 0, 0, 800, 600)
    root.draw(outline='maroon', width=4, tags=['root', 'chip'])
    if base_units == None:
        base_units = [root]
    units = create_random_units(base_units, 9)
    for u in units:
        u.draw(tags=['unit'])
        #print(u.name, u.x1, u.y1, u.x2, u.y2)
    canvas.tag_raise('chip')
    rootWindow.update()
    time.sleep(1)
    #ImageGrab.grab((0,0,canvas.winfo_width(),canvas.winfo_height())).save("foo.jpg")
    if not file is None:
        save_units(units, file)

    response = raw_input("Continue? (y/n): ")
    if response == "n":
        return

    canvas.delete('unit')
    for u in units:
        random_move2(u)
        u.draw()
        u.draw(tags=['unit'])
    if not file is None:
        save_units(units, file)
    canvas.delete('text')
    canvas.tag_raise('chip')
    rootWindow.update()
    time.sleep(1)
    #ImageGrab.grab((0,0,canvas.winfo_width(),canvas.winfo_height())).save("bar.jpg")
    tk.mainloop()

def random_floor():
    root = Unit("chip", 0, 0, 800, 600)
    root.draw(outline='maroon', width=2, tags=['root', 'chip'])
    units = random_cell_list(root.x1, root.y1, root.x2, root.y2, 30)
    for u in units:
        #u.draw(tags=['unit'], fill='cornsilk', stipple="gray12")
        u.draw(tags=['unit'])
        #print(u.name, u.x1, u.y1, u.x2, u.y2)
    canvas.tag_raise('chip')
    #rootWindow.update()
    tk.mainloop()

def make_random_locfile_test1():
    b1 = Unit("b1",0,0,280,440)
    b2 = Unit("b2",0,440,600,600)
    b3 = Unit("b3",600,200,800,600)
    b4 = Unit("b4",280,0,800,200)
    b5 = Unit("b5",280,200,600,440)
    base = [b1, b2, b3, b4, b5]
    make_random_locfile(base, "cells18.loc")

def random_netlist(locfile, netsfile, num_nets):
    units = read_units(locfile)
    f = open(netsfile, 'w')
    E = list()

    for i in range(num_nets):
        random.shuffle(units)
        name = "net" + str(i)
        elements = []
        n = random_num_units()
        for u in units[0:n]:
            elements.append(u.name)
        sorted_elements = sorted(elements, key = lambda x: int(x[1:]))
        if sorted_elements in E:
            print("Skip dup")
            continue
        d = 1
        if len(elements)>3:
            if random.uniform(0,1)<0.1:
                d = 2
        drivers = sorted(elements[0:d], key = lambda x: int(x[1:]))
        line = "net: %s, elements: %s, drivers: %s\n" % (name, " ".join(sorted_elements), " ".join(drivers))
        f.write(line)
    f.close()
    return netsfile

def random_num_units():
    i = random.randint(1,100)
    if i<50:   n = 2
    elif i<70: n = 3
    elif i<85: n = 4
    elif i<92: n = 5
    elif i<96: n = 6
    elif i<98: n = 7
    else: n = random.randint(8,12)
    return n

def make_netlist_files(i, seq):
    loc = "GAL%d/gal%d.loc" % (i,i)
    for n in seq:
        nfile = "GAL%d/netlist%d.nets" % (i,n)
        random_netlist(loc, nfile, n)

def draw_floorplan_test(canvas, locfile, netlist=None, pause=True):
    chip = Unit("chip", 0, 0, 800, 600)
    chip.draw(canvas, outline='maroon', width=2, tags=['root', 'chip'])
    units = read_units(locfile)
    udict = dict()  # unit name lookup table
    for u in units:
        u.draw(canvas, tags=['unit', u.name], fill='red', stipple='gray12')
        udict[u.name] = u

    #raw_input("Press Enter for placement:")
    canvas.update()
    time.sleep(0.5)

    if netlist is not None:
        nets = read_nets(netlist, udict)
        if pause:
            for n in nets:
                n.draw(canvas)
                rootWindow.update()
                time.sleep(1)
                canvas.delete(n.name)
        else:
            for n in nets:
                n.draw(canvas)

    canvas.tag_raise('chip')
    tk.mainloop()

if __name__ == "__main__":
    #make_netlist_files(1, [10, 20, 30, 40, 50, 60, 100, 150, 200, 250, 300, 350, 400])
    #make_netlist_files(2, [10, 20, 30, 40, 50, 60, 100, 150, 200, 250, 300, 350, 400, 500])
    #make_netlist_files(3, [10, 20, 30, 40, 50, 60, 100, 150, 200, 250, 300, 350, 400, 500, 600, 800])

    #make_random_locfile_test1()
    #make_random_locfile(None, "designs/design4/design.loc")
    #random_floor()
    #draw_floorplan_test("designs/design3/design.loc", "designs/design3/netlist10.nets", False)
    #draw_floorplan_test("designs/design4/design.loc", "designs/design4/netlist250.nets", False)
    from eda_canvas import eda_canvas
    app = eda_canvas()
    canvas = app.canvas
    draw_floorplan_test(canvas, "designs/design2/design.loc", "designs/design2/netlist800.nets", False)

