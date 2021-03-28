from tkinter import Toplevel


class CustomToplevel(Toplevel):

    def __init__(self, master, **kwargs):
        super(CustomToplevel, self).__init__(master, **kwargs)
        self._master = master
        self.title(getattr(self, '_title', 'Default Title'))
        self.resizable(getattr(self, '_is_resizable', True), getattr(self, '_is_resizable', True))
        self.focus_force()
        self.grab_set()

    def start(self):
        # Set window size:
        self._master.update_idletasks()
        w = getattr(self, '_width', self.winfo_width())
        h = getattr(self, '_height', self.winfo_height())

        if w and h:
            x = int(self.master.winfo_x() + (self.master.winfo_width() - w)/2)
            y = int(self.master.winfo_y() + (self.master.winfo_height() - h)/2)
            self.geometry(f'{w}x{h}+{x}+{y}')
            self.minsize(w, h)