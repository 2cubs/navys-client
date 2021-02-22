from tkinter import VERTICAL, RIGHT, Y, END, BOTH
from tkinter.ttk import Treeview, Scrollbar

from applets import PADX, PADY
from applets.base import BaseFrameView, BaseController


class ServerInfoModel:

    def __init__(self, instance):
        self._instance = instance
        self._info = self._instance.remote.server_info()['uname']

    @property
    def info(self):
        keys = ['sysname', 'nodename', 'release', 'version', 'machine']
        return dict(zip(keys, self._info))


class ServerInfoFrameView(BaseFrameView):

    def __init__(self, controller):
        super(ServerInfoFrameView, self).__init__(controller)
        self._system_info_tree_view = ServerInfoTreeView(self, controller)


class ServerInfoController(BaseController):

    _model_cls = ServerInfoModel
    _view_cls = ServerInfoFrameView

    @property
    def attributes(self):
        return self._model.info


class ServerInfoTreeView(Treeview):

    _columns = ['item', 'value']
    _rows = {'sysname': 'System name',
             'nodename': 'Node name',
             'release': 'Release',
             'version': 'Version',
             'machine': 'Machine'}

    def __init__(self, master, controller):
        super(ServerInfoTreeView, self).__init__(master)
        self._controller = controller
        self._build()

    def _build(self):
        # Scrollbar initialization
        scrollbar = Scrollbar(self, orient=VERTICAL, command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # TreeView configuration
        self.config(columns=self._columns, show='headings', yscrollcommand=scrollbar.set)

        # Items initialization
        for col in self._columns:
            self.heading(col, text=col.title())
            self.column(col, width=100, stretch=False)

        self.column(self._columns[-1], stretch=True)

        for key, value in self._rows.items():
            self.insert('', END, text='attrib', values=[value, self._controller.attributes.get(key, '')])

        self.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)