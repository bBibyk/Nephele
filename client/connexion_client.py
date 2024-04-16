import socket
import time
import yaml

class Connexion:
    def __init__(self):
        self.load_configurations()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.configurations["network"]["client"]["host"], self.configurations["network"]["client"]["port"]))

    def load_configurations(self):
        self.configurations = None
        try:
            self.configurations = yaml.load(open("config.yaml", "r"), Loader=yaml.SafeLoader)
            self.__logger("Configurations loaded.")
        except Exception as e:
            self.__logger("Unable to load configurations.", e)

    def connect(self):
        try:
            self.__socket.connect((self.configurations["network"]["server"]["host"], self.configurations["network"]["server"]["port"]))
            self.__logger("Connexion established.")
            return True
        except Exception as e:
            self.__logger("Unable to connect.", e)
            return False
        
    def handle_request(self):
        pass

    def recv_request(self):
        request = None
        try:
            request = self.__socket.recv(1024)
            request.decode("utf-8")
            self.__logger("Request received.")
        except Exception as e:
            self.__logger("Unable to receive request.", e)
        return request
    
    def send_parameters(self):
        pass

    def send_time(self):
        pass

    def recv_photo(self):
        pass

    def __logger(self, message : str, exception : Exception = None):
        current_time = time.strftime("%d/%m/%Y-%H:%M:%S", time.localtime())
        if exception is None:
            print(f"\t[{current_time}] Connexion : {message}")
        else:
            print(f"\t[{current_time}] Connexion : {message}", exception)

if __name__ == "__main__":
    print("Test class Connexion")
    connexion = Connexion()
    print(connexion.connect())