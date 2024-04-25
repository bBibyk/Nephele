import socket
import os
import yaml
import time
import json

class Connexion:
    def __init__(self):
        self.load_configurations()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
            self.__client_socket, self.__client_address = self.__socket.accept()
            self.__logger(f"Connexion established with {self.__client_address}.")
            return True
        except Exception as e:
            self.__logger("Unable to connect.", e)
            return False
        
    def __recv_until_end(self):
        data = b""
        done = False
        try:
            while not done and not self.is_socket_closed():
                buffer = self.__client_socket.recv(1024)
                if data[-5:] == bytes("<END>", "utf-8"):
                    done = True
                else:
                    data += buffer
            return data[:-5]
        except Exception as e:
            self.__logger("Unable to receive data.", e)
            return None

    def __send_all_data(self, data):
        try:
            self.__client_socket.sendall(data)
            self.__client_socket.send(bytes("<END>", "utf-8"))
            self.__logger("Data sent.")
            return True
        except Exception as e:
            self.__logger("Unable to send data.", e)
            return False

    def send_request(self, request : str):
        try:
            if(self.is_socket_closed()):
                self.__logger("Unable to send request. Connexion closed.")
                return False
            self.__client_socket.sendall(bytes(request, "utf-8"))
            self.__logger("Request sent.")
            return True
        except Exception as e:
            self.__logger("Unable to send request.", e)
            return False
    
    def is_socket_closed(self) -> bool:
        try:
            data = self.__client_socket.recv(1, socket.MSG_DONTWAIT | socket.MSG_PEEK)
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
    
    def recv_configurations(self):
        self.__logger("Waiting for configurations...")
        data = self.__recv_until_end()
        if data is not None:
            self.__logger("Configurations received.")
            data = data.decode("utf-8").replace("\'", "\"")
            data = json.loads(data)
            self.configurations = data
            return data
        self.__logger("Unable to receive configurations.")
        return None



    def recv_time(self):
        pass

    def send_photo(self):
        pass

    def __logger(self, message : str, exception : Exception = None):
        current_time = time.strftime("%d/%m/%Y-%H:%M:%S", time.localtime())
        if exception is None:
            print(f"\t[{current_time}] Connexion : {message}")
        else:
            print(f"\t[{current_time}] Connexion : {message}", exception)

    def disconnect_client(self):
        self.__client_socket.close()
        self.__logger("Clinet socket closed.")
    
    def disconnect(self):
        self.__socket.close()
        self.__logger("Listening socket closed.")

if __name__ == "__main__":
    print("Test class Connexion")
    connexion = Connexion()

    connexion.connect()
    print(connexion.recv_configurations())
    connexion.disconnect_client()
    connexion.disconnect()