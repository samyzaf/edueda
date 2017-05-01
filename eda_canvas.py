import sys
import tkinter as tk
from tkinter import messagebox
from xcanvas import XCanvas

# General template for creating a standard Application UI
# Just copy this code and replcae the methods to whatever you need
# The Main App window in this example is an XCanvas window, but it can
# be replaced with whatever is needed

class EdaCanvas(tk.Frame):
    def __init__(self, master=None, **opt):
        opt.setdefault('width', 800)
        opt.setdefault('height', 600)
        opt.setdefault('bg', 'white')
        opt.setdefault('bd', 0)
        opt.setdefault('highlightthickness', 0)
        opt.setdefault('scrollregion', (-50, -50, opt['width']+50, opt['height']+50))
        self.region = opt['scrollregion']

        tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2)
        self.create_menubar()
        self.master.config(menu=self.menubar)
        self.pack(fill=tk.BOTH, expand=True)
        self.canvas = XCanvas(self, **opt)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def create_menubar(self):
        self.menubar = tk.Menu(self)

        #----- File Menu -----
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="New", command=self.new)
        menu.add_command(label="Open", command=self.open)
        menu.add_command(label="Exit", command=self.exit)
    
        #----- Edit Menu -----
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=menu)
        menu.add_command(label="Cut", command=self.cut)
        menu.add_command(label="Copy", command=self.copy)
        menu.add_command(label="Paste", command=self.paste)
        menu.add_command(label="Clear ALL", command=self.clear)

        #----- Help Menu -----
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=menu)
        menu.add_command(label="About", command=self.about)
        menu.add_command(label="Help", command=self.help)

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
        self.canvas.delete('item')

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
        t = tk.Text(self.help_top, font='Consolas 10 bold', width=80, height=24, background='cornsilk', foreground='blue')
        t.insert(tk.END, "Edit the help method:\nRead some help file and insert it here")
        t.pack(fill=tk.BOTH, expand=True)

    def about(self):
        messagebox.showinfo(
            "About EDA Application",
            "Engineering Design Project\nEEE Depatment\nPublic Education College"
        )


def eda_canvas(root=None):
    if root is None:
        root = tk.Tk()
    app = EdaCanvas(root)
    app.master.wm_title('EDA Canvas Application')
    return app


if __name__ == '__main__':
    app = EdaCanvas(bg='ivory', width=800, height=600)
    app.master.wm_title('My Canvas Application')
    app.canvas.create_rectangle(100, 120, 400, 230, width=2, outline='blue', fill='yellow', tags=['item'])
    app.canvas.create_oval(400, 320, 600, 530, width=2, outline='blue', fill='cyan', tags=['item'])
    app.mainloop()


