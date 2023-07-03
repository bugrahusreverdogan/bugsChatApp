import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget
from clientStaticHandling import StaticHandling
import asyncio

class LoginWidget(QWidget):

    def __init__(self):
        self.closeSignal = "<<<??!close!??>>>"
        self.isControlled = False #if forced the program to exit from user 
        super().__init__()
    
    def closeEvent(self, event: QtGui.QCloseEvent):

        if (self.isControlled == False):
           message = self.closeSignal + " " + "login"

           hppn = False

           while(hppn == False):
                hppn = asyncio.run(StaticHandling.sendBufferChange(message))

           hppn2 = True

           while(hppn2):
                response = StaticHandling.recvBuffer.decode('utf-8')
                response = response.split(' ')
                if(response[0] == self.closeSignal):
                    if(response)[1] == 'login':
                        StaticHandling.recvBuffer = bytearray()

                        StaticHandling.stopEvent.set()
                        StaticHandling.stopSocet()
                        hppn2 = False
                        super().closeEvent(event)
        else:
            super().closeEvent(event)


class RegisterWidget(QWidget):

    def __init__(self):
        self.closeSignal = "<<<??!close!??>>>"
        self.isControlled = False #if forced the program to exit from user 
        super().__init__()
    
    def closeEvent(self, event: QtGui.QCloseEvent):

        if (self.isControlled == False):
           message = self.closeSignal + " " + "register"

           hppn = False

           while(hppn == False):
                hppn = asyncio.run(StaticHandling.sendBufferChange(message))

           hppn2 = True

           while(hppn2):
                response = StaticHandling.recvBuffer.decode('utf-8')
                response = response.split(' ')
                if(response[0] == self.closeSignal):
                    if(response[1] == 'register'):
                        StaticHandling.recvBuffer = bytearray()

                        StaticHandling.stopEvent.set()
                        StaticHandling.stopSocet()
                        hppn2 = False
                        super().closeEvent(event)
        else:
            super().closeEvent(event)


class ClientMainWidget(QWidget):

    def __init__(self):
        self.closeSignal = "<<<??!close!??>>>"
        self.isControlled = False #if forced the program to exit from user 
        self.mail = ""
        super().__init__()
        
    
    def closeEvent(self, event: QtGui.QCloseEvent):

        if (self.isControlled == False):
           message = self.closeSignal + " " + "main" + " " + self.mail

           hppn = False

           while(hppn == False):
                hppn = asyncio.run(StaticHandling.sendBufferChange(message))

           hppn2 = True

           while(hppn2):
                response = StaticHandling.recvBuffer.decode('utf-8')
                response = response.split(' ')
                if(response[0] == self.closeSignal):
                    if(response[1] == 'main'):
                        StaticHandling.recvBuffer = bytearray()

                        StaticHandling.stopEvent.set()
                        StaticHandling.stopSocet()
                        hppn2 = False
                        super().closeEvent(event)
        else:
            super().closeEvent(event)

