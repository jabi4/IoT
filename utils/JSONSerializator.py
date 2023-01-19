import json

# serializatori najcesce pomocna klasa koja nam pretvara json propertie u propertie nase klase
# ovaj utils mozemo krosistiti dalje kroz svo predavanje
# necemo je instancirat jer nikad necemo koristiti njezin objekt nego ce nam klase nasljedivati svojstva ove klase

def loadModel(jsonModel):
    try:
        return json.loads(jsonModel)

    except Exception as e:
        print(e)

    return jsonModel


class JSONSerializator:

    def serialize(self, jsonModel, ignoreProperties=False):
        model = loadModel(jsonModel)
        for key in model.keys():
            if ignoreProperties:
                # set atribute motoda govori gdje sta spremamo
                # dobit cemo model["temperature"]
                # ako ignoriramo propertie onda nam nije bitno koje tocno varijable nam sadrzava nas model
                setattr(self, key, model.get(key))
            else:
                # ako ne ignoriramo propertie onda cemo prvo provjeriti da li nam klasa ima vec varijablu koja se zove ka json kljuc
                if hasattr(self, key):
                    setattr(self, key, model.get(key)) # s ovim je postavimo vrijednost u varijablu

        return self

# pomocne metode koje cesto koristimo
    def dumpModel(self):
        return json.dumps(self.__dict__, indent=4)

    def __repr__(self):
        return str(self.__dict__)