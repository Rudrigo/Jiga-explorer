# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Rudrigo\Desktop\SENFIO\designer\tela_producao.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormProducao(object):
    def setupUi(self, FormProducao):
        FormProducao.setObjectName("FormProducao")
        FormProducao.resize(650, 518)
        FormProducao.setStyleSheet("background-color: rgb(247, 247, 247);")
        self.verticalLayout = QtWidgets.QVBoxLayout(FormProducao)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(FormProducao)
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
        self.frame_2 = QtWidgets.QFrame(FormProducao)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.lineEditNome_1 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEditNome_1.setGeometry(QtCore.QRect(62, 43, 111, 30))
        self.lineEditNome_1.setObjectName("lineEditNome_1")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 50, 51, 16))
        self.label_6.setObjectName("label_6")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(180, 50, 41, 16))
        self.label_2.setObjectName("label_2")
        self.lineEditPath_1 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEditPath_1.setGeometry(QtCore.QRect(220, 43, 341, 30))
        self.lineEditPath_1.setObjectName("lineEditPath_1")
        self.checkBox_1 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_1.setGeometry(QtCore.QRect(580, 50, 21, 20))
        font = QtGui.QFont()
        font.setKerning(True)
        self.checkBox_1.setFont(font)
        self.checkBox_1.setAccessibleName("")
        self.checkBox_1.setAccessibleDescription("")
        self.checkBox_1.setText("")
        self.checkBox_1.setObjectName("checkBox_1")
        self.verticalLayout_2.addWidget(self.groupBox_2)
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
        self.groupBox_3.setObjectName("groupBox_3")
        self.lineEditNome_2 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditNome_2.setGeometry(QtCore.QRect(62, 43, 111, 30))
        self.lineEditNome_2.setObjectName("lineEditNome_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(10, 50, 51, 16))
        self.label_7.setObjectName("label_7")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(180, 50, 41, 16))
        self.label_3.setObjectName("label_3")
        self.lineEditPath_2 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditPath_2.setGeometry(QtCore.QRect(220, 43, 341, 30))
        self.lineEditPath_2.setObjectName("lineEditPath_2")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_2.setGeometry(QtCore.QRect(580, 50, 21, 20))
        font = QtGui.QFont()
        font.setKerning(True)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setAccessibleName("")
        self.checkBox_2.setAccessibleDescription("")
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_2.addWidget(self.groupBox_3)
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
        self.groupBox_5.setObjectName("groupBox_5")
        self.lineEditNome_3 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEditNome_3.setGeometry(QtCore.QRect(62, 43, 111, 30))
        self.lineEditNome_3.setObjectName("lineEditNome_3")
        self.label_9 = QtWidgets.QLabel(self.groupBox_5)
        self.label_9.setGeometry(QtCore.QRect(10, 50, 51, 16))
        self.label_9.setObjectName("label_9")
        self.label_5 = QtWidgets.QLabel(self.groupBox_5)
        self.label_5.setGeometry(QtCore.QRect(180, 50, 41, 16))
        self.label_5.setObjectName("label_5")
        self.lineEditPath_3 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEditPath_3.setGeometry(QtCore.QRect(220, 43, 341, 30))
        self.lineEditPath_3.setObjectName("lineEditPath_3")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_3.setGeometry(QtCore.QRect(580, 50, 21, 20))
        font = QtGui.QFont()
        font.setKerning(True)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setAccessibleName("")
        self.checkBox_3.setAccessibleDescription("")
        self.checkBox_3.setText("")
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setObjectName("groupBox_6")
        self.lineEditNome_4 = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEditNome_4.setGeometry(QtCore.QRect(62, 43, 111, 30))
        self.lineEditNome_4.setObjectName("lineEditNome_4")
        self.label_10 = QtWidgets.QLabel(self.groupBox_6)
        self.label_10.setGeometry(QtCore.QRect(10, 50, 51, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_6)
        self.label_11.setGeometry(QtCore.QRect(180, 50, 41, 16))
        self.label_11.setObjectName("label_11")
        self.lineEditPath_4 = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEditPath_4.setGeometry(QtCore.QRect(220, 43, 341, 30))
        self.lineEditPath_4.setObjectName("lineEditPath_4")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_6)
        self.checkBox_4.setGeometry(QtCore.QRect(580, 50, 21, 20))
        font = QtGui.QFont()
        font.setKerning(True)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setAccessibleName("")
        self.checkBox_4.setAccessibleDescription("")
        self.checkBox_4.setText("")
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout_2.addWidget(self.groupBox_6)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_4 = QtWidgets.QFrame(FormProducao)
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
        self.btnSairProducao = QtWidgets.QPushButton(self.frame_4)
        self.btnSairProducao.setMinimumSize(QtCore.QSize(100, 50))
        self.btnSairProducao.setStyleSheet("QPushButton {\n"
"     color: white;\n"
"     font: bold 12pt;\n"
"     background-color: #379ca8;\n"
"     border: 1px solid black;\n"
"     border-radius: 10px;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,   stop:0             rgba(60, 186, 162, 255), stop:1 rgba(98, 211, 162, 255))\n"
"}")
        self.btnSairProducao.setObjectName("btnSairProducao")
        self.horizontalLayout_4.addWidget(self.btnSairProducao)
        self.btnSalvarProducao = QtWidgets.QPushButton(self.frame_4)
        self.btnSalvarProducao.setMinimumSize(QtCore.QSize(100, 50))
        self.btnSalvarProducao.setStyleSheet("QPushButton {\n"
"     color: white;\n"
"     font: bold 12pt;\n"
"     background-color: #379ca8;\n"
"     border: 1px solid black;\n"
"     border-radius: 10px;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,   stop:0             rgba(60, 186, 162, 255), stop:1 rgba(98, 211, 162, 255))\n"
"}")
        self.btnSalvarProducao.setObjectName("btnSalvarProducao")
        self.horizontalLayout_4.addWidget(self.btnSalvarProducao)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.frame_4)

        self.retranslateUi(FormProducao)
        self.btnSairProducao.clicked.connect(FormProducao.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(FormProducao)

    def retranslateUi(self, FormProducao):
        _translate = QtCore.QCoreApplication.translate
        FormProducao.setWindowTitle(_translate("FormProducao", "Produção"))
        self.label.setText(_translate("FormProducao", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Produção - Firmware</span></p></body></html>"))
        self.groupBox_2.setTitle(_translate("FormProducao", "Arquivo 4 - Dinâmico - 0x00010000"))
        self.label_6.setText(_translate("FormProducao", "Nome: "))
        self.label_2.setText(_translate("FormProducao", "Path: "))
        self.groupBox_3.setTitle(_translate("FormProducao", "Arquivo 4 - Dinâmico - 0x00010000"))
        self.label_7.setText(_translate("FormProducao", "Nome: "))
        self.label_3.setText(_translate("FormProducao", "Path: "))
        self.groupBox_5.setTitle(_translate("FormProducao", "Arquivo 4 - Dinâmico - 0x00010000"))
        self.label_9.setText(_translate("FormProducao", "Nome: "))
        self.label_5.setText(_translate("FormProducao", "Path: "))
        self.groupBox_6.setTitle(_translate("FormProducao", "Arquivo 4 - Dinâmico - 0x00010000"))
        self.label_10.setText(_translate("FormProducao", "Nome: "))
        self.label_11.setText(_translate("FormProducao", "Path: "))
        self.btnSairProducao.setText(_translate("FormProducao", "Sair"))
        self.btnSalvarProducao.setText(_translate("FormProducao", "Salvar"))
