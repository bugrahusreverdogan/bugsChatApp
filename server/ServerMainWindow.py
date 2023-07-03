from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QListWidget, QLabel, QPushButton, QLineEdit, QListWidgetItem
from PyQt5.QtCore import QRect, Qt, QThread, pyqtSignal, QObject, QMutex
import sys
import mysql.connector
from mysql.connector import MySQLConnection
from socket import socket, AF_INET, SOCK_STREAM
from threading import Event, Thread
from datetime import datetime
import time


class ServerMainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("ServerMainWindow")
        self.resize(829, 733)
        self.setWindowTitle("Bug's Chat App Server")

        self.commonChatListWidget = QListWidget(self)
        self.commonChatListWidget.setGeometry(QRect(20, 40, 351, 571))
        self.commonChatListWidget.setObjectName("CommonChatListWidget")
        
        self.actionListWidget = QListWidget(self)
        self.actionListWidget.setGeometry(QRect(390, 40, 231, 571))
        self.actionListWidget.setObjectName("ActionListWidget")

        self.onlineListWidget = QListWidget(self)
        self.onlineListWidget.setGeometry(QRect(640, 40, 171, 571))
        self.onlineListWidget.setObjectName("OnlineListWidget") 

        self.commonChatLabel = QLabel(self)
        self.commonChatLabel.setGeometry(QRect(20, 10, 101, 21))
        self.commonChatLabel.setTextFormat(Qt.AutoText)
        self.commonChatLabel.setObjectName("commonChatLabel")
        self.commonChatLabel.setText("Common Chat")

        self.onlineLabel = QLabel(self)
        self.onlineLabel.setGeometry(QRect(640, 10, 67, 19))
        self.onlineLabel.setObjectName("OnlineLabel")
        self.onlineLabel.setText("Online")

        self.actionsLabel = QLabel(self)
        self.actionsLabel.setGeometry(QRect(390, 10, 67, 19))
        self.actionsLabel.setObjectName("ActionsLabel")
        self.actionsLabel.setText("Actions")

        self.weatherLabel = QLabel(self)
        self.weatherLabel.setGeometry(QRect(390, 650, 67, 19))
        self.weatherLabel.setObjectName("WeatherLabel")

        self.timeLabel = QLabel(self)
        self.timeLabel.setGeometry(QRect(390, 690, 67, 19))
        self.timeLabel.setObjectName("TimeLabel")
        self.timeLabel.setText("Time")

        self.startServerButton = QPushButton(self)
        self.startServerButton.setGeometry(QRect(50, 640, 141, 51))
        self.startServerButton.setObjectName("StartServerButton")
        self.startServerButton.setText("Start Server")

        self.stopServerButton = QPushButton(self)
        self.stopServerButton.setGeometry(QRect(200, 640, 141, 51))
        self.stopServerButton.setObjectName("StopServerButton")
        self.stopServerButton.setText("Stop Server")

        self.timeLineEdit = QLineEdit(self)
        self.timeLineEdit.setGeometry(QRect(470, 680, 151, 27))
        self.timeLineEdit.setObjectName("TimeLineEdit")

        self.startServerButton.clicked.connect(self.startServer)
        self.stopServerButton.clicked.connect(self.stopServer)

        self.timeLineEdit.setReadOnly(True)

        self.onlines = {}
        
        self.clientThreads = []

        self.stopEvent = Event()

        self.mutex = QMutex()

        self.timeThread = Thread(target=self.timeHandling)
        self.timeThread.daemon = True
        self.timeThread.start()
    

    def closeEvent(self, event: QtGui.QCloseEvent):
        
        for client in self.clientThreads:
            client.stopEvent.set()
            client.socket.close()
            
        if not self.serverSocket == None:
            self.serverSocket.close()

        self.stopEvent.set()
        return super().closeEvent(event)
    

    def startServer(self):
        
        #database connection
        self.conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "chatAppDb"
        )

        #server socket starts for all authentication, registration and communication
        tcp_socket_host = ""
        tcp_socket_port = 29999

        self.signalHandler = SignalHandler()
        self.signalHandler.action_list_signal.connect(self.addItemToActionList)
        self.signalHandler.online_list_signal.connect(self.addItemToOnlineList)
        self.signalHandler.common_list_signal.connect(self.addItemToCommonList)
        self.signalHandler.offline_list_signal.connect(self.deleteItemFromOnlineList)

        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((tcp_socket_host, tcp_socket_port))
        self.serverSocket.listen(10)

        self.handlingSockThread = Thread(target=self.handlingSockAcception, args=())
        self.handlingSockThread.start()


    def stopServer(self):
        self.stopEvent.set()

        for client in self.clientThreads:
            client.stopEvent.set()
            client.socket.close()

        self.serverSocket.close()

    
    def addItemToActionList(self, item):
        self.mutex.lock()
        newItem = QListWidgetItem(item)
        self.actionListWidget.addItem(newItem)
        self.mutex.unlock()
    
    def addItemToOnlineList(self, online : list):
        self.mutex.lock()
        self.onlines[online[0]] = online
        newItem = str(online[1] + " " + online[2])
        newOnline = QListWidgetItem(newItem)
        newOnline.setData(1, online[0])
        self.onlineListWidget.addItem(newOnline)
        self.mutex.unlock()
    
    def deleteItemFromOnlineList(self, item : str):

        count = self.onlineListWidget.count()
        willClose = -1
        for i in range(count):
            if self.onlineListWidget.item(i).data(1) == item:
                willClose = i

        if willClose >= 0:
            self.onlineListWidget.takeItem(willClose)

    def addItemToCommonList(self, item):
        self.mutex.lock()
        newCommonMsg = QListWidgetItem(item)
        self.commonChatListWidget.addItem(newCommonMsg)
        self.mutex.unlock()

    def handlingSockAcception(self):
        
        while not self.stopEvent.is_set():
            print("handle")
            sock, addr = self.serverSocket.accept()
            handlingThread = ClientHandler(self.signalHandler, sock, addr, self.conn)
            self.clientThreads.append(handlingThread)
            handlingThread.start()
    
    def timeHandling(self):
        
        while not self.stopEvent.is_set():
            now = datetime.now()
            MyGlobals.time = now.strftime("%H:%M")
            self.timeLineEdit.setText(MyGlobals.time)
            time.sleep(0.01)


