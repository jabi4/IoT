from tkinter import  StringVar, BooleanVar
from PIL import ImageTk, Image

class TkConnection:

    def __init__(self):
        self.url = StringVar()
        self.port = StringVar()
        self.topic = StringVar()
        self.connectionStatus = StringVar()
        self.saveInfo = BooleanVar()
        self.imageConnected: ImageTk = None
        self.imageDisconnencted: ImageTk = None

    def loadImages(self, connectedPath, disconnectedPath):
        imageConnected = Image.open(connectedPath)
        imageDisconnected = Image.open(disconnectedPath)
        self.imageConnected = ImageTk.PhotoImage(imageConnected)
        self.imageDisconnencted = ImageTk.PhotoImage(imageDisconnected)