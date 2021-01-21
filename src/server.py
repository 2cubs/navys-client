import csv
from datetime import datetime
from client.Client import Client


class DummyServer:

    def __init__(self):
        self.services = self.get_services()
        self.system = System()
        self._client = None
        self._remote = None

    def subscribe(self):
        self._client = Client.get_instance()
        self._client.subscribe_to_event(Client.EVENT_SERVICE_STATUS_CHANGED, self.my_event_cb)
        self._remote = self._client.remote

    def unsubscribe(self):
        raise NotImplementedError('Not implemented yet.')

    def get_service_by_unit(self, unit):
        for service in self.services:
            if service.unit == unit:
                return service

    @staticmethod
    def get_services():
        path = r'D:\PyProjects\navys-client\tests\services\services.csv'
        services = []

        with open(path, newline='') as file:
            reader = csv.reader(file, delimiter='\t')
            keys = next(reader)
            values = list(reader)

        keys = [key.lower() for key in keys]

        for val in values:
            d = dict(zip(keys, val))
            services.append(Service(**d))

        return services

    def my_event_cb(self, service, config):
        print(
            f'[{datetime.now()}] Status changed: {service} | started: {config["started"]} | enabled: {config["enabled"]}')
        print(f'Get repeatedly the config: ', self._remote.service_config(service))


class Service:
    def __init__(self, **kwargs):
        self.unit = kwargs['unit']
        self.load = kwargs['load']
        self.active = kwargs['active']
        self.sub = kwargs['sub']
        self.description = kwargs['description']

    def __str__(self):
        return str(self.__dict__)

    def start(self):
        self.sub = 'running'

    def stop(self):
        self.sub = 'stopped'

    def rerun(self):
        self.sub = 'rerunning...'

    def enable(self):
        self.active = 'active'

    def disable(self):
        self.active = 'inactive'


class System:
    def __init__(self):
        self.host_name = 'DummyHostName'
        self.os_name = 'DummyOSName'
        self.kernel = 'DummyKernel'
        self.ram = 'DummyRAM'
        self.graphics_card = 'DummyGraphicsCard'
        self.hard_drive = 'DummyHardDrive'





