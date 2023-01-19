from threading import Thread
from time import sleep as delay
from screens.SimulatorScreen import SimulatorScreen
from datasource.dto.IoTDto import IoTDto
from datetime import datetime as dt


class MovementStatusCheck(Thread):

    def __init__(self, simulator: SimulatorScreen, iotDto: IoTDto):
        super().__init__()
        self.simulator = simulator
        self.iotDto = iotDto

    def run(self):
        while True:
            if self.iotDto.lastMotionDetected is not None:
                now = dt.now()
                movementTime = dt.strptime(self.iotDto.lastMotionDetected, "%Y-%m-%d %H:%M:%S.%f")
                diff = now - movementTime
                print(f"Time diff: {diff}")
                if diff.seconds > 20:
                    self.simulator.setMovementImage(False)
                else:
                    self.simulator.setMovementImage(True)

            delay(5)
