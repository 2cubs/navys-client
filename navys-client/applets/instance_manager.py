from importlib import import_module
from tkinter import PanedWindow, Frame, Scrollbar, VERTICAL, RIGHT, Y, BOTH, END
from tkinter.ttk import Treeview

from applets import PADX, PADY


class Instance:

    def __init__(self, instance):
        self._applet = None
        self._instance = instance

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

    def start_applet(self, applet, controller):
        try:
            self._applet = applet(controller, instance=self._instance)
            self._applet.start()
        except Exception as e:
            print(e)

    def stop_applet(self):
        try:
            self._applet = self._applet.stop()
        except Exception as e:
            print(e)


class InstanceView(PanedWindow):

    def __init__(self, controller, root, **kwargs):
        self._controller = controller
        super(InstanceView, self).__init__(root, **kwargs)

        # Panes
        navi_frame = Frame(self)
        self._applet_frame = Frame(self)

        # Tree
        self._tree = Treeview(navi_frame)

        # Scrollbar initialization
        scrollbar = Scrollbar(self, orient=VERTICAL, command=self._tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Tree configuration
        self._tree.config(yscrollcommand=scrollbar.set)
        self._tree.config(show='tree')
        self._tree.column('#0', width=200)

        # Insert items
        self._tree.insert('', END, iid='service_control', text='Services')
        self._tree.insert('', END, iid='server_info', text='System')
        self._tree.insert('', END, iid='user_management', text='Users')
        self._tree.insert('', END, iid='backing_up_planning', text='Back-ups')

        # Set initial focus
        item = self._tree.get_children()[0]
        self._tree.focus(item)

        # Bindings
        self._tree.bind('<<TreeviewSelect>>', self._start_applet)

        # Pack tree
        self._tree.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)

        # Add frames to paned window
        self.add(navi_frame, minsize=200)
        self.add(self._applet_frame)

        # Packing
        self.pack(fill='both', expand=True)

    def _start_applet(self, event=None):
        self._controller.start_applet(self._tree.focus())

    @property
    def applet_frame(self):
        return self._applet_frame


class InstanceController:

    _model_cls = Instance
    _view_cls = InstanceView

    def __init__(self, root, **kwargs):
        self._model = self._model_cls(**kwargs) if self._model_cls else None
        self._view = self._view_cls(controller=self, root=root)

    def start_applet(self, applet):
        self.stop_applet()
        try:
            applet = self._model.get_applet(applet)
        except Exception as e:
            print(e)
        else:
            self._model.start_applet(applet, self._view.applet_frame)

    def stop_applet(self):
        self._model.stop_applet()

    @property
    def view(self):
        return self._view

    # TODO: Refactor this!
    @property
    def root(self):
        return self.view.applet_frame