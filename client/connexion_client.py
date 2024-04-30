import socket
import time
import yaml
from utils import *

class Connexion:
    def __init__(self):
        self.update_configurations()

    def update_configurations(self):
        self.configurations = load_configurations("config.yaml")

    def connect(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__socket.connect((self.configurations["network"]["server"]["host"], self.configurations["network"]["server"]["port"]))
            logger("Connexion", "Connexion established.")
            return True
        except Exception as e:
            logger("Connexion", "Unable to connect.", e)
            return False
        
    def __recv_until_end(self, buffer_size=1024):
        data = b""
        done = False
        try:
            while not done and not self.is_socket_closed():
                buffer = self.__socket.recv(buffer_size)
                data += buffer
                if data[-5:] == bytes("<END>", "utf-8"):
                    done = True
            return data[:-5]
        except Exception as e:
            logger("Connexion", "Unable to receive data.", e)
            return None

    def __send_all_data(self, data):
        try:
            self.__socket.sendall(data)
            self.__socket.send(bytes("<END>", "utf-8"))
            logger("Connexion", "Data sent.")
            return True
        except Exception as e:
            logger("Connexion", "Unable to send data.", e)
            return False
        
    def handle_request(self, request):
        if request=="<TIME>":
            self.send_time()
        elif request=="<PARA>":
            self.send_configurations()
        elif request=="<PHOT>":
            self.recv_photo()
        else:
            logger("Connexion", "Unrecognized tag received.")

    # Les balises des requêtes sont dans le format <XXXX> où XXXX est l'identifiant de la requête
    def recv_request(self):
        request = None
        try:
            logger("Connexion", "Waiting for request...")
            request = self.__socket.recv(6)
            request = request.decode("utf-8")
            logger("Connexion", "Request received.")
        except Exception as e:
            logger("Connexion", "Unable to receive request.", e)
        return request
    
    # Tag <PARA>
    def send_configurations(self):
        logger("Connexion", "Sending configurations...")
        self.update_configurations()
        status = self.__send_all_data(bytes(str(self.configurations), "utf-8"))
        if status:
            logger("Connexion", "Configurations sent.")
            return True
        logger("Connexion", "Failed sending configurations.")
        return False

    # Tag <TIME>
    def send_time(self):
        logger("Connexion", "Sending time...")
        status = self.__send_all_data(bytes(str(time.time()), "utf-8"))
        if status:
            logger("Connexion", "Time sent.")
            return True
        logger("Connexion", "Failed sending time.")
        return False
        
    # Tag <PHOT>
    def recv_photo(self):
        logger("Connexion", "Waiting for photo...")
        try :
            filename = self.__recv_until_end(1).decode("utf-8")
            filedata = self.__recv_until_end()
            path = self.configurations["client"]["storage_path"]
            with open(path + "/" + filename, "wb") as file:
                file.write(filedata)
                file.close()
            logger("Connexion", "Photo received.")
            return True
        except Exception as e:
            logger("Connexion", "Unable to receive photo.", e)
            return False
        
    def request(self):
        request = self.recv_request()
        if request is not None:
            self.handle_request(request)
            return True
        return False

    def is_socket_closed(self) -> bool:
        try:
            data = self.__socket.recv(1, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # Socket ouvert et la lecture bloquera
        except ConnectionResetError:
            return True  # socket fermée pour d'autres raisons
        except Exception as e:
            logger("Connexion", "Unexpected exception when checking if a socket is closed.", e)
            return False
        return False
    
    def disconnect(self):
        self.__socket.close()
        logger("Connexion", "Connexion closed.")

if __name__ == "__main__":
    print("Test class Connexion")
    connexion = Connexion()
    
    for i in range(3):
        connexion.connect()
        print(connexion.request())
        connexion.disconnect()