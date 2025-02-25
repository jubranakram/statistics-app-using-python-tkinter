from app.gui.main_window import MainWindow

class App:
    def __init__(self):
        # Specify title, size and resizable flags
        self.main_window = MainWindow("Statistics Calculator", (1000, 600), (False, False))

    def run(self):
        self.main_window.setup()
        self.main_window.mainloop()