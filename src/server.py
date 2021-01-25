import csv
from datetime import datetime
from client.Client import Client
from model.server_manager import ServerManager
from model.service_manager import ServiceManager


class DummyServer:

    def __init__(self):
        self.system = System()
        self.client = None
        self.remote = None
        self.service_manager = None
        self.server_manager = None

    def subscribe(self, event, command):
        self.client.subscribe_to_event(event, command)

    def connect(self):
        self.client = Client.get_instance()
        # self.client.subscribe_to_event(Client.EVENT_SERVICE_STATUS_CHANGED, self.my_event_cb)
        self.remote = self.client.remote
        self.service_manager = ServiceManager(self.remote)
        self.server_manager = ServerManager(self.remote)

    def disconnect(self):
        raise NotImplementedError('Not implemented yet.')

    # def get_service_by_unit(self, unit):
    #     for service in self.services:
    #         if service.unit == unit:
    #             return service
    #
    # def get_services(self):
    #     try:
    #         print('Getting list of services')
    #         print(self._remote.services_list())
    #     except Exception as e:
    #         print(e)


    # @staticmethod
    # def get_services():
    #     path = r'D:\PyProjects\navys-client\tests\services\services.csv'
    #     services = []
    #
    #     with open(path, newline='') as file:
    #         reader = csv.reader(file, delimiter='\t')
    #         keys = next(reader)
    #         values = list(reader)
    #
    #     keys = [key.lower() for key in keys]
    #
    #     for val in values:
    #         d = dict(zip(keys, val))
    #         services.append(Service(**d))
    #
    #     return services

    def my_event_cb(self, service, config):
        """Обновлять виджеты ГУИ здесь"""
        pass
    #     print(
    #         f'[{datetime.now()}] Status changed: {service} | started: {config["started"]} | enabled: {config["enabled"]}')
    #     print(f'Get repeatedly the config: ', self._remote.service_config(service))
    #     print(self._remote.service_status(service))



class System:
    def __init__(self):
        self.host_name = 'DummyHostName'
        self.os_name = 'DummyOSName'
        self.kernel = 'DummyKernel'
        self.ram = 'DummyRAM'
        self.graphics_card = 'DummyGraphicsCard'
        self.hard_drive = 'DummyHardDrive'





