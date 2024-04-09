import socket
import time

class Connexion:
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind(("localhost", 4000))
        self.__socket.connect(("localhost", 4202))
        self.__socket.sendall(b"Hello")
        print("Data sent")
        data = self.__socket.recv(1024)
        print("Received", repr(data))
        self.__socket.close() ### Envoi-t-il un message de fin ?

    def connect(self):
        # TODO
        pass

    def refrech_parameters(self, parameters : dict):
        # TODO
        pass

if __name__ == "__main__":
    print("Test class Connexion")
    connexion = Connexion()