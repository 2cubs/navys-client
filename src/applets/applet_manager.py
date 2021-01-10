from importlib import import_module
from tkinter import Frame, LEFT, Y, W, BOTH, RIGHT, VERTICAL, END
from tkinter.ttk import Treeview, Scrollbar

from applets.applet_base import AppletBase, PADX, PADY


class AppletManagerApplet(AppletBase):

    def __init__(self, model, root):
        super(AppletManagerApplet, self).__init__(model, root)
        self._model = model
        self._view = AppletManagerFrame(root, self)
        self._tree = self._view.navigation_tree_frame.navigation_tree_view
        self._frame = self._view.applet_display_frame
        self._applet = None

    def _init_applet(self, package):
        try:
            applet = package.replace('_', ' ')
            applet = applet.title()
            applet = applet.replace(' ', '')
            applet += 'Applet'
            module = import_module('.'.join(['applets', package]))
            return getattr(module, applet, None)(self._model, self._frame)
        except ModuleNotFoundError as e:
            raise e

    def run_applet(self, event):
        try:
            self._applet.close()
            self._applet = None
        except Exception as e:
            print(e)

        try:
            self._applet = self._init_applet(self._tree.focus())
            self._applet.run()
        except ModuleNotFoundError as e:
            print(e)


class NavigationTreeView(Treeview):
    def __init__(self, master, controller):
        super(NavigationTreeView, self).__init__(master)
        self._controller = controller
        self._master = master
        self._build()

    def _build(self):

        # Scrollbar initialization
        # TODO: fix scroll bar
        scrollbar = Scrollbar(self.master, orient=VERTICAL, command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # TreeView configuration
        self.config(yscrollcommand=scrollbar.set)
        self.config(show='tree')
        self.column('#0', width=200)

        self.insert('', END, iid='service_control', text='Services')
        self.insert('', END, iid='system_info', text='System')
        self.insert('', END, iid='user_management', text='Users')
        self.insert('', END, iid='backing_up_planning', text='Back-ups')

        # Set initial focus
        item = self.get_children()[0]
        self.focus(item)

        # Bindings
        self.bind('<<TreeviewSelect>>', self._controller.run_applet)


class NavigationTreeFrame(Frame):
    def __init__(self, master, controller):
        super(NavigationTreeFrame, self).__init__(master, width=200)
        self.navigation_tree_view = NavigationTreeView(self, controller)
        self.navigation_tree_view.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)


class AppletDisplayFrame(Frame):
    def __init__(self, master, controller):
        super(AppletDisplayFrame, self).__init__(master)


class AppletManagerFrame(Frame):
    def __init__(self, master, controller):
        super(AppletManagerFrame, self).__init__(master)
        self.navigation_tree_frame = NavigationTreeFrame(self, controller)
        self.navigation_tree_frame.pack(padx=PADX, pady=PADY, fill=Y, anchor=W, side=LEFT)
        self.applet_display_frame = AppletDisplayFrame(self, controller)
        self.applet_display_frame.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)