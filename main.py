#!/bin/env python3

# from app import App
# if __name__ == '__main__':
#     app = App()
#     app.run()
from datetime import datetime
from time import sleep

from navys.Remote import Remote
from navys.client.Client import Client


def my_event_cb(service, config):
    print(f'[{datetime.now()}] Status changed: {service} | started: {config["started"]} | enabled: {config["enabled"]}')
    print(f'Get repeatedly the config: ', remote.service_config(service))


if __name__ == '__main__':
    app = Client.get_instance()
    app.subscribe_to_event(Client.EVENT_SERVICE_STATUS_CHANGED, my_event_cb)
    remote: Remote = app.remote

    print(f'Server Time: {remote.server_time()}')
    print(f'Initial Services: {remote.services_list()}')
    print('Sleep 60 sec')
    sleep(60)

    # while True:
    #     sleep(1)
    #     print('Starting wpa_supplicant.service')
    #     remote.service_start('wpa_supplicant.service')
    #     sleep(1)
    #     print('Stopping wpa_supplicant.service')
    #     remote.service_stop('wpa_supplicant.service')
