from tkinter import DoubleVar, BooleanVar


class TkSimulatedValues:

    def __init__(self):
        self.temperature = DoubleVar()
        self.humidity = DoubleVar()
        self.pressure = DoubleVar()
        self.light = BooleanVar()
        self.simulated = BooleanVar()
        self.simulated.set(False)