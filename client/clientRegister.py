# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientRegister.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from clientStaticHandling import StaticHandling
import asyncio
import clientLogin
from clientWidgets import RegisterWidget, LoginWidget

class Ui_ClientRegisterWidget(object):


    def setupUi(self, ClientRegisterWidget : RegisterWidget, loginWidget : LoginWidget):

        ClientRegisterWidget.setObjectName("ClientRegisterWidget")
        ClientRegisterWidget.resize(441, 629)
        self.nameLineEdit = QtWidgets.QLineEdit(ClientRegisterWidget)
        self.nameLineEdit.setGeometry(QtCore.QRect(140, 190, 251, 27))
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.surnameLabel = QtWidgets.QLabel(ClientRegisterWidget)
        self.surnameLabel.setGeometry(QtCore.QRect(20, 270, 67, 19))
        self.surnameLabel.setObjectName("surnameLabel")
        self.passwordAgainLabel = QtWidgets.QLabel(ClientRegisterWidget)
        self.passwordAgainLabel.setGeometry(QtCore.QRect(20, 410, 121, 19))
        self.passwordAgainLabel.setObjectName("passwordAgainLabel")
        self.surnameLineEdit = QtWidgets.QLineEdit(ClientRegisterWidget)
        self.surnameLineEdit.setGeometry(QtCore.QRect(140, 260, 251, 27))
        self.surnameLineEdit.setObjectName("surnameLineEdit")
        self.backButton = QtWidgets.QPushButton(ClientRegisterWidget)
        self.backButton.setGeometry(QtCore.QRect(220, 530, 88, 27))
        self.backButton.setObjectName("backButton")
        self.applyButton = QtWidgets.QPushButton(ClientRegisterWidget)
        self.applyButton.setGeometry(QtCore.QRect(220, 470, 88, 27))
        self.applyButton.setObjectName("applyButton")
        self.passwordLineEdit = QtWidgets.QLineEdit(ClientRegisterWidget)
        self.passwordLineEdit.setGeometry(QtCore.QRect(140, 330, 251, 27))
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.passwordAgainLineEdit = QtWidgets.QLineEdit(ClientRegisterWidget)
        self.passwordAgainLineEdit.setGeometry(QtCore.QRect(140, 400, 251, 27))
        self.passwordAgainLineEdit.setObjectName("passwordAgainLineEdit")
        self.emailLabel = QtWidgets.QLabel(ClientRegisterWidget)
        self.emailLabel.setGeometry(QtCore.QRect(20, 130, 67, 19))
        self.emailLabel.setObjectName("emailLabel")
        self.emailLineEdit = QtWidgets.QLineEdit(ClientRegisterWidget)
        self.emailLineEdit.setGeometry(QtCore.QRect(140, 120, 251, 27))
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.nameLabel = QtWidgets.QLabel(ClientRegisterWidget)
        self.nameLabel.setGeometry(QtCore.QRect(20, 200, 67, 19))
        self.nameLabel.setObjectName("nameLabel")
        self.passwordLabel = QtWidgets.QLabel(ClientRegisterWidget)
        self.passwordLabel.setGeometry(QtCore.QRect(20, 340, 67, 19))
        self.passwordLabel.setObjectName("passwordLabel")

        self.retranslateUi(ClientRegisterWidget)
        QtCore.QMetaObject.connectSlotsByName(ClientRegisterWidget)
        # ui-auto codes end

        self.clientRegisterWidget = ClientRegisterWidget
        self.loginWidget = loginWidget

        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordAgainLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.isControlled = False

        self.registerSignal = "<<<??!register!??>>>"
        self.closeSignal = "<<<??!close!??>>>"

        self.applyButton.clicked.connect(self.applyButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

    def retranslateUi(self, ClientRegisterWidget):
        _translate = QtCore.QCoreApplication.translate
        ClientRegisterWidget.setWindowTitle(_translate("ClientRegisterWidget", "Client Register"))
        self.surnameLabel.setText(_translate("ClientRegisterWidget", "surname:"))
        self.passwordAgainLabel.setText(_translate("ClientRegisterWidget", "password(again):"))
        self.backButton.setText(_translate("ClientRegisterWidget", "Back"))
        self.applyButton.setText(_translate("ClientRegisterWidget", "Apply"))
        self.emailLabel.setText(_translate("ClientRegisterWidget", "email:"))
        self.nameLabel.setText(_translate("ClientRegisterWidget", "name:"))
        self.passwordLabel.setText(_translate("ClientRegisterWidget", "password:"))

    # def closeEvent(self, event):

    #     if (self.isControlled == False):
    #        message = self.closeSignal

    #        hppn = False

    #        while(hppn == False):
    #             hppn = asyncio.run(StaticHandling.sendBufferChange(message))

    #        hppn2 = True

    #        while(hppn2):
    #             response = StaticHandling.recvBuffer.decode('utf-8')
    #             response = response.split(' ')
    #             if(response[0] == self.closeSignal):

    #                 StaticHandling.recvBuffer = bytearray()

    #                 StaticHandling.stopEvent.set()
    #                 StaticHandling.stopSocet()
    #                 hppn2 = False
    #                 super().closeEvent(event)
    #     else:
    #         super().closeEvent(event)

    def applyButtonClicked(self):

        emailTxt = self.emailLineEdit.text().replace(' ', '')
        nameTxt = self.nameLineEdit.text().replace(' ', '')
        surnameTxt = self.surnameLineEdit.text().replace(' ', '')
        passwordTxt = self.passwordLineEdit.text().replace(' ', '')
        passwordAgainTxt = self.passwordAgainLineEdit.text().replace(' ', '')

        if(emailTxt != "" and emailTxt != None
           and nameTxt != "" and nameTxt != None
           and surnameTxt != "" and surnameTxt != None
           and passwordTxt != "" and passwordTxt != None
           and passwordAgainTxt != "" and passwordAgainTxt != None):
            
            if(passwordTxt == passwordAgainTxt):

                message = self.registerSignal + " "
                message += emailTxt + " " + nameTxt + " " + surnameTxt + " " + passwordTxt

                hppn = False

                while(hppn == False):
                    hppn = asyncio.run(StaticHandling.sendBufferChange(message))

                hppn2 = True
                
                while(hppn2):
                    response = StaticHandling.recvBuffer.decode('utf-8')
                    response = response.split(' ')
                    if(response[0] == self.registerSignal):

                        StaticHandling.recvBuffer = bytearray()

                        hppn2 = False

                if(response[1] == 'true'):

                    msg = QtWidgets.QMessageBox.information(self.clientRegisterWidget, "Succesfull", 
                                                "Registration Succesful. Please go back to login!",
                                                    QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                                
                else:
                    if(response[2] == 'exists'):
                        msg = QtWidgets.QMessageBox.critical(self.clientRegisterWidget, "Failed", 
                                                    "Registration Failed. This email already exists!",
                                                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                    else:
                        msg = QtWidgets.QMessageBox.critical(self.clientRegisterWidget, "Failed", 
                                                    "Registration Failed. An unexpected error has occured, please try again!",
                                                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        
            else:
                msg = QtWidgets.QMessageBox.critical(self.clientRegisterWidget, "Failed", 
                                                    "Password Failed. Please enter the correct password!",
                                                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
            msg = QtWidgets.QMessageBox.critical(self.clientRegisterWidget, "Failed", 
                                                "Failed. Please fill in all the boxes!",
                                                    QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

    def backButtonClicked(self):

        # self.clientLogin = LoginWidget()
        # self.client_ui = clientLogin.Ui_ClientLoginWidget()
        # self.client_ui.setupUi(self.clientLogin)
        self.clientRegisterWidget.isControlled = True
        self.loginWidget.show()
        self.clientRegisterWidget.close()
