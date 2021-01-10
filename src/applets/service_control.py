from applets.applet_base import AppletBase, PADX, PADY

from tkinter import Frame, LEFT, END, BOTH, W, X, RIGHT, Y, VERTICAL
from tkinter.ttk import Treeview, Button, Scrollbar


class ServiceControlApplet(AppletBase):

    def __init__(self, model, root):
        super(ServiceControlApplet, self).__init__(model, root)
        self._view = ServiceControlFrame(root, self)
        self._controls = self._view.control_panel_frame
        self._tree = self._view.service_tree_frame.service_tree_view

    def update_controls(self, event):
        item = self._tree.get_item()
        service = self.model.get_service_by_unit(item['values'][0])
        if service.sub == 'running':
            self._controls.start_stop_button['state'] = 'enabled'
            self._controls.start_stop_button['text'] = 'Stop'
            self._controls.rerun_button['state'] = 'enabled'
        elif service.sub == 'stopped':
            self._controls.start_stop_button['state'] = 'enabled'
            self._controls.start_stop_button['text'] = 'Start'
            self._controls.rerun_button['state'] = 'disabled'

        if service.active == 'active':
            self._controls.enable_disable_button['state'] = 'enabled'
            self._controls.enable_disable_button['text'] = 'Disable'
        elif service.active == 'inactive':
            self._controls.enable_disable_button['state'] = 'enabled'
            self._controls.enable_disable_button['text'] = 'Enable'

    def start_stop_service(self):
        item = self._tree.get_item()
        try:
            service = self.model.get_service_by_unit(item['values'][0])
            if service.sub == 'running':
                service.stop()
            elif service.sub == 'stopped':
                service.start()
        except Exception as e:
            print(e)
        else:
            self._tree.set_item(service)
            self.update_controls(self._tree.get_item())

    def enable_disable_service(self):
        item = self._tree.get_item()
        try:
            service = self.model.get_service_by_unit(item['values'][0])
            if service.active == 'active':
                service.disable()
            elif service.active == 'inactive':
                service.enable()
        except Exception as e:
            print(e)
        else:
            self._tree.set_item(service)
            self.update_controls(self._tree.get_item())

    def rerun_service(self):
        return NotImplementedError


class ServiceControlFrame(Frame):
    def __init__(self, master, controller):
        super(ServiceControlFrame, self).__init__(master)
        self.control_panel_frame = ServiceControlPanelFrame(self, controller)
        self.control_panel_frame.pack(anchor=W, padx=PADX, pady=PADY, fill=X)
        self.service_tree_frame = ServiceTreeFrame(self, controller)
        self.service_tree_frame.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)


class ServiceTreeFrame(Frame):
    def __init__(self, master, controller):
        super(ServiceTreeFrame, self).__init__(master)
        self.service_tree_view = ServiceTreeView(self, controller)
        self.service_tree_view.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)


class ServiceControlPanelFrame(Frame):
    def __init__(self, master, controller):
        super(ServiceControlPanelFrame, self).__init__(master)
        self.start_stop_button = StartStopButton(self, controller)
        self.start_stop_button.pack(side=LEFT, padx=PADX, pady=PADY)
        self.rerun_button = RerunButton(self, controller)
        self.rerun_button.pack(side=LEFT, padx=PADX, pady=PADY)
        self.enable_disable_button = EnableDisableButton(self, controller)
        self.enable_disable_button.pack(side=LEFT, padx=PADX, pady=PADY)


class ServiceTreeView(Treeview):

    # TODO: disable multiple selection

    _columns = ('unit', 'load', 'active', 'sub', 'description')

    def __init__(self, master, controller):
        super(ServiceTreeView, self).__init__(master)
        self._controller = controller
        self._build()

    def get_item(self):
        return self.item(self.focus())

    def set_item(self, item):
        self.item(self.focus(), values=[getattr(item, col, None) for col in self._columns])

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

        for service in self._controller.model.services:
            self.insert('', END, values=[getattr(service, col, None) for col in self._columns])

        # Set initial focus
        item = self.get_children()[0]
        self.focus(item)

        # Bindings
        self.bind('<<TreeviewSelect>>', self._controller.update_controls)


class StartStopButton(Button):

    def __init__(self, master, controller):
        super(StartStopButton, self).__init__(master)
        self._controller = controller
        self.config(text='Start', state='disabled', command=self._controller.start_stop_service)


class RerunButton(Button):
    def __init__(self, master, controller):
        super(RerunButton, self).__init__(master)
        self._controller = controller
        self.config(text='Rerun', state='disabled', command=self._controller.rerun_service)


class EnableDisableButton(Button):
    def __init__(self, master, controller):
        super(EnableDisableButton, self).__init__(master)
        self._controller = controller
        self.config(text='Enable', state='disabled', command=self._controller.enable_disable_service)