import tkinter as tk
from tkinter import ttk, LabelFrame
from mqtt.MqttClient import MqttClient
from datetime import datetime as dt



class MessageBoxScreen(LabelFrame):

    def __init__(self, parent, mqtt:MqttClient):
        super().__init__(master=parent, text="Message box")
        self.grid(pady=5, padx=5, columnspan=2)
        self.mqtt = mqtt
        self.createMessagePanel()

    def setupCommandIndex(self):
        self.commandIndex = len(self.commands)

    def createMessagePanel(self):
        self.commands = []
        self.setupCommandIndex()

        self.messageBoxText = tk.Text(self, width=60)
        self.messageBoxText.grid(row=0, column=0, padx=5, pady=5)
        self.messageBoxText.config(state=tk.DISABLED)

        self.messegeVar = tk.StringVar()
        eMessege = ttk.Entry(self, textvariable=self.messegeVar)
        eMessege.grid(row=1, column=0, pady=5, padx=5, columnspan=2, sticky=tk.EW)
        eMessege.bind("<Return>", self.sendMessageEvent)
        eMessege.bind("<Up>", self.upArrow)
        eMessege.bind("<Down>", self.downArrow)

        lblSendTopic = ttk.Label(self, text="Send topic:")
        lblSendTopic.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.topicVar = tk.StringVar()
        eTopic = ttk.Entry(self, textvariable=self.topicVar)
        eTopic.grid(row=3, column=0, pady=5, padx=5, sticky=tk.W)

        btnSend = ttk.Button(self, text="Send", command=self.sendMessage)
        btnSend.grid(row=3, column=0, pady=5, padx=5, sticky=tk.E)

        self.messegeBoxReceive = tk.Text(self, width=60)
        self.messegeBoxReceive.grid(row=0, column=2, padx=5, pady=5)
        self.messegeBoxReceive.config(state=tk.DISABLED)



    # NAPOMENA: smisao Dto klase nam je da prosljedujemo podatke kroz aplikaciju kad se vrsi razmjena objekata kroz klase,
    # takve podatke saljemo kroz mrezu, svaki nam Dto treba imati konverziju u json da bi ga mogli poslati preko mreze do
    # nekog drugog mjesta. Dto je najobicnija data klasa koja nam ima podatke koji nam sluze kqao nekakav slozeni tip
    # podatka tj tip podatka koji nam u ovom slucaju sadrzi temperaturu, vlagu i tlak. Napravili smo pomocnu metodu
    # self.mqtt.publish(testDto.getJson() koja nam podatke pripremi u json format koji mozemo poslati kroz mrezu



    def sendMessageEvent(self, event):
        self.sendMessage()

    def upArrow(self, event):
        if self.commandIndex > 0:
            self.commandIndex -= 1
            self.messegeVar.set(self.commands[self.commandIndex])

    def downArrow(self, event):
        if self.commandIndex < len(self.commands):
            self.commandIndex += 1
            if self.commandIndex == len(self.commands):
                self.messegeVar.set("")
            else:
                self.messegeVar.set(self.commands[self.commandIndex])


    def sendMessage(self):
        messege = self.messegeVar.get().strip()
        topic = self.topicVar.get().strip()
        if messege != "" and topic != "":
            self.commands.append(messege)
            self.setupCommandIndex()
            self.mqtt.publish(messege, topic)
            output = f"[{dt.now()}]-[{topic}]: {messege}"
            self.messageBoxText.config(state=tk.NORMAL)
            self.messageBoxText.insert(tk.END, output + "\n")
            self.messageBoxText.config(state=tk.DISABLED)
            self.messageBoxText.see(tk.END) # metoda koja prikazuje posljednje poruke
            self.messegeVar.set("")

    def writeMessageToBox(self, text):
        topic, msg = text.split(";")
        self.messegeBoxReceive.config(state=tk.NORMAL)
        output = f"[{dt.now()}-[{topic}]: {msg}]"
        self.messegeBoxReceive.insert(tk.END, output + "\n")
        self.messegeBoxReceive.config(state=tk.DISABLED)