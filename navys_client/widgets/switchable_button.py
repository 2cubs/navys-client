from tkinter import NORMAL
from tkinter.ttk import Button


class SwitchableButton(Button):

    def __init__(self, master, switches, **kwargs):
        super(SwitchableButton, self).__init__(master, **kwargs)
        self._switches = switches

    def switch(self, state):
        self.config(state=NORMAL, text=self._switches[state])