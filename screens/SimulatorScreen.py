import tkinter as tk
from tkinter import ttk, LabelFrame
from PIL import ImageTk, Image
from datasource.tk.TkSimulatedValues import TkSimulatedValues


class SimulatorScreen(LabelFrame):

    def __init__(self, parent, rpiValues, tkSimulated: TkSimulatedValues):
        super().__init__(master=parent, text="RPi")
        self.grid(padx=5, pady=5)
        self.rpiValues = rpiValues
        self.tkSimulated = tkSimulated
        self._loadImages()
        self._lastMovementStatus = False
        self.createSimulatroPanel()


    def createSimulatroPanel(self):

        lblTemperature = ttk.Label(self, image=self.tkImgTemperature)
        lblTemperature.grid(row=1, column=0, pady=5, padx=5)
        lblTemperatureValues = ttk.Label(self, textvariable=self.rpiValues.temperature)
        lblTemperatureValues.grid(row=1, column=1, padx=5, pady=5)

        lblHumidity = ttk.Label(self, image=self.tkImgHumidity)
        lblHumidity.grid(row=2, column=0, pady=5, padx=5)
        lblHumidityValue = ttk.Label(self, textvariable=self.rpiValues.humidity)
        lblHumidityValue.grid(row=2, column=1, padx=5, pady=5)

        lblPressure = ttk.Label(self, image=self.tkImgPressure)
        lblPressure.grid(row=3, column=0, pady=5, padx=5)
        lblPressureValues = ttk.Label(self, textvariable=self.rpiValues.pressure)
        lblPressureValues.grid(row=3, column=1, padx=5, pady=5)

        self.lblLight = ttk.Label(self, image=self.tkimgLightOff)
        self.lblLight.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.lblMovement = ttk.Label(self, image=self.tkimgNoMovement)
        self.lblMovement.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.cbSimulate = ttk.Checkbutton(self, text="Simulate values", variable=self.tkSimulated.simulated)
        self.cbSimulate.grid(row=0, column=3, pady=5, padx=5)

        scaleTemperature = ttk.Scale(self, from_=-30, to=60, variable=self.tkSimulated.temperature)
        scaleTemperature.grid(row=1, column=3, pady=5, padx=5)
        lblSimTemp = ttk.Label(self, textvariable=self.tkSimulated.temperature)
        lblSimTemp.grid(row=1, column=4, padx=5, pady=5)

        scaleHumidity = ttk.Scale(self, from_=0, to=100, variable=self.tkSimulated.humidity)
        scaleHumidity.grid(row=2, column=3, pady=5, padx=5)
        lblSimHum = ttk.Label(self, textvariable=self.tkSimulated.humidity)
        lblSimHum.grid(row=2, column=4, padx=5, pady=5)

        scalePressure = ttk.Scale(self, from_=900, to=1100, variable=self.tkSimulated.pressure)
        scalePressure.grid(row=3, column=3, pady=5, padx=5)
        lblSimPres = ttk.Label(self, textvariable=self.tkSimulated.pressure)
        lblSimPres.grid(row=3, column=4, padx=5, pady=5)

        cbSimulateLight = ttk.Checkbutton(self, text="Light", variable=self.tkSimulated.light)
        cbSimulateLight.grid(row=4, column=3, columnspan=2, padx=5, pady=5)



    def _loadImages(self):
        imgTemperature = Image.open("./images/thermometer.png")
        imgHumidity = Image.open("./images/humidity.png")
        imgPressure = Image.open("./images/pressure.png")
        imgLightOn = Image.open("./images/light_on.png")
        imgLightOff = Image.open("./images/light_off.png")
        imgMovementDetected = Image.open("./images/burglar.png")
        imgNoMovement = Image.open("./images/no_movement.png")


        self.tkImgTemperature = ImageTk.PhotoImage(imgTemperature)
        self.tkImgHumidity = ImageTk.PhotoImage(imgHumidity)
        self.tkImgPressure = ImageTk.PhotoImage(imgPressure)
        self.tkImgLightOn = ImageTk.PhotoImage(imgLightOn)
        self.tkimgLightOff = ImageTk.PhotoImage(imgLightOff)
        self.tkimgMovementDetected = ImageTk.PhotoImage(imgMovementDetected)
        self.tkimgNoMovement = ImageTk.PhotoImage(imgNoMovement)

    def setLightImage(self, status):
        if status:
            self.lblLight.config(image=self.tkImgLightOn)
        else:
            self.lblLight.config(image=self.tkimgLightOff)

    def setMovementImage(self, movementDetected):
        if self._lastMovementStatus != movementDetected:
            self._lastMovementStatus = movementDetected
            if movementDetected:
                self.lblMovement.config(image=self.tkimgMovementDetected)
            else:
                self.lblMovement.config(image=self.tkimgNoMovement)


