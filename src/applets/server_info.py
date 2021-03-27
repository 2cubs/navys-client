from datetime import datetime
from tkinter import VERTICAL, RIGHT, Y, END, BOTH, Frame
from tkinter.ttk import Treeview, Scrollbar

from pydantic import validator
from pydantic.dataclasses import dataclass

from applets import PADX, PADY


@dataclass
class UName:
    system_name: str
    node_name: str
    release: str
    version: str
    machine: str
    processor: str


@dataclass
class ServerInfo:
    uname: UName
    current_time: datetime

    @validator('uname', pre=True)
    def set_uname(cls, value):
        return dict(zip(['system_name', 'node_name', 'release', 'version', 'machine', 'processor'], value))


class ServerInfoView(Frame):

    def __init__(self, root, controller):
        super(ServerInfoView, self).__init__(root)
        self._controller = controller

        # Tree initialization
        tree = Treeview(self)
        columns = ['item', 'value']

        # Scrollbar initialization
        scrollbar = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # TreeView configuration
        tree.config(columns=columns, show='headings', yscrollcommand=scrollbar.set)

        # Items initialization
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, width=100, stretch=False)

        tree.column(columns[-1], stretch=True)

        try:
            for key, value in vars(self._controller.attributes).items():
                if not key.startswith('_'):
                    key = key.replace('_', ' ').capitalize()
                    tree.insert('', END, text='attrib', values=[key, value])
        except Exception as e:
            print(e)

        # Packing
        tree.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)


class ServerInfoController:

    def __init__(self, root, instance):
        self._model = ServerInfo(**instance.remote.server_info())
        self._view = ServerInfoView(root=root, controller=self)

    @property
    def attributes(self):
        return self._model.uname

    def start(self):
        self._view.pack(fill='both', expand=True)

    def stop(self):
        self._view.pack_forget()
