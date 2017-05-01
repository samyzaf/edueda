from design import *
import time

class LevelPlacer:
    def __init__(self, chip, units, log=True):
        self.log = log
        self.shelf = dict()
        self.anchor = dict()
        self.shelf[0] = []
        self.chip = chip
        self.anchor[0] = (self.chip.x1, self.chip.y1)
        self.units = units
        #self.units.sort(key=lambda u: u.height(), reverse=True)

    def run(self):
        unplaced_area = 0
        for unit in self.units:
            placed = self.place(unit)
            if not placed:
                if self.log:
                    print("Failed to place unit:", unit)
                unplaced_area += unit.area()
        if self.log:
            print("UNPLACEAD AREA =", unplaced_area)
            print("SUCCESS RATE =", (self.chip.area() - unplaced_area) / float(self.chip.area()))

    def place(self, unit):
        placed = False
        n = max(self.shelf.keys())
        for k in range(n+1):
            x,y = self.anchor[k]
            available_height = self.chip.y2 - y
            if available_height < unit.height():
                break # no room for unit at all !
            available_width = self.chip.x2 - x
            if available_width < unit.width():
                continue
            unit.place(x, y)
            if self.log and k<n-1: print("Optimized placement! great!!", unit)
            placed = True
            x += unit.width()
            self.anchor[k] = (x,y)
            self.shelf[k].append(unit)
            break

        if not placed:
            x = self.chip.x1
            y = max([u.y2 for u in self.shelf[n]])
            available_height = self.chip.y2 - y
            available_width = self.chip.x2 - x
            if unit.height() <= available_height and unit.width() <= available_width:
                unit.place(x, y)
                placed = True
                x += unit.width()
                self.shelf[n+1] = [unit]
                self.anchor[n+1] = (x,y)

        return placed

    def list_placed_units(self):
        placed_units = []
        n = max(self.shelf.keys())
        for k in range(n+1):
            for u in self.shelf[k]:
                placed_units.append(u)
        return placed_units

    def list_unplaced_units(self):
        return set(self.units).difference(self.list_placed_units())

#---------------------------------------------------------------

def throw_random_cells_test():
    from eda_canvas import EdaCanvas
    app = EdaCanvas(width=300, height=200)
    canvas = app.canvas
    top = Unit("chip", 0, 0, 300, 200)
    top.draw(canvas, outline='maroon', width=2, tags=['top', 'chip'])
    units = random_cell_list(top.x1, top.y1, top.x2, top.y2, 200, True)
    units = sort_units_by_height(units)
    for u in units:
        u.draw(canvas, tags=['unit'], fill='cornsilk', stipple='gray12')
        app.update()
        time.sleep(0.1)
        #u.draw(canvas, tags=['unit'])
        #print(u.name, u.x1, u.y1, u.x2, u.y2)
    canvas.tag_raise('chip')
    app.mainloop()

def placement_test(design_path):
    des = Design(design_path)
    from eda_canvas import EdaCanvas
    app = EdaCanvas()
    canvas = app.canvas
    #app.canvas.fit()
    des.chip.draw(canvas, outline='maroon', width=3, fill=None, stipple=None, tags=['root', 'chip'])
    #units = random_cell_list(chip.x1, chip.y1, chip.x2, chip.y2, 200, True)
    for u in des.units:
        u.draw(canvas, tags=['unit', u.name], fill='red', stipple='gray12')

    #raw_input("Press Enter for placement:")
    app.update()
    time.sleep(1)

    lp = LevelPlacer(des.chip, des.units)
    lp.run()
    unplaced_units = lp.list_unplaced_units()
    print("Unplaced units:", unplaced_units)

    for u in lp.list_placed_units():
        #print(u)
        canvas.delete(u.name)
        u.draw(canvas, tags=['unit'], fill='green', stipple='gray12')
        app.update()
        #time.sleep(0.05)
    for u in unplaced_units:
        canvas.tag_raise(u.name)

    for n in des.nets:
        n.draw(canvas)
        app.update()
        time.sleep(1)
        canvas.delete(n.name)

    canvas.tag_raise('chip')
    app.mainloop()

if __name__ == "__main__":
    #throw_random_cells_test()
    placement_test("designs/design1")



