PADX = 2
PADY = 2


class AppletBase:

    def __init__(self, model, root):
        self._root = root
        self.model = model
        self._view = None

    def run(self):
        self._view.pack(fill='both', expand=True)

    def close(self):
        self._view.pack_forget()
