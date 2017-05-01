# An Introduction to Tkinter
# tkSimpleStatusBar.py
#
# Copyright (c) 1997 by Fredrik Lundh
#
# fredrik@pythonware.com
# http://www.pythonware.com
#
# Some enhancements by Samy Zafrany (June 2014)

import tkinter as tk
from tkinter import Frame, Label, SUNKEN, BOTTOM, BOTH, W, X

class StatusBar(Frame):
    def __init__(self, master, **opt):
        opt.setdefault('font', 'Consolas 8 normal')
        opt.setdefault('bd', 1)
        opt.setdefault('relief', SUNKEN)
        opt.setdefault('anchor', W)
        opt.setdefault('fg', 'black')
        opt.setdefault('height', 0)
        opt.setdefault('padx', 2)
        opt.setdefault('pady', 0)
        Frame.__init__(self, master)
        self.label = Label(self, opt)
        self.label.pack(fill=X)
        self.stack = []

    def set(self, format, *args, **opt):
        opt['text'] = format % args
        self.label.config(**opt)
        self.label.update_idletasks()

    def append(self, chars):
        text = self.label.cget('text') + chars
        self.label.config(text=text)
        self.label.update_idletasks()

    def push(self, format, *args, **opt):
        delay = opt.pop('delay', 3)
        current_state = (self.label.cget('text'),
                         self.label.cget('font'),
                         self.label.cget('fg'),
                         self.label.cget('state'))
        self.stack.append(current_state)
        self.set(format, *args, **opt)
        self.after(int(delay*1000), self.pop)

    def pop(self):
        txt, font, fg, state = self.stack.pop()
        self.set(txt, fg=fg, font=font, stat=state)

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

def stbar_test():
    import time
    gui = tk.Tk()
    f = Frame(gui, width=600, height=360)
    status = StatusBar(gui)
    status.pack(side=BOTTOM, fill=X)
    f.pack(side=BOTTOM, fill=BOTH)
    gui.update()

    status.set("Connecting foo.bar.ac.il ...")
    for i in range(16):
        status.append(' .')
        gui.after(250)
    gui.after(1000)
    status.set("Connected, logging in...")
    gui.after(1000)
    status.set("Login accepted...")
    gui.after(2000)
    status.push("Temporary: gui for sale ... (3 seconds push ...)")
    time.sleep(4)
    status.set("Clearup in 5 seconds ...")
    time.sleep(2)
    gui.after(5000, status.clear)

    gui.mainloop()

if __name__ == "__main__":
    stbar_test()
