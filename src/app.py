# -*- coding: utf-8 -*-
__author__ = 'Alexey Elizarov (alexei.elizarov@gmail.com)'

from tkinter import Tk, Menu

from applets.connection_manager import ConnectionManager
from applets.main_window import MainWindowController
from client.Client import Client


class App(Tk):

    _title = 'Navy Client'
    _min_width = 900
    _min_height = 700

    def __init__(self):
        super(App, self).__init__()
        self.title(self._title)
        self.geometry(f'{self._min_width}x{self._min_height}')
        self.minsize(self._min_width, self._min_height)
        self.config(menu=MainMenu(self))
        self._tab_frame = MainWindowController(self)
        self._tab_frame.start()

    def start(self):
        self.mainloop()

    def stop(self):
        self.quit()

    @property
    def root(self):
        return self

    def connection_manager(self):
        ConnectionManager(self)

    def connect(self, kwargs):
        params = {'host': 'host',
                  'port': 'socket',
                  'server_hostname': 'host_name'}

        p = {key: kwargs[params[key]] for key in params}
        p['port'] = int(p['port'])
        try:
            instance = Client.get_instance(**p)
            instance.connect()
        except Exception as e:
            raise e
        else:
            self._tab_frame.add_tab(instance, kwargs['description'])


class MainMenu(Menu):
    def __init__(self, controller):
        super(MainMenu, self).__init__(controller.root)
        self._controller = controller
        self._server = Menu(self, tearoff=0)
        self._server.add_command(label='Connect...', command=self.connection_manager)
        self._server.add_command(label='Connect Recent', command=self.dummy)
        self._server.add_separator()
        self._server.add_command(label='Exit', command=self.exit)
        self.add_cascade(label='Server', menu=self._server)

    def create_new_connection(self):
        self._controller.create_new_connection()

    def dummy(self):
        pass

    def exit(self):
        self._controller.root.stop()

    def connection_manager(self):
        self._controller.connection_manager()
