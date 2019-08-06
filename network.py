import socket
import pickle


# class which is responsible to connect to the server
class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.178.24"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            # connect and provide a msg
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))

        except Exception as err:
            print(err)
            pass

    def send(self, data):
        """
        Function sends data to your Network
        :param data:
        :return: decoded information
        """
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))

        except socket.error as err:
            print(err)


