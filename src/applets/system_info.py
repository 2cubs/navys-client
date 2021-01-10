from tkinter.ttk import Treeview, Scrollbar

from applets.applet_base import AppletBase, PADX, PADY
from tkinter import Frame, VERTICAL, RIGHT, Y, BOTH, END


class SystemInfoApplet(AppletBase):
    def __init__(self, model, root):
        super(SystemInfoApplet, self).__init__(model, root)
        self._view = SystemInfoFrame(root, self)


class SystemInfoTreeView(Treeview):

    _columns = ['item', 'value']
    _items = {'host_name': 'Host name',
              'os_name': 'OS name',
              'kernel': 'Kernel',
              'ram': 'RAM',
              'graphics_card': 'Graphics card',
              'hard_drive': 'Hard drive'}

    def __init__(self, master, controller):
        super(SystemInfoTreeView, self).__init__(master)
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

        for attrib in self._controller.model.system.__dict__:
            self.insert('', END, text='attrib', values=[self._items.get(attrib, attrib),
                                                        getattr(self._controller.model.system, attrib)])


class SystemInfoFrame(Frame):
    def __init__(self, master, controller):
        super(SystemInfoFrame, self).__init__(master)
        self.sysinfo_tree_view = SystemInfoTreeView(self, controller)
        self.sysinfo_tree_view.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)