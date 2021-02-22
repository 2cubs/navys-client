from tkinter import Frame, X, Label, BOTH, Menu, DISABLED, NORMAL, Toplevel

from applets.base import BaseController, BaseFrameView
from applets.applet_manager import AppletManagerController
from applets.connection_manager import ConnectionManager
# from applets.new_connection import NewConnectionController
from client.Client import Client


class MainWindowModel:
    def __init__(self):
        self.title = 'Navy Client'
        self.min_width = 900
        self.min_height = 700
        self.applet_manager = None


class MainWindowFrameView(BaseFrameView):
    def __init__(self, controller):
        super(MainWindowFrameView, self).__init__(controller)
        self._main_menu = MainMenu(self._controller)
        self._applet_frame = AppletFrame(self._controller.root)
        self._status_bar_frame = StatusBarFrame(self._controller.root)

    @property
    def applet_frame(self):
        return self._applet_frame

    @property
    def main_menu(self):
        return self._main_menu


class MainWindowController(BaseController):

    _model_cls = MainWindowModel
    _view_cls = MainWindowFrameView

    def __init__(self, root):
        super(MainWindowController, self).__init__(root)
        self._root.title(self._model.title)
        self._root.geometry(f'{self._model.min_width}x{self._model.min_height}')
        self._root.minsize(self._model.min_width, self._model.min_height)
        self._root.config(menu=self._view.main_menu)

    def create_new_connection(self):
        pass
        # NewConnectionController(Toplevel(self._root))

    def disconnect(self):
        self._model.applet_manager.stop()

    def connect(self):
        ConnectionManager(self._root)

    def connect_to(self):
        try:
            # TODO: to be refactored
            instance = Client.get_instance()
        except Exception as e:
            raise e
        else:
            self._model.applet_manager = AppletManagerController(self._view.applet_frame, instance=instance)
            self._model.applet_manager.start()


class StatusBarFrame(Frame):
    def __init__(self, root):
        super(StatusBarFrame, self).__init__(root)
        self.pack(fill=X)
        Label(self).pack()


class AppletFrame(Frame):
    def __init__(self, root):
        super(AppletFrame, self).__init__(root)
        self.pack(expand=True, fill=BOTH)


class MainMenu(Menu):
    def __init__(self, controller):
        super(MainMenu, self).__init__(controller.root)
        self._controller = controller
        self._server = Menu(self, tearoff=0)
        self._server.add_command(label='New...', command=self.create_new_connection)
        self._server.add_command(label='Connect...', command=self.connect)
        self._server.add_command(label='Connect Recent', command=self.dummy)
        self._server.add_separator()
        self._server.add_command(label='Connect', command=self.connect_to)
        self._server.add_command(label='Disconnect', state='disabled', command=self.disconnect)
        self._server.add_separator()
        self._server.add_command(label='Exit', command=self.exit)
        self.add_cascade(label='Server', menu=self._server)

    def create_new_connection(self):
        self._controller.create_new_connection()

    def dummy(self):
        pass

    def exit(self):
        self._controller.root.stop()

    def connect_to(self):
        """To be replaced"""
        try:
            self._controller.connect_to()
        except Exception as e:
            print(e)
        else:
            self._server.entryconfig('Connect', state=DISABLED)
            self._server.entryconfig('Disconnect', state=NORMAL)

    def connect(self):
        self._controller.connect()

    def disconnect(self):
        self._server.entryconfig('Connect', state=NORMAL)
        self._server.entryconfig('Disconnect', state=DISABLED)
        self._controller.disconnect()


