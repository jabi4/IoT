from tkinter import ttk, Frame
import tkinter as tk
from datasource.tk.TkConnections import TkConnection
from utils.FileUtil import FileUtil
from mqtt.MqttClient import MqttClient
from time import sleep as delay
from service.MqttMessageReaderService import MqttMessageReaderService
from datasource.tk.TkRPiValues import TkRPiValues
from screens.MessageBoxScreen import MessageBoxScreen
from screens.SimulatorScreen import SimulatorScreen
from datasource.dto.IoTDto import IoTDto
from service.MovementStatusCheck import MovementStatusCheck
from datasource.tk.TkSimulatedValues import TkSimulatedValues
from service.SimulationService import SimulationService



class IotScreen(Frame):

    FILE_NAME = "ServerInfo.txt"

    def __init__(self, mainWindow):
        super().__init__(master=mainWindow)
        self.grid()
        self.tkConnection = TkConnection()
        self.tkConnection.loadImages(
            "./images/connected.png",
            "./images/disconnected.png"

        )
        self.rpiValues = TkRPiValues()
        self.iotDto = IoTDto()
        self.tkSimulated = TkSimulatedValues()
        self.connectionTriggered = False
        self.createConnectionsFrame()

    def createConnectionsFrame(self):
        connectionPanel = ttk.LabelFrame(self, text="Server connection")
        connectionPanel.grid(row=0, column=0, pady=5, padx=5, sticky=tk.N)

        lblSreverUrl = ttk.Label(connectionPanel, text="URL:")
        lblSreverUrl.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        eServerUrl = ttk.Entry(connectionPanel, textvariable=self.tkConnection.url, width=40)
        eServerUrl.grid(row=0, column=1, pady=5, padx=5)

        lblPort = ttk.Label(connectionPanel, text="Port:")
        lblPort.grid(row=1, column=0, padx=5, pady=5,sticky=tk.W)
        ePort = ttk.Entry(connectionPanel, textvariable=self.tkConnection.port)
        ePort.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        lblTopic = ttk.Label(connectionPanel, text="Topic:")
        lblTopic.grid(row=2, column=0, padx=5, pady=5,sticky=tk.W)
        eTopic = ttk.Entry(connectionPanel, textvariable=self.tkConnection.topic)
        eTopic.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        cbSaveInfo = ttk.Checkbutton(connectionPanel, text="Save server info", variable=self.tkConnection.saveInfo)
        cbSaveInfo.grid(row=3, column=1, pady=5, padx=5, sticky=tk.E)

        self.btnConnect = ttk.Button(connectionPanel, text="Connect", command=self.handleButtonConnect)
        self.btnConnect.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        lblStatus = ttk.Label(connectionPanel, textvariable=self.tkConnection.connectionStatus)
        lblStatus.grid(row=5, column=0, pady=5, padx=5)
        self.tkConnection.connectionStatus.set("Disconnected")

        self.lblStatusImage = ttk.Label(connectionPanel, image=self.tkConnection.imageDisconnencted)
        self.lblStatusImage.grid(row=5, column=1, padx=5, pady=5, sticky=tk.E)

        url, port = FileUtil.readServerInfo(self.FILE_NAME)
        if url is not None and port is not None:
            self.tkConnection.url.set(url)
            self.tkConnection.port.set(port)
            self.tkConnection.saveInfo.set(True)
        else:
            self.tkConnection.url.set("")
            self.tkConnection.port.set("")
            self.tkConnection.saveInfo.set(False)




    def handleButtonConnect(self):
        if not self.connectionTriggered:
            serverUrl = self.tkConnection.url.get()
            serverPort = self.tkConnection.port.get()
            serverTopic = self.tkConnection.topic.get()
            isSaveInfo = self.tkConnection.saveInfo.get()

            if isSaveInfo:
                FileUtil.writeServerInfo(self.FILE_NAME, f"{serverUrl};{serverPort}")
            else:
                FileUtil.writeServerInfo(self.FILE_NAME, f";")

            if serverUrl != "" and serverPort != "" and serverTopic != "":
                self.mqtt = MqttClient(serverUrl, int(serverPort), serverTopic)
                self.mqtt.start()

                timeProtection = 10
                while not self.mqtt.mqttc.is_connected():
                    if timeProtection > 0:
                        timeProtection -= 1
                        delay(.5)
                    else:
                        self.tkConnection.connectionStatus.set("Timeout")
                        break

                if self.mqtt.mqttc.is_connected():
                    self.lblStatusImage.config(image=self.tkConnection.imageConnected)
                    self.btnConnect.config(text="Disconnected")
                    self.tkConnection.connectionStatus.set("Connected")
                    self.connectionTriggered = True
                    self.createIotPanel()
            else:
                self.tkConnection.connectionStatus.set("Fill data!")

        else:
            self.mqtt.mqttc.disconnect()
            self.mqtt = None
            self.connectionTriggered = False
            self.btnConnect.config(text="Connect")
            self.lblStatusImage.config(image=self.tkConnection.imageDisconnencted)
            self.tkConnection.connectionStatus.set("Disconnected")
            self.destroyIoTPanel()

    def createIotPanel(self):
        self.iotPanel = ttk.LabelFrame(self, text="IoT Panel")
        self.iotPanel.grid(row=0, column=1, pady=5, padx=5)

        self.tabs = ttk.Notebook(self.iotPanel)
        self.tabs.grid(row=0, column=0, padx=5, pady=5)

        self.tabMessages = ttk.Frame(self.tabs)
        self.tabSimulator = ttk.Frame(self.tabs)

        self.tabs.add(self.tabMessages, text="Messages")
        self.tabs.add(self.tabSimulator, text="Simulator")

        self.messagesBoxScreen = MessageBoxScreen(self.tabMessages, self.mqtt)
        self.simulatorScreen = SimulatorScreen(self.tabSimulator, self.rpiValues, self.tkSimulated)

        mqttMessageReaderService = MqttMessageReaderService(self.mqtt, self.rpiValues, self.messagesBoxScreen, self.simulatorScreen, self.iotDto)
        mqttMessageReaderService.start()

        movementStatusCheck = MovementStatusCheck(self.simulatorScreen, self.iotDto)
        movementStatusCheck.start()

        simulationService = SimulationService(self.mqtt, self.tkSimulated)
        simulationService.start()

    def destroyIoTPanel(self):
        self.iotPanel.grid_remove()


















