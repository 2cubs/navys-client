# -*- coding: utf-8 -*-
__author__ = 'Alexey Elizarov (alexei.elizarov@gmail.com)'

from tkinter import Tk

# some tests

class GUI(Tk):

    def __init__(self, controller):
        super().__init__()
        self._controller = controller

    def run(self):
        self.mainloop()