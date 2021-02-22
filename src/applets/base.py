from abc import abstractmethod
from tkinter import Frame, Toplevel


class BaseController:

    _model_cls = None
    _view_cls = None

    def __init__(self, root, **kwargs):
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


class BaseFrameView(Frame):

    def __init__(self, controller, **kwargs):
        super().__init__(controller.root, **kwargs)
        self._root = controller.root
        self._controller = controller

    def pack(self):
        super().pack(fill='both', expand=True)

    def forget(self):
        self.pack_forget()


class BaseToplevelView(Toplevel):

    _title = ''
    _is_resizable = True

    def __init__(self, controller, **kwargs):
        super().__init__(controller.root, **kwargs)
        self._controller = controller
        self._root = self._controller.root
        self.__config__()
        self.__build__()
        self.__refresh__()
        self.modal = ModalManager(self._controller)
        # self.update_idletasks()
        # print(self.geometry())

    def __config__(self):

        # Set title
        self.title(self._title)
        self.focus_force()
        self.grab_set()

        # Set window size:
        self.update_idletasks()
        w = getattr(self, '_width', None)
        h = getattr(self, '_height', None)
        if w and h:
            x = int(self.master.winfo_x() + (self.master.winfo_width() - w)/2)
            y = int(self.master.winfo_y() + (self.master.winfo_height() - h)/2)
            self.geometry(f'{w}x{h}+{x}+{y}')
            self.minsize(w, h)

        # Set resizeable
        self.resizable(self._is_resizable, self._is_resizable)

    @abstractmethod
    def __build__(self):
        pass

    def __refresh__(self):
        pass

    def close(self):
        self.destroy()


class ModalManager:

    def __init__(self, controller):
        self._controller = controller
        self._view = None

    def open(self, view, **kwargs):
        self._view = view(self._controller, **kwargs)

    def close(self):
        self._view.close()
        self._view = None

    @property
    def feedback(self):
        return self._view.feedback


class Refreshable:

    @abstractmethod
    def refresh(self, *args, **kwargs):
        pass