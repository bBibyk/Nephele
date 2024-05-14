import socket
from utils import *
import os
import json

class Connection:
    def __init__(self):
        self.update_configurations()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.bind((self.configurations["network"]["server"]["host"], self.configurations["network"]["server"]["port"]))

    def update_configurations(self):
        self.configurations = load_configurations("default.yaml")

    def connect(self):
        try:
            self.__socket.listen(1)
            self.__client_socket, self.__client_address = self.__socket.accept()
            logger("Connection", f"Connection established with {self.__client_address}.")
            return True
        except Exception as e:
            logger("Connection", "Unable to connect.", e)
            return False
        
    def __recv_until_end(self, buffer_size=1024):
        data = b""
        done = False
        try:
            while not done and not self.is_socket_closed():
                buffer = self.__client_socket.recv(buffer_size)
                data += buffer
                if data[-5:] == bytes("<END>", "utf-8"):
                    done = True
            return data[:-5]
        except Exception as e:
            logger("Connection", "Unable to receive data.", e)
            return None

    def __send_all_data(self, data):
        try:
            self.__client_socket.sendall(data)
            self.__client_socket.send(bytes("<END>", "utf-8"))
            logger("Connection", "Data sent.")
            return True
        except Exception as e:
            logger("Connection", "Unable to send data.", e)
            return False

    def send_request(self, request : str):
        try:
            if(self.is_socket_closed()):
                logger("Connection", "Unable to send request. Connection closed.")
                return False
            self.__client_socket.sendall(bytes(request, "utf-8"))
            logger("Connection", "Request sent.")
            return True
        except Exception as e:
            logger("Connection", "Unable to send request.", e)
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
            logger("Connection", "Unexpected exception when checking if a socket is closed.", e)
            return False
        return False
    
    def recv_configurations(self):
        logger("Connection", "Waiting for configurations...")
        data = self.__recv_until_end()
        if data is not None:
            logger("Connection", "Configurations received.")
            data = data.decode("utf-8").replace("\'", "\"")
            print(data)
            try :
                data = json.loads(fr"{data}")
            except Exception as e:
                logger("Connection", "Unable to load configurations.", e)
                return None
            self.configurations = data
            return data
        logger("Connection", "Unable to receive configurations.")
        return None

    def recv_time(self):
        logger("Connection", "Waiting for time...")
        try:
            data = self.__recv_until_end()
            if data is not None:
                logger("Connection", "Time received.")
                data = float(data.decode("utf-8"))
                return data
        except Exception as e:
            logger("Connection", "Unable to receive time.")
            return None

    def send_photo(self, filename : str):
        logger("Connection", "Sending photo " + filename + "...")
        try :
            status = self.__send_all_data(bytes(filename, "utf-8"))
            with open(get_script_directory() + "/shots/" + filename, "rb") as file:
                data = file.read()
                status = status and self.__send_all_data(data)
                file.close()
            if status:
                logger("Connection", "Photo sent.")
                return True
        except Exception as e:
            logger("Connection", "Unable to send photo.", e)
            return False

    def disconnect_client(self):
        self.__client_socket.close()
        logger("Connection", "Clinet socket closed.")
    
    def disconnect(self):
        self.__socket.close()
        logger("Connection", "Listening socket closed.")

if __name__ == "__main__":
    print("Test class Connection")
    connection = Connection()

    connection.connect()
    print(connection.send_request("<PARA>"))
    print(connection.recv_configurations())
    connection.disconnect_client()

    connection.connect()
    print(connection.send_request("<TIME>"))
    print(connection.recv_time())
    connection.disconnect_client()

    connection.connect()
    print(connection.send_request("<PHOT>"))
    print(connection.send_photo("image.jpg"))
    connection.disconnect_client()

    connection.disconnect()