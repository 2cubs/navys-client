from pydantic import Field, BaseModel
from threading import Thread

from applets import PADX, PADY

from tkinter import Frame, LEFT, END, BOTH, W, X, RIGHT, Y, VERTICAL, StringVar, DISABLED
from tkinter.ttk import Treeview, Button, Scrollbar, Label

from widgets.switchable_button import SwitchableButton


class Service(BaseModel):
    unit: str = Field(alias='name')
    type: str
    started: bool
    enabled: bool
    description: str
    load: str = 'loaded'

    @property
    def active(self):
        if self.enabled:
            return 'active'
        return 'inactive'

    @property
    def sub(self):
        if self.started:
            return 'running'
        return 'stopped'


class ServicesList:
    def __init__(self, instance):
        self._instance = instance
        self.services = {key: Service(**value)
                         for key, value in instance.remote.service_status(instance.remote.services_list()).items()}

    def update_service(self, service_name: str, service: dict = None):

        if not service:
            service = self._instance.remote.service_config(service_name)

        try:
            self.services[service_name] = Service(**service)
            return self.services[service_name]
        except Exception as e:
            print(e)

    def start_service(self, service_name: str):
        try:
            self._instance.remote.service_start(service_name)
        except Exception as e:
            print(e)

    def stop_service(self, service_name):
        try:
            self._instance.remote.service_stop(service_name)
        except Exception as e:
            print(e)

    def enable_service(self, service_name):
        try:
            self._instance.remote.service_enable(service_name)
        except Exception as e:
            print(e)

    def disable_service(self, service_name):
        try:
            self._instance.remote.service_disable(service_name)
        except Exception as e:
            print(e)


class ServiceControlView(Frame):

    def __init__(self, root, controller):
        self._controller = controller
        super(ServiceControlView, self).__init__(root)

        control_panel = Frame(self)
        details_frame = Frame(control_panel)
        controls_frame = Frame(control_panel)
        self._start_button = SwitchableButton(controls_frame, switches={1: 'Stop', 0: 'Start'},
                                              text='Start', state=DISABLED, command=self._start)
        rerun_button = Button(controls_frame, text='Rerun', state=DISABLED, command=self._rerun)
        self._enable_button = SwitchableButton(controls_frame, switches={1: 'Disable', 0: 'Enable'},
                                               text='Enable', state=DISABLED, command=self._enable)
        tree_frame = Frame(self)
        self._tree = Treeview(tree_frame)
        self._columns = ['unit', 'load', 'active', 'sub', 'description']
        self._vars = {}

        # Service details

        for i in range(len(self._columns)):
            text = self._columns[i]
            text = text.title()
            text += ':'
            var = StringVar()
            Label(details_frame, text=text).grid(column=0, row=i, sticky=W)
            Label(details_frame, textvariable=var).grid(column=1, row=i, sticky=W)
            self._vars[self._columns[i]] = var

        # TreeView
        # Scrollbar initialization
        scrollbar = Scrollbar(self._tree, orient=VERTICAL, command=self._tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # TreeView configuration
        self._tree.config(columns=self._columns[1:], yscrollcommand=scrollbar.set)

        # Tree initialization
        self._tree.heading('#0', text=self._columns[0].title())
        self._tree.column('#0', width=150, stretch=False)

        # Columns initialization
        for column in self._columns[1:]:
            self._tree.heading(column, text=column.title())
            self._tree.column(column, width=100, stretch=False)

        self._tree.column(self._columns[-1], stretch=True)

        # Items initialization
        try:
            for key, service in self._controller.services.items():
                self._tree.insert('', END, iid=key,
                                  text=key,
                                  values=[getattr(service, col, None) for col in self._columns[1:]])
        except Exception as e:
            print(e)

        # Set initial focus
        try:
            self._tree.focus(self._tree.get_children()[0])
        except Exception as e:
            print(e)

        # Bindings
        self._tree.bind('<<TreeviewSelect>>', self._controller.refresh_view)

        # Packing
        control_panel.pack(anchor=W, padx=PADX, pady=PADY, fill=X)
        details_frame.pack(fill=BOTH, padx=PADX, pady=PADY)
        controls_frame.pack(fill=BOTH, padx=PADX, pady=PADY)
        self._start_button.pack(side=LEFT, padx=PADX, pady=PADY)
        rerun_button.pack(side=LEFT, padx=PADX, pady=PADY)
        self._enable_button.pack(side=LEFT, padx=PADX, pady=PADY)
        tree_frame.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)
        self._tree.pack(padx=PADX, pady=PADY, fill=BOTH, expand=True)

    @property
    def focus(self):
        return self._tree.focus()

    def refresh(self, service):

        # Refresh tree view
        self._tree.item(getattr(service, self._columns[0]),
                        values=[getattr(service, col, None) for col in self._columns[1:]])

        # Refresh controls
        if service.unit == self.focus:

            for var in self._vars:
                self._vars[var].set(getattr(service, var, ''))

            self._start_button.switch(service.started)
            self._enable_button.switch(service.enabled)

    def _start(self):
        try:
            self._controller.start_service()
        except Exception as e:
            print(e)

    def _rerun(self):
        try:
            self._controller.rerun_service()
        except Exception as e:
            print(e)

    def _enable(self):
        try:
            self._controller.enable_service()
        except Exception as e:
            print(e)


class ServiceControlController:

    def __init__(self, root, instance):
        self._model = ServicesList(instance)
        self._view = ServiceControlView(root=root, controller=self)
        instance.subscribe_to_event(instance.EVENT_SERVICE_STATUS_CHANGED, self._on_service_update)

    @property
    def services(self):
        return self._model.services

    def _on_service_update(self, service, config):
        service = self._model.update_service(service, config)
        Thread(target=self._view.refresh, args=(service, )).start()

    def start_service(self):
        service = self.services[self._view.focus]
        try:
            if service.started:
                Thread(target=self._model.stop_service, args=(service.unit, )).start()
            else:
                Thread(target=self._model.start_service, args=(service.unit, )).start()
        except Exception as e:
            print(e)

    def enable_service(self):
        service = self.services[self._view.focus]
        try:
            if service.enabled:
                Thread(target=self._model.disable_service, args=(service.unit, )).start()
            else:
                Thread(target=self._model.enable_service, args=(service.unit, )).start()
        except Exception as e:
            print(e)

    def rerun_service(self):
        return NotImplemented

    def start(self):
        self._view.pack(fill='both', expand=True)

    def stop(self):
        self._view.pack_forget()

    def refresh_view(self, event=None):
        self._view.refresh(self.services[self._view.focus])
