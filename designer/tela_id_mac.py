# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Rudrigo\Desktop\SENFIO_V1.1\designer\tela_id_mac.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormIdMac(object):
    def setupUi(self, FormIdMac):
        FormIdMac.setObjectName("FormIdMac")
        FormIdMac.resize(650, 518)
        FormIdMac.setLayoutDirection(QtCore.Qt.LeftToRight)
        FormIdMac.setStyleSheet("background-color: rgb(247, 247, 247);")
        self.verticalLayout = QtWidgets.QVBoxLayout(FormIdMac)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(FormIdMac)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 50))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(274, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(274, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(FormIdMac)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.lineEditMac1 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditMac1.setEnabled(True)
        self.lineEditMac1.setGeometry(QtCore.QRect(62, 43, 211, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditMac1.setFont(font)
        self.lineEditMac1.setObjectName("lineEditMac1")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 50, 51, 16))
        self.label_6.setObjectName("label_6")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(290, 50, 61, 20))
        self.label_2.setObjectName("label_2")
        self.lineEditNSerie1 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditNSerie1.setGeometry(QtCore.QRect(360, 43, 231, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditNSerie1.setFont(font)
        self.lineEditNSerie1.setObjectName("lineEditNSerie1")
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setStyleSheet("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.lineEditMac2 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditMac2.setGeometry(QtCore.QRect(62, 43, 211, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditMac2.setFont(font)
        self.lineEditMac2.setObjectName("lineEditMac2")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setGeometry(QtCore.QRect(10, 50, 51, 16))
        self.label_8.setObjectName("label_8")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(290, 50, 61, 20))
        self.label_4.setObjectName("label_4")
        self.lineEditNSerie2 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditNSerie2.setGeometry(QtCore.QRect(360, 43, 231, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditNSerie2.setFont(font)
        self.lineEditNSerie2.setObjectName("lineEditNSerie2")
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setStyleSheet("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.lineEditMac3 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEditMac3.setGeometry(QtCore.QRect(62, 43, 211, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditMac3.setFont(font)
        self.lineEditMac3.setObjectName("lineEditMac3")
        self.label_9 = QtWidgets.QLabel(self.groupBox_4)
        self.label_9.setGeometry(QtCore.QRect(10, 50, 51, 16))
        self.label_9.setObjectName("label_9")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(290, 50, 61, 20))
        self.label_5.setObjectName("label_5")
        self.lineEditNSerie3 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEditNSerie3.setGeometry(QtCore.QRect(360, 43, 231, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditNSerie3.setFont(font)
        self.lineEditNSerie3.setObjectName("lineEditNSerie3")
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.groupBox_5 = QtWidgets.QGroupBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setStyleSheet("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.lineEditMac4 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEditMac4.setGeometry(QtCore.QRect(62, 43, 211, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditMac4.setFont(font)
        self.lineEditMac4.setObjectName("lineEditMac4")
        self.label_10 = QtWidgets.QLabel(self.groupBox_5)
        self.label_10.setGeometry(QtCore.QRect(10, 50, 51, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_5)
        self.label_11.setGeometry(QtCore.QRect(290, 50, 61, 20))
        self.label_11.setObjectName("label_11")
        self.lineEditNSerie4 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEditNSerie4.setGeometry(QtCore.QRect(360, 43, 231, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditNSerie4.setFont(font)
        self.lineEditNSerie4.setObjectName("lineEditNSerie4")
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_4 = QtWidgets.QFrame(FormIdMac)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.btnOKiDmac = QtWidgets.QPushButton(self.frame_4)
        self.btnOKiDmac.setMinimumSize(QtCore.QSize(200, 50))
        self.btnOKiDmac.setStyleSheet("QPushButton {\n"
"     color: white;\n"
"     font: bold 12pt;\n"
"     background-color: #379ca8;\n"
"     border: 1px solid black;\n"
"     border-radius: 10px;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,   stop:0             rgba(60, 186, 162, 255), stop:1 rgba(98, 211, 162, 255))\n"
"}")
        self.btnOKiDmac.setObjectName("btnOKiDmac")
        self.horizontalLayout_4.addWidget(self.btnOKiDmac)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.frame_4)

        self.retranslateUi(FormIdMac)
        self.btnOKiDmac.clicked.connect(FormIdMac.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(FormIdMac)

    def retranslateUi(self, FormIdMac):
        _translate = QtCore.QCoreApplication.translate
        FormIdMac.setWindowTitle(_translate("FormIdMac", "Nº Série"))
        self.label.setText(_translate("FormIdMac", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Números de Série</span></p></body></html>"))
        self.groupBox.setTitle(_translate("FormIdMac", "Placa 1"))
        self.label_6.setText(_translate("FormIdMac", "MAC:"))
        self.label_2.setText(_translate("FormIdMac", "Nº Série:"))
        self.groupBox_3.setTitle(_translate("FormIdMac", "Placa 2"))
        self.label_8.setText(_translate("FormIdMac", "MAC:"))
        self.label_4.setText(_translate("FormIdMac", "Nº Série:"))
        self.groupBox_4.setTitle(_translate("FormIdMac", "Placa 3"))
        self.label_9.setText(_translate("FormIdMac", "MAC:"))
        self.label_5.setText(_translate("FormIdMac", "Nº Série:"))
        self.groupBox_5.setTitle(_translate("FormIdMac", "Placa 4"))
        self.label_10.setText(_translate("FormIdMac", "MAC:"))
        self.label_11.setText(_translate("FormIdMac", "Nº Série:"))
        self.btnOKiDmac.setText(_translate("FormIdMac", "OK"))