class MyGlobals:
    time = "00:00"
    clients = {}
    #{email : [socketClass, email, name, surname]}

class SignalHandler(QObject):

    action_list_signal = pyqtSignal(str)
    online_list_signal = pyqtSignal(list)
    offline_list_signal = pyqtSignal(str)
    common_list_signal = pyqtSignal(str)
    


class ClientHandler(QThread):

    def __init__(self, signalHandler : SignalHandler, clientSock : socket, clientAddr, connection : MySQLConnection):

        super().__init__()

        self.signalHandler = signalHandler
        self.socket = clientSock
        self.address = clientAddr
        self.conn = connection

        self.stopEvent = Event()
        
        self.loginSignal = "<<<??!login!??>>>"
        self.registerSignal = "<<<??!register!??>>>"
        self.commonChatSignal = "<<<??!common!??>>>"
        self.closeSignal = "<<<??!close!??>>>"
        self.mainSignal = "<<<??!main!??>>>"

        self.clients = {}

    def run(self):
        
        
        while not self.stopEvent.is_set():

            data = self.socket.recv(1024)
            if(len(data) == 0):
                time.sleep(0.01)
                continue

            data = data.decode('utf-8')
            print(data)
            msgArr = data.split(' ')

            #login handling
            if msgArr[0] == self.loginSignal:
                
                print(msgArr[0])

                email = msgArr[1]
                tup = (email,)
                query = "SELECT * FROM users WHERE email = %s"
                # id, email, name, surname, password
                mycursor = self.conn.cursor()
                mycursor.execute(query, tup)
                user = mycursor.fetchall()
                mycursor.close()

                if user:
                    if msgArr[2] == user[0][4]:
                        
                        sendData = self.loginSignal + " " + "true"
                        print(sendData)
                        sendData = sendData.encode('utf-8')

                        self.socket.send(sendData)
                        
                    else:
                        sendData = self.loginSignal + " "
                        logStr = "false"
                        sendData += logStr + " " + "password"
                        sendData = sendData.encode('utf-8')

                        self.socket.send(sendData)

                else:
                    sendData = self.loginSignal + " "
                    logStr = "false"
                    sendData += logStr + " " + "email"
                    sendData = sendData.encode('utf-8')

                    self.socket.send(sendData)

            #registration handling
            elif msgArr[0] == self.registerSignal:
                
                email = msgArr[1]
                tup = (email,)
                query = "SELECT * FROM users WHERE email = %s"
                # id, email, name, surname, password
                mycursor = self.conn.cursor()
                mycursor.execute(query, tup)
                user = mycursor.fetchall()
                mycursor.close()

                if user:
                    sendData = self.registerSignal + " " + "false" + " " + "exists"
                    sendData = sendData.encode('utf-8')

                    self.socket.send(sendData)

                else:
                    # mail, name, surname, password
                    tup = (msgArr[1], msgArr[2], msgArr[3], msgArr[4])
                    query = ("INSERT INTO users (email, name, surname, password) VALUES (%s, %s, %s, %s)")
                    mycursor = self.conn.cursor()
                    mycursor.execute(query, tup)
                    self.conn.commit()
                    
                    if (mycursor.rowcount > 0):
                        sendData = self.registerSignal + " " + "true"
                        sendData = sendData.encode('utf-8')

                        self.socket.send(sendData)
                    
                    else:
                        sendData = self.registerSignal + " " + "false" + " " + "error"
                        sendData = sendData.encode('utf-8')

                        self.socket.send(sendData)
                        
                    mycursor.close()
                        
            elif msgArr[0] == self.mainSignal:

                if msgArr[1] == 'info':
                    #msgArr[2] = email
                    mail = msgArr[2]

                    
                    #back all-online info
                    sendData = self.mainSignal + " " + "info" + " " + MyGlobals.time

                    for onln in MyGlobals.clients.keys():
                        sendData += " " + MyGlobals.clients[onln][1] + " " + MyGlobals.clients[onln][2] + " " + MyGlobals.clients[onln][3]
                    
                    print(sendData)
                    sendData = sendData.encode('utf-8')

                    self.socket.send(sendData)
                    
                    #for broadcasting-add to dict
                    tup = (mail,)
                    query = "SELECT * FROM users WHERE email = %s"
                    mycursor = self.conn.cursor()
                    mycursor.execute(query, tup)
                    user = mycursor.fetchall()
                    mycursor.close()

                    item = MyGlobals.time + " " + user[0][2] + " " + user[0][3] + " " + "Logged In"
                    
                    self.signalHandler.action_list_signal.emit(item)

                    sourceList = [user[0][1], user[0][2], user[0][3]]
                    # asyncio.run(self.tcpMulticasting("online", sourceList))
                    sendMultiData = str(self.mainSignal + " " + "online" + " " + user[0][1] + " " + user[0][2] + " " + user[0][3])
                    sendMultiData = sendMultiData.encode('utf-8')

                    for usr in MyGlobals.clients.keys():
                        MyGlobals.clients[usr][0].send(sendMultiData)
                    print(user[0][1], user[0][2])
                    MyGlobals.clients[mail] = [self.socket, user[0][1], user[0][2], user[0][3]]

                    newOnline = [user[0][1], user[0][2], user[0][3]]
                    self.signalHandler.online_list_signal.emit(newOnline)
                    print(MyGlobals.clients)

                    
                elif msgArr[1] == 'common':

                    mail = msgArr[2]
                    msg = " ".join(msgArr[3:])
                    signalData = self.mainSignal + " " + "common" + " " 
                    sendData = MyGlobals.time + " " + MyGlobals.clients[mail][2] + " " + MyGlobals.clients[mail][3] + ":" + " "
                    sendData += msg
                    
                    self.signalHandler.common_list_signal.emit(sendData)
                    
                    sendData = signalData + sendData
                    sendData = str(sendData)
                    sendData = sendData.encode('utf-8')

                    for usr in MyGlobals.clients.keys():
                        MyGlobals.clients[usr][0].send(sendData)


                
                elif msgArr[1] == 'private':
                    sourceMail = msgArr[2]
                    destinationMail = msgArr[3]
                    signalData = self.mainSignal + " " + "private" + " " + sourceMail + " "
                    time = MyGlobals.time + " "
                    nameSurname = MyGlobals.clients[sourceMail][2] + " " + MyGlobals.clients[sourceMail][3] + ": "
                    message = " ".join(msgArr[4:])
                    sendData = str(signalData + time + nameSurname + message)
                    sendData = sendData.encode('utf-8')
                    for usr in MyGlobals.clients.keys():
                        if usr == destinationMail:
                            MyGlobals.clients[destinationMail][0].send(sendData)

                    signalData = self.mainSignal + " " + "private" + " " + destinationMail + " "
                    sendData = str(signalData + time + nameSurname + message)
                    sendData = sendData.encode('utf-8')
                    MyGlobals.clients[sourceMail][0].send(sendData)



            
            elif msgArr[0] == self.closeSignal:

                if msgArr[1] == "login":

                    sendData = self.closeSignal + " " + 'login'
                    sendData = sendData.encode('utf-8')
                    self.socket.send(sendData)
                    self.socket.close()
                    self.stopEvent.set()

                elif msgArr[1] == "register":

                    sendData = self.closeSignal + " " + 'register'
                    sendData = sendData.encode('utf-8')
                    self.socket.send(sendData)
                    self.socket.close()
                    self.stopEvent.set()
                
                elif msgArr[1] == "main":

                    mail = msgArr[2]

                    sendData = self.closeSignal + " " + 'main'
                    sendData = sendData.encode('utf-8')
                    self.socket.send(sendData)

                    self.signalHandler.offline_list_signal.emit(mail)

                    actionMessage = MyGlobals.clients[mail][2] + " " + MyGlobals.clients[mail][3] + " is offline now."
                    self.signalHandler.action_list_signal.emit(actionMessage)

                    self.stopEvent.set()
                    del MyGlobals.clients[mail]
                    self.socket.close()

                    sendData = self.mainSignal + " " + 'offline' + " " + mail
                    sendData = sendData.encode('utf-8')
                    for client in MyGlobals.clients.keys():
                        MyGlobals.clients[client][0].send(sendData)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    server = ServerMainWindow()
    server.show()
    sys.exit(app.exec_())