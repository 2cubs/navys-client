from tkinter import Tk, Menu
from tkinter import Frame, BOTH, X
from tkinter.ttk import Label

from applets.applet_manager import AppletManagerApplet


class MainWindow(Tk):

    _min_width = 900
    _min_height = 700

    def __init__(self, model):
        super(MainWindow, self).__init__()
        self._model = model
        self._build()
        self._applet = None

    def run(self):
        self.mainloop()

    def _build(self):
        self.title('Navy Client')
        self.geometry(f'{self._min_width}x{self._min_height}')
        self.minsize(self._min_width, self._min_height)
        self.main_menu = MainMenu(self)
        self.config(menu=self.main_menu)
        self.main_frame = MainFrame(self)

    def connect(self):
        try:
            self._model.subscribe()
        except Exception as e:
            print(e)
        else:
            self.main_menu.remote_menu.entryconfig('Connect', state='disabled')
            self.main_menu.remote_menu.entryconfig('Disconnect', state='normal')
            self._applet = AppletManagerApplet(model=self._model, root=self.main_frame.applet_frame)
            self._applet.run()

    def disconnect(self):
        try:
            self._model.unsubscribe()
        except Exception as e:
            print(e)
        finally:
            self.main_menu.remote_menu.entryconfig('Connect', state='normal')
            self.main_menu.remote_menu.entryconfig('Disconnect', state='disabled')
            self._applet.close()

    def exit(self):
        try:
            self._model.unsubscribe()
        except Exception as e:
            print(e)
        finally:
            self.quit()


class MainMenu(Menu):

    def __init__(self, master):
        super(MainMenu, self).__init__(master)
        self.remote_menu = Menu(self, tearoff=0)
        self.remote_menu.add_command(label='Connect', command=master.connect)
        self.remote_menu.add_command(label='Disconnect', state='disabled', command=master.disconnect)
        self.remote_menu.add_separator()
        self.remote_menu.add_command(label='Exit', command=master.exit)
        self.add_cascade(label='Server', menu=self.remote_menu)


class MainFrame(Frame):
    def __init__(self, master):
        super(MainFrame, self).__init__(master)
        self.applet_frame = AppletFrame(self)
        self.status_bar_frame = StatusBarFrame(self)
        self.pack(expand=True, fill=BOTH)


class StatusBarFrame(Frame):
    def __init__(self, master):
        super(StatusBarFrame, self).__init__(master)
        self.pack(fill=X)
        Label(self).pack()


class AppletFrame(Frame):
    def __init__(self, master):
        super(AppletFrame, self).__init__(master)
        self.pack(expand=True, fill=BOTH)