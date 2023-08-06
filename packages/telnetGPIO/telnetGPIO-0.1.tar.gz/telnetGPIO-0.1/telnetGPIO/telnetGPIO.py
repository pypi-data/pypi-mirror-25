import asyncio
import paho.mqtt.publish as publish
import telnetlib
from bitarray import bitarray
import binascii

class MqttChangeHandler:
    def __init__(self, mqqthost, mqttport, sender):
        self._mqtthost = mqqthost
        self._mqttport = mqttport
        self._sender = sender

    async def __aenter__(self):
        self._brokerHost = self._mqtthost
        self._brokerPort = self._mqttport
        self._sender = self._sender
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self

    async def sendDiff(self, newState, oldState):
        try:
            diff = newState ^ oldState

            for q in range(len(diff)):
                if diff[q]:
                    publish.single("home-assistant/" + str(self._sender) + "/" + str((q + 1)),
                                   payload=str(newState[(q)]),
                                   hostname= str(self._brokerHost),
                                   port=self._brokerPort)
            return True
        except:
            return False

class telnetGPIOHandler():
    def __init__(self, mqttHost, mqttPort, devName, telnethost):
        self._tn = telnetlib.Telnet(telnethost)
        self._devName = devName
        self._brokerPort = mqttPort
        self._oldState = "FFFFFFFF"
        self._newState = "FFFFFFFF"
        self._loop = asyncio.get_event_loop()
        self._mqttChangeHandler = MqttChangeHandler(mqttHost, mqttPort, devName)
        self._xOld = bitarray(endian='big')
        self._xNew = bitarray(endian='big')

    @property
    def oldState(self):
        return self._oldState

    @oldState.setter
    def oldState(self, value):
        self._oldState = value

    @property
    def newState(self):
        return self._newState

    @newState.setter
    def newState(self, value):
        self._newState = value

    def initializeConn(self, username="", password=""):
        # Still need to implement username and password
        self._tn.read_until(("User Name: ").encode())
        self._tn.write("\n".encode('ascii'))
        self._tn.read_until(("Password: ").encode())
        self._tn.write("\n".encode('ascii'))

    def read(self):
        self._oldState = self._newState
        self._xOld = self._xNew
        self._tn.write("gpio readall \n".encode('ascii'))
        self._newState = str(self._tn.read_some()).rstrip('\\r\\n>\'').lstrip('b\'')

    def updateBinary(self):
        try:
            self._xNew = bitarray(endian='big')
            bNewState = binascii.unhexlify(self._newState)
            self._xNew.frombytes(bNewState)
        except:
            return False
    def writeChange(self):
        return self._loop.run_until_complete(self.__async__writeChange(self._xNew, self._xOld))

    async def __async__writeChange(self, nS, oS):
        async with self._mqttChangeHandler as sender:
            return await sender.sendDiff(nS, oS)
