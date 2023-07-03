import socket
import asyncio
from threading import Thread, Event
from PyQt5.QtCore import QObject, pyqtSignal

class SignalClass(QObject):
    signal = pyqtSignal()

class StaticHandling:

    signalClass = SignalClass()
    receive_signal = signalClass.signal

    recvBuffer = bytearray()
    sendBuffer = bytearray()

    stopEvent = Event()

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    tcpPort = 29999
    udpPort = 39999


    @staticmethod
    async def sendBufferChange(message: str) -> bool:
        async with asyncio.Lock():
            if(len(StaticHandling.sendBuffer) == 0):
                StaticHandling.sendBuffer = message.encode('utf-8')
                return True
            else:
                return False
            
    @staticmethod
    async def recvBufferCheck() -> str:
        async with asyncio.Lock():
            if(len(StaticHandling.recvBuffer > 0)):
                response = StaticHandling.recvBuffer.decode('utf-8')
                return response
            else:
                return None
                

    @staticmethod
    def sendingMessage():

        while not StaticHandling.stopEvent.is_set():
            if(len(StaticHandling.sendBuffer) > 0):
                StaticHandling.socket.send(StaticHandling.sendBuffer)
                StaticHandling.sendBuffer = bytearray()


    @staticmethod
    def receivingMessage():
        
        while not StaticHandling.stopEvent.is_set():
            if(len(StaticHandling.recvBuffer) == 0):
                StaticHandling.recvBuffer = StaticHandling.socket.recv(1024)
                StaticHandling.receive_signal.emit()
    
    @staticmethod
    def connectSocket():
        try:
            StaticHandling.socket.connect((StaticHandling.host, StaticHandling.tcpPort))
            return True
        except:
            return False
        
    @staticmethod
    def stopSocet():
        StaticHandling.socket.close()

    @staticmethod
    def startUdpSocket():
        pass

    @staticmethod
    def stopUdpSocket():
        pass

print(len(StaticHandling.sendBuffer))