from tkinter import PhotoImage
from tkinter.ttk import Notebook, Style
from applets.instance_manager import InstanceController


class TabView(Notebook):

    def __init__(self, controller, root, **kwargs):
        self._controller = controller
        super(TabView, self).__init__(root, **kwargs)
        style = Style()
        self.images = (PhotoImage("img_close", data='''
                    R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                    d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                    5kEJADs=
                    '''),
                       PhotoImage("img_closeactive", data='''
                    R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                    AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                    '''),
                       PhotoImage("img_closepressed", data='''
                    R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                    d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                    5kEJADs=
                '''))
        style.element_create("close", "image", "img_close",
                             ("active", "pressed", "!disabled", "img_closepressed"),
                             ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])

        self._active = None
        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)
        self.config(style='CustomNotebook')

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""
        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element = self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            applet = self._controller.applets.pop(index)
            applet.stop_applet()
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

        if len(self._controller.applets) == 0:
            self.pack_forget()

    def add_tab(self, frame, text):
        self.add(frame, text=text)
        self.pack(expand=True, fill='both')


class TabController:

    _model_cls = None
    _view_cls = TabView

    def __init__(self, root):
        self._view = self._view_cls(controller=self, root=root)
        self._instances = []

    def add_tab(self, instance, text):
        instance_controller = InstanceController(root=self._view, instance=instance)
        self._instances.append(instance_controller)
        self._view.add_tab(instance_controller.view, text)