import socket


# class which is responsible to connect to the server
class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.178.24"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            # connect and provide a msg
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()

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
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()

        except socket.error as err:
            print(err)


