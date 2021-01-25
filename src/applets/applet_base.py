from tkinter import Frame, Widget
from abc import abstractmethod

PADX = 2
PADY = 2


class Refreshable:

    @abstractmethod
    def refresh(self, *args):
        pass


class BaseView(Frame):

    def __init__(self, root, controller):
        super(BaseView, self).__init__(root)
        self._controller = controller

    def start(self):
        self.pack(fill='both', expand=True)

    def stop(self):
        self.pack_forget()

    def refresh(self, obj):
        pass


class BaseApplet:

    def __init__(self, model, root):
        self._root = root
        self._model = model
        self._view = BaseView(self._root, self)

    def run(self):
        self._view.start()

    def stop(self):
        self._view.stop()


