# from app import App
# if __name__ == '__main__':
#     app = App()
#     app.run()
from time import sleep

from navys.client.Client import Client


def my_event_cb(service, status):
    print(f'Event of my event cb!!! service: {service}; status: {status}')


if __name__ == '__main__':
    app = Client.get_instance()
    app.subscribe_to_event(Client.EVENT_SERVICE_STATUS_CHANGED, my_event_cb)
    remote = app.remote

    server_time = remote.server_time()
    print(f'Server Time: {server_time}')
    print(f'Sleeping 20 sec before exiting')
    sleep(20)
