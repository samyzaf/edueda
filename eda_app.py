import sys
import tkinter as tk
from tkinter import messagebox
from basics import *
from xcanvas import XCanvas
from pytkcon import TkConsole
from statusbar import StatusBar
from tkinter import TOP, BOTTOM, RIGHT, LEFT, X, Y, BOTH, VERTICAL, HORIZONTAL, N, S, E, W, SUNKEN, END
from tkinter import PanedWindow, Frame

# General template for creating a standard Application UI
# Just copy this code and replcae the methods to whatever you need
# The Main App window in this example is a Text window, but it can
# be replaced with whatever is needed

class EdaApp(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, relief=SUNKEN, bd=2)

        self.create_menubar()
        self.master.config(menu=self.menubar)
        self.pack(side=TOP, fill=BOTH, expand=True)

        panwin = PanedWindow(self, orient=VERTICAL, sashwidth=5, bd=0, bg='gray80', opaqueresize=0)
        self.canvas = XCanvas(self.master, bg="white", width=1200, height=640, x_axis=11, scalewidget=False, bd=0, highlightthickness=0)
        self.tkcon = TkConsole(self.master, height=12, width=90, background='ivory')
        self.status = StatusBar(self.master)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tkcon.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.status.pack(side=BOTTOM, fill=X, expand=False)

        self.tkcon.focus_set()


        # Put here all initializations you want to have in console
        # However it's better to use an initialization file for tkcon (look at tkcon.py)
        self.tkcon.eval('import os')
        self.tkcon.eval('import sys')
        self.tkcon.eval('from basics import *')
        self.status.set("%-60s %-16s %-16s", "Status line for this eda app (60 chars)", "Part2 (16c)", "Part3 (16c)")
    
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
        menu.add_command(label="Cut", command=self.cut)
        menu.add_command(label="Copy", command=self.copy)
        menu.add_command(label="Paste", command=self.paste)
        menu.add_command(label="Clear ALL", command=self.clear)

        # Help menu
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=menu)
        menu.add_command(label="About", command=self.about)
        menu.add_command(label="Help", command=self.help)

    def debug(self, event):
        #print(event.keysym)
        #print(self.panwin.cget('sashwidth'))
        #self.panwin.config(sashwidth=6)
        #print(self.winfo_geometry())
        #self.panwin.paneconfigure(self.tkcon, minsize=100)
        pass

    def new(self):
        messagebox.showwarning(
            "Not implemented",
            "The 'new' method is not implemented yet"
        )

    def open(self):
        messagebox.showwarning(
            "Not implemented",
            "The 'open' method is not implemented yet"
        )

    def exit(self):
        answer = messagebox.askyesno(
            "Exit?",
            "Are you sure you want to exit?"
        )
        if answer:
            sys.exit(0)

    def clear(self):
        self.tkcon.clear()

    def cut(self):
        messagebox.showwarning(
            "Not implemented",
            "The 'cut' method is not implemented yet"
        )

    def copy(self):
        messagebox.showwarning(
            "Not implemented",
            "The 'copy' method is not implemented yet"
        )

    def paste(self):
        messagebox.showwarning(
            "Not implemented",
            "The 'paste' method is not implemented yet"
        )

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

    def about(self):
        messagebox.showinfo(
            "About EDA Application",
            "Engineering Design Project\nEEE Depatment\nPublic Education College"
        )

def eda_app(root=None):
    app = EdaApp(root)
    app.pack()
    app.master.wm_title('Educational EDA Design App')
    return app

def test_app():
    app = eda_app()
    app.master.wm_title('Educational EDA Design App')
    #sys.modules['__builtin__'].__dict__['app'] = app
    app.canvas.create_rectangle(100,100,300,300, width=2, fill='yellow', outline='maroon')
    app.canvas.create_rectangle(200,200,400,400, width=2, fill='cyan', outline='blue')
    app.canvas.create_rectangle(100,330,600,360, width=3, fill='AliceBlue', outline='red')
    app.canvas.create_oval(300,340,550,500, width=4, fill='gray92', outline='Firebrick')
    app.logo = tk.PhotoImage(file="eda.gif")
    app.canvas.create_image(200, 30, image=app.logo, anchor = N+W)
    app.mainloop()

if __name__ == '__main__':
    test_app()

