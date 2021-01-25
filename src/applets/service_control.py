from threading import Thread

from applets.applet_base import BaseApplet, PADX, PADY, BaseView, Refreshable

from tkinter import Frame, LEFT, END, BOTH, W, X, RIGHT, Y, VERTICAL, StringVar, DISABLED, NORMAL
from tkinter.ttk import Treeview, Button, Scrollbar, Label

from client.Client import Client


class ServiceControlApplet(BaseApplet):

    def __init__(self, model, root):
        super(ServiceControlApplet, self).__init__(model, root)
        self._model.subscribe(Client.EVENT_SERVICE_STATUS_CHANGED, self._on_service_update)
        # FIXME: service_manager must be a model.
        self.service_manager.initialize()
        self._view = ServiceControlView(root, self)

    @property
    def service_manager(self):
        return self._model.service_manager

    def _on_service_update(self, service, config):
        # Update model
        obj = self.service_manager.update(service, config)
        # Update view
        Thread(target=self._view.refresh, args=(obj, )).start()

    def start_service(self):
        service = self.service_manager.services[self._view.item]
        try:
            if service.is_running:
                Thread(target=service.stop).start()
            else:
                Thread(target=service.start).start()
        except Exception as e:
            print(e)

    def enable_service(self):
        service = self.service_manager.services[self._view.item]
        try:
            if service.is_active:
                Thread(target=service.disable).start()
            else:
                Thread(target=service.enable).start()
        except Exception as e:
            print(e)

    def rerun_service(self):
        return NotImplemented

    def refresh_view(self, event):
        service = self.service_manager.services[self._view.item]
        self._view.refresh(service)


class ServiceControlView(BaseView):
    def __init__(self, master, controller):
        super(ServiceControlView, self).__init__(master, controller)
        self._control_panel_frame = ServiceControlPanelFrame(self, controller)
        self._service_tree_frame = ServiceTreeFrame(self, controller)

    def refresh(self, service):
        self._service_tree_frame.refresh(service)
        if service.unit == self.item:
            self._control_panel_frame.refresh(service)

    @property
    def item(self):
        return self._service_tree_frame.get_item()


class ServiceTreeFrame(Frame, Refreshable):
    def __init__(self, master, controller):
        super(ServiceTreeFrame, self).__init__(master)
        self._service_tree_view = ServiceTreeView(self, controller)
        self.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)

    def refresh(self, service):
        self._service_tree_view.refresh(service)

    def get_item(self):
        return self._service_tree_view.get_item()


class ServiceDetailsFrame(Frame, Refreshable):

    _details = ['unit', 'load', 'active', 'sub', 'description']

    def __init__(self, master, controller):
        super(ServiceDetailsFrame, self).__init__(master)
        self._vars = {}

        for i in range(len(self._details)):
            text = self._details[i]
            text = text.title()
            text += ':'
            var = StringVar()
            Label(self, text=text).grid(column=0, row=i, sticky=W)
            Label(self, textvariable=var).grid(column=1, row=i, sticky=W)
            self._vars[self._details[i]] = var

        self.pack(fill=BOTH, padx=PADX, pady=PADY)

    def refresh(self, service):
        for var in self._vars:
            self._vars[var].set(getattr(service, var, ''))


class ServiceControlsFrame(Frame, Refreshable):
    def __init__(self, master, controller):
        super(ServiceControlsFrame, self).__init__(master)
        self._start_button = StartButton(self, controller)
        self._rerun_button = RerunButton(self, controller)
        self._enable_button = EnableButton(self, controller)
        self.pack(fill=BOTH, padx=PADX, pady=PADY)

    def refresh(self, service):
        self._start_button.refresh(service.is_running)
        self._rerun_button.refresh(service.is_running)
        self._enable_button.refresh(service.is_active)


class ServiceControlPanelFrame(Frame, Refreshable):
    def __init__(self, master, controller):
        super(ServiceControlPanelFrame, self).__init__(master)
        self._service_details_frame = ServiceDetailsFrame(self, controller)
        self._service_controls_frame = ServiceControlsFrame(self, controller)
        self.pack(anchor=W, padx=PADX, pady=PADY, fill=X)

    def refresh(self, service):
        self._service_details_frame.refresh(service)
        self._service_controls_frame.refresh(service)


class ServiceTreeView(Treeview, Refreshable):

    _iid = 'unit'
    _headings = ['load', 'active', 'sub', 'description']

    def __init__(self, master, controller):
        super(ServiceTreeView, self).__init__(master)
        self._controller = controller
        self._build()

    def get_item(self):
        return self.item(self.focus(), 'text')

    def refresh(self, service):
        self.item(getattr(service, self._iid), values=[getattr(service, col, None) for col in self._headings])

    def _build(self):

        # Scrollbar initialization
        scrollbar = Scrollbar(self, orient=VERTICAL, command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # TreeView configuration
        self.config(columns=self._headings, yscrollcommand=scrollbar.set, selectmode='browse')

        # Tree initialization
        self.heading('#0', text=self._iid.title())
        self.column('#0', width=150, stretch=False)

        # Columns initialization
        for column in self._headings:
            self.heading(column, text=column.title())
            self.column(column, width=100, stretch=False)

        self.column(self._headings[-1], stretch=True)

        # Items initialization
        for key, service in self._controller.service_manager.services.items():
            try:
                self.insert('', END, iid=key,
                            text=key,
                            values=[getattr(service, col, None) for col in self._headings])
            except Exception as e:
                print(e)

        # Set initial focus
        self.focus(self.get_children()[0])

        # Bindings
        self.bind('<<TreeviewSelect>>', self._controller.refresh_view)

        # Register
        self.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)


class StartButton(Button, Refreshable):

    def __init__(self, master, controller):
        super(StartButton, self).__init__(master)
        self.config(text='Start', state=DISABLED, command=controller.start_service)
        self.pack(side=LEFT, padx=PADX, pady=PADY)

    def refresh(self, switched):
        if switched:
            self.config(state=NORMAL, text='Stop')
        else:
            self.config(state=NORMAL, text='Start')


class RerunButton(Button, Refreshable):
    def __init__(self, master, controller):
        super(RerunButton, self).__init__(master)
        self.config(text='Rerun', state=DISABLED, command=controller.rerun_service)
        self.pack(side=LEFT, padx=PADX, pady=PADY)

    def refresh(self, switched):
        if switched:
            self.config(state=NORMAL)
        else:
            self.config(state=DISABLED)


class EnableButton(Button, Refreshable):
    def __init__(self, master, controller):
        super(EnableButton, self).__init__(master)
        self.config(text='Enable', state=DISABLED, command=controller.enable_service)
        self.pack(side=LEFT, padx=PADX, pady=PADY)

    def refresh(self, switched):
        if switched:
            self.config(state=NORMAL, text='Disable')
        else:
            self.config(state=NORMAL, text='Enable')
