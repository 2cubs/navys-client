# -*- coding: utf-8 -*-
__author__ = 'Alexey Elizarov (alexei.elizarov@gmail.com)'

from gui import GUI


class App:

    def __init__(self):
        self._model = None
        self._view = GUI(self)

    def run(self):
        self._view.mainloop()

    def quit(self):
        self._view.quit()