from abc import abstractmethod
from tkinter import Frame


class BaseController:

    _model_cls = None
    _view_cls = None

    def __init__(self, root, *args, **kwargs):
        self._root = root
        self._model = self._model_cls(**kwargs)
        self._view = self._view_cls(self)

    @property
    def root(self):
        return self._root

    def start(self, *args, **kwargs):
        self._view.pack()

    def stop(self):
        self._view.forget()


class BaseView(Frame):

    def __init__(self, controller, **kwargs):
        super().__init__(controller.root, **kwargs)
        self._controller = controller

    def pack(self):
        super().pack(fill='both', expand=True)

    def forget(self):
        self.pack_forget()


class Refreshable:

    @abstractmethod
    def refresh(self, *args, **kwargs):
        pass