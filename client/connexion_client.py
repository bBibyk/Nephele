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

    # Les balises des requêtes sont dans le format <XXXX> où XXXX est l'identifiant de la requête
    def recv_request(self):
        request = None
        try:
            request = self.__socket.recv(6)
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

    def is_socket_closed(self) -> bool:
        try:
            data = self.__client_socet.recv(1, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        except Exception as e:
            self.__logger("Unexpected exception when checking if a socket is closed.", e)
            return False
        return False

    def __logger(self, message : str, exception : Exception = None):
        current_time = time.strftime("%d/%m/%Y-%H:%M:%S", time.localtime())
        if exception is None:
            print(f"\t[{current_time}] Connexion : {message}")
        else:
            print(f"\t[{current_time}] Connexion : {message}", exception)
    
    def disconnect(self):
        self.__socket.close()
        self.__logger("Connexion closed.")

if __name__ == "__main__":
    print("Test class Connexion")
    connexion = Connexion()
    print(connexion.connect())
    print(connexion.recv_request())

    connexion.disconnect()