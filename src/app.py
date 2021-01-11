# -*- coding: utf-8 -*-
__author__ = 'Alexey Elizarov (alexei.elizarov@gmail.com)'

from tkinter import Tk
from applets import AppletManager
from server import DummyServer as Server


class App(Tk):

    _min_width = 900
    _min_height = 700

    def __init__(self):
        super(App, self).__init__()
        self._model = Server()
        self._view = AppletManager(model=self._model, root=self)
        self._build()

    def run(self):
        self._view.run()
        self.mainloop()

    def _build(self):
        self.title('Navy Client')
        self.geometry(f'{self._min_width}x{self._min_height}')
        self.minsize(self._min_width, self._min_height)
