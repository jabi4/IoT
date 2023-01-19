import json
from utils.JSONSerializator import JSONSerializator

# NAPOMENA: smisao Dto klase nam je da prosljedujemo podatke kroz aplikaciju kad se vrsi razmjena objekata kroz klase,
# takve podatke saljemo kroz mrezu, svaki nam Dto treba imati konverziju u json da bi ga mogli poslati preko mreze do
# nekog drugog mjesta. Dto je najobicnija data klasa koja nam ima podatke koji nam sluze kqao nekakav slozeni tip
# podatka tj tip podatka koji nam u ovom slucaju sadrzi temperaturu, vlagu i tlak.
# DTO KLASE ISKLJUCIVO KORISTIMO KAO PODATKOVNI TIP NPR ZA BROJEVE NAM JE BIO INT,
# tako je testDto objekt koji u sebi sadrzi 3 varijable
# najsljedivanje je poprimanje svojstava klase koja je nasljedena

class IoTDto(JSONSerializator):

    def __init__(self):
        self.temperature = None
        self.humidity = None
        self.pressure = None
        self.objectDistance = None
        self.light = None
        self.lastMotionDetected = None

    def getJson(self):
        model = {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'light': self.light
        }
        return json.dumps(model)