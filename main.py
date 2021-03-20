#!/bin/env python3

# from app import App
# if __name__ == '__main__':
#     app = App()
#     app.run()

from datetime import datetime
from time import sleep

from navys.Remote import Remote
from navys.client.Client import Client

# from model.service_manager import Service, ServiceManager
from applets.server_info import ServerInfoModel

def my_event_cb(service, config):
    pass
    # print(f'[{datetime.now()}] Status changed: {service} | started: {config["started"]} | enabled: {config["enabled"]}')
    # print(f'Get repeatedly the config: ', remote.service_config(service))


if __name__ == '__main__':
    app = Client.get_instance(server_hostname="tst")
    # app.subscribe_to_event(Client.EVENT_SERVICE_STATUS_CHANGED, my_event_cb)
    remote: Remote = app.remote

    # sd = ServerInfoModel(app)
    # print(sd.info)

    # print(f'Server Time: {app.remote.server_info()}')

    # services = remote.services_list()
    # for service in services:
    #     print(remote.service_status(service))

    # sm = ServiceManager(remote)
    # sm.update()
    # for s in sm.services:
    #     print(s)


    # services = remote.services_list()
    #
    #
    # for service in services:
    #     serv = Service(remote, service)
    #     serv.update()
    #     print(serv)
        # kwargs = remote.service_config(service)
        # # print(kwargs)
        # serv = Service(**kwargs)
        # print(serv)
    #     print('-'*50)

    # print(remote.service_status(services))

    # print('Sleep 60 sec')
    # sleep(60)


    # servs = remote.service_config(remote.services_list())
    # print(servs)

    # while True:
    #     sleep(1)
    #     print('Starting wpa_supplicant.service')
    #     remote.service_start('wpa_supplicant.service')
    #     sleep(1)
    #     print('Stopping wpa_supplicant.service')
    #     remote.service_stop('wpa_supplicant.service')
