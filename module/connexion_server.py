import socket
import os

class Connexion:
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind(("localhost", 4202))
        self.__socket.listen(10)
        self.client_socet, self.client_address = self.__socket.accept()
        print("Connection from", self.client_address)
        data = self.client_socet.recv(1024)
        print("Received", repr(data))
        self.client_socet.send(b"Hi, how are you ?")
        print("Data sent")
        data = self.client_socet.recv(1024) #Est-ce bloquant ?
        self.client_socet.close()
        self.__socket.close()

    def open_connection(self):
        pass

    def synchronize(self):
        pass

if __name__ == "__main__":
    print("***Test class Connexion***")
    connexion = Connexion()
    