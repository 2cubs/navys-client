from time import sleep

from applets.applet_base import AppletBase, PADX, PADY

from tkinter import Frame, LEFT, END, BOTH, W, X, RIGHT, Y, VERTICAL, StringVar, DISABLED, NORMAL
from tkinter.ttk import Treeview, Button, Scrollbar, Label


class ServiceControlApplet(AppletBase):

    def __init__(self, model, root):
        super(ServiceControlApplet, self).__init__(model, root)
        self.model = model.service_manager
        self.model.update()
        self._view = ServiceControlFrame(root, self)
        self._controls = self._view.control_panel_frame.unit_controls_frame
        self._tree = self._view.service_tree_frame.service_tree_view
        self._attribs = self._view.control_panel_frame.service_details_frame.attribs

    def update_details(self, event):
        item = self._tree.get_item()
        service = self.model.services[item['text']]
        self._update_attribs(service)
        self._update_controls(service)

    def _update_attribs(self, service):
        for key in self._attribs:
            self._attribs[key].set(getattr(service, key, ''))

    def _update_controls(self, service):
        if service.is_running:
            self._controls.start_stop_button['state'] = NORMAL
            self._controls.start_stop_button['text'] = 'Stop'
            self._controls.rerun_button['state'] = NORMAL
        else:
            self._controls.start_stop_button['state'] = NORMAL
            self._controls.start_stop_button['text'] = 'Start'
            self._controls.rerun_button['state'] = DISABLED

        if service.is_active:
            self._controls.enable_disable_button['state'] = NORMAL
            self._controls.enable_disable_button['text'] = 'Disable'
        else:
            self._controls.enable_disable_button['state'] = NORMAL
            self._controls.enable_disable_button['text'] = 'Enable'

    def start_stop_service(self):
        item = self._tree.get_item()
        try:
            service = self.model.services[item['text']]
            if service.is_running:
                service.stop()
            else:
                service.start()
        except Exception as e:
            print(e)
        else:
            self._tree.set_item(service)
            self.update_details(item)

    def enable_disable_service(self):
        item = self._tree.get_item()
        try:
            service = self.model.services[item['text']]
            if service.active:
                service.disable()
            else:
                service.enable()
        except Exception as e:
            print(e)
        else:
            self._tree.set_item(service)
            self.update_details(item)

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


class ServiceDetailsFrame(Frame):

    _attribs = ['unit', 'load', 'active', 'sub', 'description']

    def __init__(self, master, controller):
        super(ServiceDetailsFrame, self).__init__(master)
        self.attribs = {}

        for i in range(len(self._attribs)):
            text = self._attribs[i]
            text = text.title()
            text += ':'
            var = StringVar()
            Label(self, text=text).grid(column=0, row=i, sticky=W)
            Label(self, textvariable=var).grid(column=1, row=i, sticky=W)
            self.attribs[self._attribs[i]] = var


class ServiceControlsFrame(Frame):
    def __init__(self, master, controller):
        super(ServiceControlsFrame, self).__init__(master)
        self.start_stop_button = StartStopButton(self, controller)
        self.start_stop_button.pack(side=LEFT, padx=PADX, pady=PADY)
        self.rerun_button = RerunButton(self, controller)
        self.rerun_button.pack(side=LEFT, padx=PADX, pady=PADY)
        self.enable_disable_button = EnableDisableButton(self, controller)
        self.enable_disable_button.pack(side=LEFT, padx=PADX, pady=PADY)


class ServiceControlPanelFrame(Frame):
    def __init__(self, master, controller):
        super(ServiceControlPanelFrame, self).__init__(master)
        self.service_details_frame = ServiceDetailsFrame(self, controller)
        self.service_details_frame.pack(fill=BOTH, padx=PADX, pady=PADY)
        self.unit_controls_frame = ServiceControlsFrame(self, controller)
        self.unit_controls_frame.pack(fill=BOTH, padx=PADX, pady=PADY)


class ServiceTreeView(Treeview):

    _tree = 'unit'
    _columns = ['load', 'active', 'sub', 'description']

    def __init__(self, master, controller):
        super(ServiceTreeView, self).__init__(master)
        self._controller = controller
        self._build()

    def get_item(self):
        return self.item(self.focus())

    def set_item(self, obj):
        self.item(self.focus(), values=[getattr(obj, col, None) for col in self._columns])

    def _build(self):

        # Scrollbar initialization
        scrollbar = Scrollbar(self, orient=VERTICAL, command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # TreeView configuration
        self.config(columns=self._columns, yscrollcommand=scrollbar.set, selectmode='browse')

        # Tree initialization
        self.heading('#0', text=self._tree.title())
        self.column('#0', width=150, stretch=False)

        # Columns initialization
        for column in self._columns:
            self.heading(column, text=column.title())
            self.column(column, width=100, stretch=False)

        self.column(self._columns[-1], stretch=True)

        # Items initialization
        for key, service in self._controller.model.services.items():
            try:
                self.insert('', END, iid=key,
                            text=key,
                            values=[getattr(service, col, None) for col in self._columns])
            except Exception as e:
                print(e)

        # Set initial focus
        self.focus(self.get_children()[0])

        # Bindings
        self.bind('<<TreeviewSelect>>', self._controller.update_details)


class StartStopButton(Button):

    def __init__(self, master, controller):
        super(StartStopButton, self).__init__(master)
        self.config(text='Start', state=DISABLED, command=controller.start_stop_service)


class RerunButton(Button):
    def __init__(self, master, controller):
        super(RerunButton, self).__init__(master)
        self.config(text='Rerun', state=DISABLED, command=controller.rerun_service)


class EnableDisableButton(Button):
    def __init__(self, master, controller):
        super(EnableDisableButton, self).__init__(master)
        self.config(text='Enable', state=DISABLED, command=controller.enable_disable_service)