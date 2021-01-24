from model.base_manager import BaseManager


class ServiceManager(BaseManager):

    def __init__(self, remote):
        super(ServiceManager, self).__init__(remote)
        self.services = {}

    def update(self):
        self.services = {}
        services = self._remote.services_list()
        for serv_name in services:
            service = Service(self._remote, serv_name)
            service.update()
            self.services[serv_name] = service


class Service:
    def __init__(self, remote, name):
        self._remote = remote
        self._name = name

    def __str__(self):
        return str(self.__dict__)

    def update(self):
        kwargs = self._remote.service_config(self._name)
        for key, value in kwargs.items():
            setattr(self, f'_{key}', value)

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
            self._remote.service_start(self._name)
        except Exception as e:
            print(e)
        else:
            self.update()

    def stop(self):
        try:
            self._remote.service_stop(self._name)
        except Exception as e:
            print(e)
        else:
            self.update()

    def enable(self):
        try:
            self._remote.service_enable(self._name)
        except Exception as e:
            print(e)
        else:
            self.update()

    def disable(self):
        try:
            self._remote.service_disable(self._name)
        except Exception as e:
            print(e)
        else:
            self.update()
