import socket


class EightChanRelay():


    def __init__(self, hostname, port, NumberOfRelays):
        ''''init '''
        self._hostname = hostname
        self._port = port
        self._NumberOfRelays = NumberOfRelays
        self._buffersize = 512
        self._relays = []
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for r in range(1, self._NumberOfRelays + 1):
            x = Relay(r, "r" + str(r), self)
            self._relays.append(x)

    @property
    def hostname(self):
        return self._hostname

    @property
    def port(self):
        return self.int(_port)

    @property
    def NumberOfRelays(self):
        return self._NumberOfRelays

    @property
    def buffersize(self):
        return self.buffersize

    @property
    def relays(self):
        return self._relays

    @property
    def s(self):
        return self._s

    @hostname.setter
    def hostname(self, value):
        self._hostname = value

    @port.setter
    def port(self, value):
        self._port = value

    @NumberOfRelays.setter
    def NumberOfRelays(self, value):
        self._numberrelays = int(value)

    @buffersize.setter
    def buffersize(self, value):
        self._buffersize = value

    @relays.setter
    def relays(self, value):
        self.relays.append(value)

    @s.setter
    def s(self, value):
        self._s = value

    def connect(self):
        '''connect'''
        self._s.connect((self._hostname, self._port))

    def disconnect(self):
        self._s.close()

    def send(self, msg):
        self._s.send(msg)
        return self._s.recv(self._buffersize)

    def setRelay(self, index, on):
        '''Check if index is ok'''
        if (index > self._numberrelays):
            raise Exception("Invalid index number, maximum of " + str(self._numberrelays) + " relays.")

        if (on):
            msg = "L" + str(index)
        else:
            msg = "D" + str(index)


    def toggleRelay(self, index):
        '''Check if index is ok'''
        if (index > self._numberrelays):
            raise Exception("Invalid index number, maximum of " + str(self._numberrelays) + " relays.")

        '''Get status'''



        if str(state).find("Relayoff") != -1:
            '''turn on (L)'''
            msg = "L" + str(index)
        else:
            '''turn off (D)'''
            msg = "D" + str(index)

        s.send(msg.encode())
        data = s.recv(self._buffersize)
        s.close()

        return (data)

class Relay:
    def __init__(self, index, name, relayBoard):
        self.ind = index
        self.name = name
        self.rb = relayBoard

    @property
    def ind(self):
        return self._ind

    @property
    def name(self):
        return self._name

    @property
    def rb(self):
        return self._rb

    @ind.setter
    def ind(self, value):
        self._ind = value

    @name.setter
    def name(self, value):
        self._name = value

    @rb.setter
    def rb(self, value):
        self._rb = value

    def turnOn(self):
        msg = "L" + str(self._ind)
        try:
            self._rb.send(msg.encode())
        except Exception as e:
            self._rb.disconnect()
            self._rb.connect()
            self._rb.send(msg.encode())
    def turnOff(self):
        msg = "D" + str(self._ind)
        try:
            self._rb.send(msg.encode())
        except Exception as e:
            self._rb.disconnect()
            self._rb.connect()
            self._rb.send(msg.encode())
    def getStatus(self):
        msg = 'R' + str(self._ind)
        try:
            response = self._rb.send(msg.encode())
        except Exception as e:
            self._rb.disconnect()
            self._rb.connect()
            response = self._rb.send(msg.encode())
        if str(response).find("off") != -1:
            return False
        else:
            return True
