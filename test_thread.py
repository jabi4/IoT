from time import sleep as delay
from threading import Thread
#
#
# class Obicna:
#
#     def __init__(self, name):
#         self.name = name
#
#     def pokreni(self):
#         for i in range(10):
#             print(f"[{self.name}]: {i + 1}")
#             delay(1)
#
# objekt1 = Obicna("objekt1")
# objekt2 = Obicna("objekt2")
#
# objekt1.pokreni()
# objekt2.pokreni()

"""
 Kad klasa nasljedi Thread da bi dobili paralelizam unutar klase koja je nasljedila
 Thread mora imati metodu koja se zove run, ni jedna druga nece funkcijonirati
 
 start - kad pozovemo start on razi da li postoji metoda run i ako postoji on ju pokrene
"""

class Dretva(Thread):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        for i in range(10):
            print(f"[{self.name}]: {i + 1}")
            delay(1)

d1 = Dretva("Dretva1")
d2 = Dretva("Dretva2")


d1.start()
d2.start()

