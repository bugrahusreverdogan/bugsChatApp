from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from clientLogin import Ui_ClientLoginWidget
from socket import socket, AF_INET, SOCK_STREAM
from clientStaticHandling import StaticHandling
from threading import Thread
from clientWidgets import LoginWidget


class Main():

    def main(self):

        app = QtWidgets.QApplication(sys.argv)
        client_login = LoginWidget()
        client_ui = Ui_ClientLoginWidget()
        client_ui.setupUi(client_login)
        
        self.connection(client_login)
        
        sendThread = Thread(target=StaticHandling.sendingMessage)
        recvThread = Thread(target=StaticHandling.receivingMessage)
        
        sendThread.daemon = True
        recvThread.daemon = True

        sendThread.start()
        recvThread.start()

        client_login.show()
        sys.exit(app.exec_())

        
    def connection(self, widget):
            sockIsOk = StaticHandling.connectSocket()

            if(sockIsOk == False):
                wrnngMsg = QtWidgets.QMessageBox.critical(widget,
                                                        "Connection Failed",
                                                        "Connection failed. Do you want try again?",
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                                                        QtWidgets.QMessageBox.No)
                    
                if wrnngMsg == QtWidgets.QMessageBox.Yes:
                    self.connection(widget)
                else:
                    
                    sys.exit()


if __name__ == "__main__":
    
    main = Main()
    main.main()
