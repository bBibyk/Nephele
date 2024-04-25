import socket
import time
import yaml

class Connexion:
    def __init__(self):
        self.load_configurations()

    def load_configurations(self):
        self.configurations = None
        try:
            self.configurations = yaml.load(open("config.yaml", "r"), Loader=yaml.SafeLoader)
            self.__logger("Configurations loaded.")
            return True
        except Exception as e:
            self.__logger("Unable to load configurations.", e)
            return False

    def connect(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__socket.bind((self.configurations["network"]["client"]["host"], self.configurations["network"]["client"]["port"]))
            self.__socket.connect((self.configurations["network"]["server"]["host"], self.configurations["network"]["server"]["port"]))
            self.__logger("Connexion established.")
            return True
        except Exception as e:
            self.__logger("Unable to connect.", e)
            return False
        
    def handle_request(self, request):
        if request=="<BALS>":
            self.__logger("Default tag received.")
        elif request=="<TIME>":
            self.send_time()
        elif request=="<PARA>":
            self.send_parameters()
        elif request=="<PHOT>":
            self.recv_photo()
        else:
            self.__logger("Unrecognized tag received.")

    # Les balises des requêtes sont dans le format <XXXX> où XXXX est l'identifiant de la requête
    def recv_request(self):
        request = None
        try:
            self.__logger("Waiting for request...")
            request = self.__socket.recv(6)
            request = request.decode("utf-8")
            self.__logger("Request received.")
        except Exception as e:
            self.__logger("Unable to receive request.", e)
        return request
    
    # Balise <PARA>
    def send_parameters(self):
        self.__logger("Sending parameters...")
        self.__logger("Parameters sent.")

    # Balise <TIME>
    def send_time(self):
        try:
            if(self.is_socket_closed()):
                self.__logger("Unable to send request. Connexion closed.")
                return False
            self.__socket.sendall(bytes(time.time(), "utf-8"))
            self.__logger("Time sent.")
            return True
        except Exception as e:
            self.__logger("Unable to send request.", e)
            return False

    # Balise <PHOT>
    def recv_photo(self):
        self.__logger("Waiting for photo...")
        self.__logger("Photo received.")

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
    
    connexion.disconnect()