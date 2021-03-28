from tkinter import Frame, Tk, StringVar
from tkinter.ttk import Label, Entry, Button


class LabeledEntry(Frame):

    def __init__(self, master, label: str, hint: str = None, search_help: object = None):
        super(LabeledEntry, self).__init__(master)
        self._var = StringVar()
        self.label = Label(self, text=label)
        self.entry = Entry(self, textvariable=self._var)
        self.label.grid(column=0, row=0, sticky='W')
        self.entry.grid(column=1, row=0, sticky='W')

        if hint:
            self.hint = Label(self, text=hint, font=('', 7), foreground='gray')
            self.hint.grid(column=1, row=1, sticky='W')

        if callable(search_help):
            self.search_help = Button(self, text='...', width=3, command=search_help)
            self.search_help.grid(column=2, row=0, sticky='W')

    @property
    def value(self):
        return self._var.get()

    @value.setter
    def value(self, value):
        self._var.set(value)

    def register(self, callback):
        self._var.trace('w', callback)