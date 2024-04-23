import socket
import os
import yaml
import time

class Connexion:
    def __init__(self):
        self.load_configurations()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.configurations["network"]["server"]["host"], self.configurations["network"]["server"]["port"]))

    def load_configurations(self):
        self.configurations = None
        try:
            self.configurations = yaml.load(open("default.yaml", "r"), Loader=yaml.SafeLoader)
            self.__logger("Configurations loaded.")
        except Exception as e:
            self.__logger("Unable to load configurations.", e)

    def connect(self):
        try:
            self.__socket.listen(1)
            self.__client_socet, self.__client_address = self.__socket.accept()
            self.__logger(f"Connexion established with {self.__client_address}.")
            return True
        except Exception as e:
            self.__logger("Unable to connect.", e)
            return False
        
    def handle_request(self):
        pass

    def send_request(self, request : str):
        try:
            if(self.is_socket_closed()):
                self.__logger("Unable to send request. Connexion closed.")
                return False
            self.__client_socet.sendall(bytes(request, "utf-8"))
            self.__logger("Request sent.")
            return True
        except Exception as e:
            self.__logger("Unable to send request.", e)
            return False
    
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

    def disconnect(self):
        self.__socket.close()
        self.__logger("Connexion closed.")

if __name__ == "__main__":
    print("Test class Connexion")
    connexion = Connexion()
    print(connexion.connect())
    print(connexion.send_request("<BALS>"))
    time.sleep(1)
    print(connexion.send_request("<SALS>"))

    connexion.disconnect()