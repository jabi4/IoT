from os import path

class FileUtil:

    @staticmethod
    def writeServerInfo(fileName, info):
        with open(fileName, "w") as f:
            f.write(f"{info}")
            f.close()

    @staticmethod
    def readServerInfo(fileName):
        if path.exists(fileName):
            f = open(fileName, "r")
            line = f.readline()
            f.close()
            url, port = line.split(";")
            if (url is not None and url != "") and (port is not None and port != ""):
                return url, port
            else:
                print("File dose not contain server info.")
                return None, None
        else:
            print("File does not exist.")
            return None, None

