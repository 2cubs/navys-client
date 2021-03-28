from tkinter import Frame, BOTH, X, LEFT, Scrollbar, VERTICAL, RIGHT, Y, END, filedialog
from tkinter.ttk import Treeview, Button, Separator

from navys_client.applets import PADX, PADY
from navys_client.applets.base import BaseController, BaseToplevelView
from navys_client.applets.database import DB
from navys_client.widgets import LabeledEntry, CustomToplevel


class Connection:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ConnectionManagerModel:

    _db = DB()
    _table = 'connections'
    pk = _db.get_primary_key(_table)
    columns = _db.get_columns(_table)

    def __init__(self):
        self.connections = self.refresh()

    def refresh(self):
        connections = {}
        try:
            for entry in self._db.select(self._table):
                connections[entry[self.pk]] = Connection(**entry)
        except Exception as e:
            print(e)
        else:
            return connections

    def insert(self, **kwargs):
        try:
            rowid = self._db.insert(self._table, **kwargs)
        except Exception as e:
            print(e)
        else:
            self.connections = self.refresh()
            return rowid

    def delete(self, **kwargs):
        try:
            self._db.delete(self._table, **kwargs)
        except Exception as e:
            print(e)
        else:
            self.connections = self.refresh()

    def update(self, pk, **kwargs):
        try:
            self._db.update(self._table, pk, **kwargs)
        except Exception as e:
            print(e)
        else:
            self.connections = self.refresh()


class ConnectionMaintenanceView(CustomToplevel):

    _is_resizable = False

    def __init__(self, root, controller):
        self._controller = controller
        super(ConnectionMaintenanceView, self).__init__(root)

        # Entries Frame
        frame = Frame(self)
        self._entries = {'description': LabeledEntry(frame, label='Description:', hint='Short description.'),
                         'host': LabeledEntry(frame, label='Host:', hint='URL or IP address.'),
                         'host_name': LabeledEntry(frame, label='Host name:', hint='Server host name.'),
                         'socket': LabeledEntry(frame, label='Port:', hint='Port number.'),
                         'path': LabeledEntry(frame, label='Path:', hint='Path to SSL certificates.',
                                              search_help=self._help_path)}

        for key, widget in self._entries.items():
            widget.columnconfigure(0, minsize=70)
            widget.entry.config(width=50)
            widget.pack(anchor='nw')

        self._entries['socket'].entry.config(width=5)
        self._entries['description'].register(self._trace_description)
        self._entries['socket'].register(self._trace_socket)

        frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Controls Frame
        self._controls = Frame(self, bg='light gray')
        self._controls.pack(fill=X)

    def _trace_description(self, *args):
        if len(self._entries['description'].value) > 20:
            self._entries['description'].value = self._entries['description'].value[:20]

    def _trace_socket(self, *args):
        try:
            if not self._entries['socket'].value[-1].isnumeric():
                self._entries['socket'].value = self._entries['socket'].value[:-1]
        except Exception as e:
            print(e)
        if len(self._entries['socket'].value) > 5:
            self._entries['socket'].value = self._entries['socket'].value[:5]

    def _help_path(self):
        directory = filedialog.askdirectory()
        self._entries['path'].value = directory


class NewConnectionView(ConnectionMaintenanceView):

    _title = 'New Connection'

    def __init__(self, root, controller):
        super(NewConnectionView, self).__init__(root, controller)
        Button(self._controls, text='Create', command=self._create).pack(side=RIGHT, padx=PADX, pady=PADY)

    def _create(self):
        try:
            self._controller.insert(**{key: entry.value for key, entry in self._entries.items()})
        except Exception as e:
            print(e)


class ChangeConnectionView(ConnectionMaintenanceView):

    _title = 'Change Connection'

    def __init__(self, root, controller):
        super(ChangeConnectionView, self).__init__(root, controller)
        Button(self._controls, text='Change', command=self._change).pack(side=RIGHT, padx=PADX, pady=PADY)

    def refresh(self):
        try:
            for key, value in self._controller.focus.items():
                self._entries[key].value = value
        except Exception as e:
            print(e)

    def _change(self):
        try:
            self._controller.update(**{key: entry.value for key, entry in self._entries.items()})
        except Exception as e:
            print(e)


