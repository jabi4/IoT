from tkinter import Tk
from screens.IoTScreen import IotScreen

class App(Tk):

    def __init__(self):
        super().__init__()
        self.title("IoT")
        self.geometry("1366x768")
        self.createServerConnection()

    def createServerConnection(self):
        IotScreen(self)



if __name__ == '__main__':
    app = App()
    app.mainloop()


