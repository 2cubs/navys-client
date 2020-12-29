from gui import GUI


class App:

    def __init__(self):
        self.model = None
        self.view = GUI(self)

    def run(self):
        self.view.mainloop()

    def quit(self):
        self.view.quit()