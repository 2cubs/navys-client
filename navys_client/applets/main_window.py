from tkinter import Label, Frame

from navys_client.applets.base import BaseController, BaseFrameView
from navys_client.applets.connection_manager import ConnectionManagerController
from navys_client.applets.tab_manager import TabController


class MainWindowView(BaseFrameView):

    def __build__(self):

        # Mainframe
        self.mainframe = Frame(self)
        shortcut = Label(self.mainframe,  text='Connect to server...', font=('', 12), fg='grey')
        shortcut.bind('<Button-1>', self._invoke_connection_manager)
        shortcut.place(relx=1/2, rely=1/2, anchor='center')
        self.mainframe.pack(expand=True, fill='both')

        # Status bar
        statusbar = Frame(self, bg='light grey')
        Label(statusbar, text='StatusBar').pack()
        statusbar.pack(fill='x')

    def _invoke_connection_manager(self, event):
        self._controller.invoke_connection_manager()


class MainWindowController(BaseController):

    _view_cls = MainWindowView

    def __init__(self, parent, **kwargs):
        super(MainWindowController, self).__init__(parent, **kwargs)
        self.tab_controller = TabController(root=self._view.mainframe)

    def invoke_connection_manager(self):
        ConnectionManagerController(self._parent)

    def add_tab(self, instance, text):
        self.tab_controller.add_tab(instance, text)


