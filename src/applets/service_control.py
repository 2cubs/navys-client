from threading import Thread

from applets import PADX, PADY
from applets.base import BaseController, BaseView, Refreshable

from tkinter import Frame, LEFT, END, BOTH, W, X, RIGHT, Y, VERTICAL, StringVar, DISABLED, NORMAL
from tkinter.ttk import Treeview, Button, Scrollbar, Label


class Service:

    def __init__(self, instance, name):
        self._instance = instance
        self._name = name
        self.update(self._instance.remote.service_config(self._name))

    def __str__(self):
        return str(self.__dict__)

    def update(self, attributes):
        for key, value in attributes.items():
            setattr(self, f'_{key}', value)
        return self

    @property
    def is_running(self):
        return getattr(self, '_started', False)

    @property
    def is_active(self):
        return getattr(self, '_enabled', False)

    @property
    def unit(self):
        return getattr(self, '_name')

    @property
    def load(self):
        return 'loaded'

    @property
    def active(self):
        if self.is_active:
            return 'active'
        return 'inactive'

    @property
    def sub(self):
        if self.is_running:
            return 'running'
        return 'stopped'

    @property
    def description(self):
        return getattr(self, '_description', '')

    def start(self):
        try:
            self._instance.remote.service_start(self._name)
        except Exception as e:
            print(e)

    def stop(self):
        try:
            self._instance.remote.service_stop(self._name)
        except Exception as e:
            print(e)

    def enable(self):
        try:
            self._instance.remote.service_enable(self._name)
        except Exception as e:
            print(e)

    def disable(self):
        try:
            self._instance.remote.service_disable(self._name)
        except Exception as e:
            print(e)


class ServiceControlModel:

    def __init__(self, instance):
        self._instance = instance
        self.services = self._get_services()

    def _get_services(self):
        services = {}
        for name in self._instance.remote.services_list():
            service = Service(self._instance, name)
            services[name] = service
        return services

    def update(self, service, config):
        return self.services[service].update(config)

    def subscribe(self, event, command):
        self._instance.subscribe_to_event(event, command)


class ServiceControlView(BaseView):
    def __init__(self, controller):
        super(ServiceControlView, self).__init__(controller)
        self._control_panel_frame = ServiceControlPanelFrame(self, self._controller)
        self._service_tree_frame = ServiceTreeFrame(self, self._controller)

    def refresh(self, service):
        self._service_tree_frame.refresh(service)
        if service.unit == self.item:
            self._control_panel_frame.refresh(service)

    @property
    def item(self):
        return self._service_tree_frame.get_item()


class ServiceControlController(BaseController):

    _model_cls = ServiceControlModel
    _view_cls = ServiceControlView

    def __init__(self, root, instance):
        super(ServiceControlController, self).__init__(root, instance=instance)
        self._model.subscribe(instance.EVENT_SERVICE_STATUS_CHANGED, self._on_service_update)

    @property
    def service_manager(self):
        return self._model

    def _on_service_update(self, service, config):
        # Update model
        obj = self._model.update(service, config)
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
