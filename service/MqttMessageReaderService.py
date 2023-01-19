import tkinter
from threading import Thread
from mqtt.MqttClient import MqttClient
from time import sleep as delay
import tkinter as tk
from datetime import datetime as dt
import json
from datasource.dto.IoTDto import IoTDto
from datasource.tk.TkRPiValues import TkRPiValues
from screens.MessageBoxScreen import MessageBoxScreen
from screens.SimulatorScreen import SimulatorScreen


class MqttMessageReaderService(Thread):

    def __init__(self, mqtt:MqttClient, tkModel: TkRPiValues, messageBoxScreen: MessageBoxScreen, simulator: SimulatorScreen, iotDto: IoTDto):
        super().__init__()
        self.mqtt = mqtt
        self.iotDto = iotDto
        self.tkRpi = tkModel
        self.messageBox = messageBoxScreen
        self.simulator = simulator

    def run(self):
        while True:
            try:
                message = self.mqtt.getFromQueue()
                if message != None:
                    print(message)
                    self.messageBox.writeMessageToBox(message)
                    topic, msg = message.split(";")

                    if self.simulator.tkSimulated.simulated.get() == False:
                        topicToListen = "iot/general"
                    else:
                        topicToListen = "iot/simulatedJB"

                    if topic == topicToListen:
                        print(msg)
                        self.iotDto.serialize(msg, ignoreProperties=False)
                        print(self.iotDto.dumpModel())
                        self.tkRpi.temperature.set(round(self.iotDto.temperature, 2))
                        self.tkRpi.humidity.set(round(self.iotDto.humidity, 2))
                        self.tkRpi.pressure.set(round(self.iotDto.pressure, 2))
                        self.simulator.setLightImage(self.iotDto.light)

                else:
                    print("Nothing to read!")
            except:
                print("Nothing to read!")
            delay(1)

    def writeMessageToBox(self, text):
        topic, msg = text.split(";")
        self.messageBox.config(state=tk.NORMAL)
        output = f"[{dt.now()}-[{topic}]: {msg}]"
        self.messageBox.insert(tk.END, output + "\n")
        self.messageBox.config(state=tk.DISABLED)