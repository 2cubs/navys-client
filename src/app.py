# -*- coding: utf-8 -*-
__author__ = 'Alexey Elizarov (alexei.elizarov@gmail.com)'

from tkinter import Tk

from applets.main_window import MainWindowController


class App(Tk):

    def __init__(self):
        super(App, self).__init__()
        MainWindowController(self)

    def start(self):
        self.mainloop()

    def stop(self):
        self.quit()