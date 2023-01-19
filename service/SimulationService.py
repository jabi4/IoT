from threading import Thread
from time import sleep as delay
from mqtt.MqttClient import MqttClient
from datasource.tk.TkSimulatedValues import TkSimulatedValues
from datasource.dto.IoTDto import IoTDto


class SimulationService(Thread):

    def __init__(self, mqtt: MqttClient, tkSimulated: TkSimulatedValues):
        super().__init__()
        self.mqtt = mqtt
        self.simulated = tkSimulated


    def run(self):
        while True:
            if self.simulated.simulated.get():
                iotDto = IoTDto()
                iotDto.temperature = self.simulated.temperature.get()
                iotDto.humidity = self.simulated.humidity.get()
                iotDto.pressure = self.simulated.pressure.get()
                iotDto.light = self.simulated.light.get()
                self.mqtt.publish(iotDto.getJson(), "iot/simulatedJB")

            delay(10)

