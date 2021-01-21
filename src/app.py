# -*- coding: utf-8 -*-
__author__ = 'Alexey Elizarov (alexei.elizarov@gmail.com)'

from applets.main_window import MainWindow
from server import DummyServer as Server


class App:

    def __init__(self):
        super(App, self).__init__()
        self._model = Server()
        self._view = MainWindow(model=self._model)

    def run(self):
        self._view.run()
