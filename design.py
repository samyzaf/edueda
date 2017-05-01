import sys, os
from utils import *
from unit import Unit

class Design:
    def __init__(self, directory, name="design"):
        if name is None:
            name = os.path.split(directory)[1].lower()
        self.name = name
        self.tech_file = os.path.join(directory, name + '.tech')
        self.loc_file = os.path.join(directory, name + '.loc')
        self.nets_file = os.path.join(directory, name + '.nets')
        self.tech = read_technology_file(self.tech_file)
        self.units = read_units(self.loc_file)
        self.udict = dict()  # unit name lookup table
        for unit in self.units:
            self.udict[unit.name] = unit
        #self.lastdir = os.path.normpath(os.path.dirname(file))
        if not os.path.exists(self.nets_file):
            raise Exception("Netlist file not found!")
        self.nets = read_nets(self.nets_file, self.udict)
        self.ndict = dict()  # net name lookup table
        for net in self.nets:
            self.ndict[net.name] = net
        self.width = self.tech['design_width']
        self.height = self.tech['design_height']
        self.chip = Unit("chip", 0, 0, self.width, self.height)

    def unit(self, name):
        return self.udict[name]

    def net(self, name):
        return self.ndict[name]

    def total_length(self):
        length = 0
        for net in self.nets:
            length += net.length()
        return length

    def total_area(self):
        return units_area(self.units)

#---------------------------------------------------

def test1():
    from eda_canvas import eda_canvas
    app = eda_canvas()
    canvas = app.canvas
    design_path = "designs/design1"
    des = Design(design_path)
    for unit in des.units:
        unit.draw(canvas)
    for net in des.nets:
        net.draw(canvas)
    app.mainloop()

if __name__ == "__main__":
    test1()


