import sys
import tkinter as tk
from xcanvas import *
from pytkcon import TkConsole
from statusbar import StatusBar
from design import *
from placer import LevelPlacer
import time
import easygui

class EdaPlacer(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2)
        self.create_menubar()
        self.master.config(menu=self.menubar)
        #self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas = XCanvas(self.master, bg="white", width=900, height=540, scalewidget=False, bd=0, highlightthickness=0)
        self.tkcon = TkConsole(self.master, height=12, width=90, background='ivory')
        self.status = StatusBar(self.master)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tkcon.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.status.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        self.tkcon.focus_set()

        self.lastdir = os.environ['HOMEPATH']
        self.units = []
        self.title()
        self.status.set("Level Placer Status")
        #self.update()
    
    def create_menubar(self):
        self.menubar = tk.Menu(self)
    
        # File menu
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="New", command=self.new)
        menu.add_command(label="Open", command=self.open)
        menu.add_command(label="Exit", command=self.exit)
    
        # Edit menu
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=menu)
        menu.add_command(label="Run Placer", command=self.place)
        menu.add_command(label="Collapse", command=self.collapse)
        menu.add_command(label="Clear ALL", command=self.clear)
        menu.add_separator()
        self.showNets = tk.IntVar(master=self.menubar, value=True)
        menu.add_checkbutton(label="Show nets", variable=self.showNets, command=self.draw_nets)

        # Help menu
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=menu)
        menu.add_command(label="About", command=self.about)
        menu.add_command(label="Help", command=self.help)

    def new(self):
        easygui.msgbox(
            "The 'new' method is not implemented yet",
            "Not implemented"
        )

    def open(self, locfile=None):
        if locfile is None:
            filetypes = [['.loc', 'LOCATION files']]
            #lastdir = self.lastdir + '/*.loc'
            lastdir = self.lastdir
            locfile = easygui.fileopenbox('Dialog', 'Select Location File', default=lastdir, filetypes=filetypes)
        if locfile is None:
            return
        design_dir, locfile = os.path.split(locfile)
        design_name = os.path.splitext(locfile)[0]
        self.design = Design(design_dir, design_name)
        self.title(self.design.name)
        self.clear()
        #self.canvas.fit()
        self.draw_units()
        self.draw_nets(True)
        self.status.set("units=%s  nets=%s  Total Area = %s  Total Length = %s" % \
                (len(self.design.units), len(self.design.nets), self.design.total_area(), self.design.total_length()))

    def draw_units(self):
        width = self.design.tech['design_width']
        height = self.design.tech['design_height']
        self.canvas.config(scrollregion=(-50, -50, width+50, height+50))
        self.canvas.draw_axis(10,10)
        self.design.chip.draw(self.canvas, outline='maroon', width=3, fill=None, stipple=None, tags=['root', 'chip'])
        for u in self.design.units:
            u.draw(self.canvas, fill='red', stipple='gray12')

    def draw_nets(self, show=None):
        if show is None:
            show = self.showNets.get()

        if show:
            for net in self.design.nets:
                net.draw(self.canvas)
        else:
            self.canvas.delete('net')

    def place(self, netlist=None):
        self.clear('eda&&net')
        if self.units is None:
            print("You must open a loc file first!")
            return
        self.placer = LevelPlacer(self.design.chip, self.design.units)
        self.placer.run()
        self.unplaced_units = self.placer.list_unplaced_units()
        print("Unplaced units:", self.unplaced_units)
    
        for u in self.placer.list_placed_units():
            #print(u)
            self.canvas.delete(u.name)
            u.draw(self.canvas, fill='green', stipple='gray12')
            #self.update()
            #time.sleep(0.05)
        for u in self.unplaced_units:
            self.canvas.tag_raise(u.name)
    
        if netlist is not None:
            nets = read_nets(netlist, udict)
            for n in nets:
                n.draw(self.canvas)
                #self.update()
                #time.sleep(1)
                self.canvas.delete(n.name)

        self.unplaced()

    def unplaced(self):
        "Put the unplaced units in a special container called unchip"
        x1 = self.design.chip.x1
        y1 = self.design.chip.y1 + self.design.chip.height() + 40
        x2 = self.design.chip.x2
        y2 = self.design.chip.y2 + self.design.chip.height() + 40
        self.unchip = Unit("unchip", x1, y1, x2, y2)
        self.unchip.draw(self.canvas, outline='blue', width=3, tags=['unchip', 'unplaced'])
        self.canvas.config(scrollregion=(-50,-50,x2+50,y2+50))

        placer = LevelPlacer(self.unchip, list(self.unplaced_units), False)
        placer.run()
        for u in placer.list_placed_units():
            #print(u)
            self.canvas.delete(u.name)
            u.draw(self.canvas, fill='red', stipple='gray12', tags=['unplaced'])
            #self.update()
            #time.sleep(0.05)

    def collapse(self):
        self.clear()
        for u in self.units:
            u.place(0,0)
        self.draw_units()

    def exit(self):
        answer = easygui.ynbox(
            "Exit?",
            "Are you sure you want to exit?"
        )
        if answer:
            sys.exit(0)

    def clear(self, tag='eda'):
        self.canvas.delete(tag)

    def help(self):
        try:
            self.help_top.destroy()
        except:
            pass
        self.help_top = tk.Tk()
        self.help_top.wm_title('HELP WINDOW')
        t = tk.Text(self.help_top, font=('Consolas', 10, 'bold'), width=80, height=24, background='cornsilk', foreground='blue')
        t.insert(END, "Edit the help method:\nRead some help file and insert it here")
        t.pack(fill=BOTH, expand=True)

    def title(self, postfix=None):
        ttl = "Simple Shelf Placer"
        if not postfix is None:
            ttl += ":" + " " + postfix
        self.master.wm_title(ttl)

    def about(self):
        easygui.msgbox(
            "Engineering Design Project\nEEE Depatment\nSimpleton College",
            "About EDA Application"
        )

    def debug(self, event):
        #print(event.keysym)
        #print(self.panwin.cget('sashwidth'))
        #self.panwin.config(sashwidth=6)
        #print(self.winfo_geometry())
        #self.panwin.paneconfigure(self.tkcon, minsize=100)
        pass

def placer_app(root=None):
    if root is None:
        root = tk.Tk()
    app = EdaPlacer(root)
    return app

def test_app():
    app = placer_app()
    #new_builtin('app', app)
    app.open("designs/design3/design.loc")
    #app.canvas.create_rectangle(100,100,300,300, width=2, fill='yellow', outline='maroon')
    #app.canvas.create_rectangle(200,200,400,400, width=2, fill='cyan', outline='blue')
    #app.canvas.create_rectangle(100,330,600,360, width=3, fill='AliceBlue', outline='red')
    #app.canvas.create_oval(300,340,550,500, width=4, fill='gray92', outline='Firebrick')
    app.mainloop()

if __name__ == '__main__':
    test_app()



