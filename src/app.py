# -*- coding: utf-8 -*-
__author__ = 'Alexey Elizarov (alexei.elizarov@gmail.com)'

from tkinter import Tk
from applets import AppletManager
from server import DummyServer as Server


class App(Tk):

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
        self.geometry('800x600')
        self.resizable(False, False)
