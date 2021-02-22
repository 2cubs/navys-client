from importlib import import_module
from tkinter import PanedWindow, Frame, Scrollbar, VERTICAL, RIGHT, Y, BOTH, END
from tkinter.ttk import Treeview

from applets import PADX, PADY
from applets.base import BaseFrameView
from applets.base import BaseController


class AppletManagerModel:

    def __init__(self, instance):
        self.applet = None
        self.instance = instance

    @staticmethod
    def get_applet(applet):
        try:
            module = import_module('.'.join(['applets', applet]))
            applet = applet.replace('_', ' ')
            applet = applet.title()
            applet = applet.replace(' ', '')
            applet += 'Controller'
            return getattr(module, applet, None)
        except ModuleNotFoundError as e:
            raise e


class AppletManagerFrameView(BaseFrameView):

    def __init__(self, controller):
        super(AppletManagerFrameView, self).__init__(controller)
        self._paned_window = AppletManagerPanedWindow(self, controller)

    @property
    def applet_display_frame(self):
        return self._paned_window.applet_display_frame


class AppletManagerController(BaseController):

    _model_cls = AppletManagerModel
    _view_cls = AppletManagerFrameView

    def start_applet(self, applet):
        self.stop_applet()
        try:
            self._model.applet = self._model.get_applet(applet)
        except Exception as e:
            print(e)
        else:
            self._model.applet = self._model.applet(self._view.applet_display_frame, instance=self._model.instance)
            self._model.applet.start()

    def stop_applet(self):
        try:
            self._model.applet = self._model.applet.stop()
        except Exception as e:
            print(e)


class NavigationTreeView(Treeview):
    def __init__(self, master, controller):
        super(NavigationTreeView, self).__init__(master)
        self._controller = controller
        self._build()

    def _build(self):

        # Scrollbar initialization
        scrollbar = Scrollbar(self, orient=VERTICAL, command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # TreeView configuration
        self.config(yscrollcommand=scrollbar.set)
        self.config(show='tree')
        self.column('#0', width=200)

        self.insert('', END, iid='service_control', text='Services')
        self.insert('', END, iid='server_info', text='System')
        self.insert('', END, iid='user_management', text='Users')
        self.insert('', END, iid='backing_up_planning', text='Back-ups')

        # Set initial focus
        item = self.get_children()[0]
        self.focus(item)

        # Bindings
        self.bind('<<TreeviewSelect>>', self._start_applet)

        # Pack
        self.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)

    def _start_applet(self, event):
        self._controller.start_applet(self.focus())


class NavigationTreeFrame(Frame):
    def __init__(self, master, controller):
        super(NavigationTreeFrame, self).__init__(master)
        self._navigation_tree_view = NavigationTreeView(self, controller)


class AppletDisplayFrame(Frame):
    def __init__(self, master):
        super(AppletDisplayFrame, self).__init__(master)
        self.pack()


class AppletManagerPanedWindow(PanedWindow):
    def __init__(self, master, controller):
        super(AppletManagerPanedWindow, self).__init__(master)
        self._navigation_tree_frame = NavigationTreeFrame(self, controller)
        self._applet_display_frame = AppletDisplayFrame(self)
        self.add(self._navigation_tree_frame, minsize=200)
        self.add(self._applet_display_frame)
        self.pack(fill='both', expand=True)

    @property
    def applet_display_frame(self):
        return self._applet_display_frame