class ConnectionManagerView(CustomToplevel):

    _title = 'Connections'
    _width = 450
    _height = 350

    def __init__(self, root, controller):
        super(ConnectionManagerView, self).__init__(root)
        self._controller = controller
        columns = ['iid', 'description', 'host', 'host_name', 'socket', 'path']

        # Toolbar
        toolbar = Frame(self)
        Button(toolbar, text='Connect', command=self._connect).pack(side=LEFT, padx=PADX, pady=PADY)
        Separator(toolbar, orient='vertical').pack(side=LEFT, padx=PADX, pady=PADY, fill=Y)
        Button(toolbar, text='Create', command=self._create).pack(side=LEFT, padx=PADX, pady=PADY)
        Button(toolbar, text='Change', command=self._change).pack(side=LEFT, padx=PADX, pady=PADY)
        Button(toolbar, text='Delete', command=self._delete).pack(side=LEFT, padx=PADX, pady=PADY)
        toolbar.pack(fill=X, padx=PADX, pady=PADY)

        # TreeView
        frame = Frame(self)
        self._tree = Treeview(frame, columns=columns[1:], selectmode='browse', show='headings')
        scrollbar = Scrollbar(self._tree, orient=VERTICAL, command=self._tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self._tree.config(yscrollcommand=scrollbar.set)

        for column in self._tree['columns']:
            self._tree.heading(column, text=column.replace('_', ' ').title())
            self._tree.column(column, width=100, stretch=False)
        self._tree.column(self._tree['columns'][-1], stretch=True)
        self._tree.heading('#0', text=columns[0])
        self.refresh()

        try:
            self._tree.focus(self._tree.get_children()[0])
        except Exception as e:
            print(e)

        self._tree.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)
        frame.pack(expand=True, fill=BOTH, padx=PADX, pady=PADY)

    @property
    def focus(self):
        try:
            return int(self._tree.focus())
        except Exception as e:
            print(e)

    def refresh(self):
        for row in self._tree.get_children():
            self._tree.delete(row)

        try:
            for key, value in self._controller.connections.items():
                values = [getattr(value, col, None) for col in self._tree['columns']]
                self._tree.insert('', END, iid=key, text=key, values=values)
        except Exception as e:
            print(e)

    def _connect(self):
        try:
            self._controller.connect()
        except Exception as e:
            print(e)

    def _create(self):
        try:
            self._controller.create_connection()
        except Exception as e:
            print(e)

    def _change(self):
        try:
            self._controller.change_connection()
        except Exception as e:
            print(e)

    def _delete(self):
        try:
            self._controller.delete_connection()
        except Exception as e:
            print(e)


class ConnectionManagerController:

    def __init__(self, root):
        self._model = ConnectionManagerModel()
        self._view = ConnectionManagerView(root=root, controller=self)

    @property
    def focus(self):
        return vars(self._model.connections[self._view.focus])

    @property
    # TODO: refactor this - shouldn't be here
    def table(self):
        pk = self._model.pk
        cols = [col for col in self._model.columns if col != pk]
        return pk, cols

    @property
    def connections(self):
        return self._model.connections

    def connect(self):
        self._parent.connect(vars(self._model.connections[self._view.focus]))
        self.stop()

    def create_connection(self):
        self._view.modal.open(view=NewConnectionView)

    def change_connection(self):
        self._view.modal.open(view=ChangeConnectionView)

    def delete_connection(self):
        self.delete(iid=self._view.focus)

    def insert(self, **kwargs):
        self._model.insert(**kwargs)
        self._view.modal.close()
        self._view.refresh()

    def delete(self, **kwargs):
        self._model.delete(**kwargs)
        self._view.refresh()

    def update(self, **kwargs):
        self._model.update(self._view.focus, **kwargs)
        self._view.modal.close()
        self._view.refresh()

    def start(self):
        self._view.pack(fill='both', expand=True)

    def stop(self):
        self._view.pack_forget()


