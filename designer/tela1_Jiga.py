# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Rudrigo\Desktop\SENFIO\designer\tela1_Jiga.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 575)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("background-color: rgb(247, 247, 247);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet("border: 0px;\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("designer/img/logoSenfio2.jpeg"))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setStyleSheet("border: 0px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setLineWidth(0)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setKerning(True)
        self.frame_3.setFont(font)
        self.frame_3.setStyleSheet("border: 0px;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setLineWidth(0)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        self.btnTestePcb = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTestePcb.sizePolicy().hasHeightForWidth())
        self.btnTestePcb.setSizePolicy(sizePolicy)
        self.btnTestePcb.setMinimumSize(QtCore.QSize(5, 80))
        self.btnTestePcb.setStyleSheet("QPushButton {\n"
"     color: white;\n"
"     font: bold 12pt;\n"
"     background-color: #379ca8; \n"
"     border: 1px solid black;\n"
"     border-radius: 40px;\n"
"     width: 10px;                                             \n"
"     height: 10px;                                             \n"
"    \n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,   stop:0             rgba(60, 186, 162, 255), stop:1 rgba(98, 211, 162, 255))\n"
"}")
        self.btnTestePcb.setObjectName("btnTestePcb")
        self.horizontalLayout.addWidget(self.btnTestePcb)
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.btnGravacao = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGravacao.sizePolicy().hasHeightForWidth())
        self.btnGravacao.setSizePolicy(sizePolicy)
        self.btnGravacao.setMinimumSize(QtCore.QSize(5, 80))
        self.btnGravacao.setStyleSheet("QPushButton {\n"
"    color: white;\n"
"    font: bold 12pt;\n"
"     background-color: #379ca8;\n"
"     border: 1px solid black;\n"
"     border-radius: 40px;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,   stop:0             rgba(60, 186, 162, 255), stop:1 rgba(98, 211, 162, 255))\n"
"}")
        self.btnGravacao.setObjectName("btnGravacao")
        self.horizontalLayout.addWidget(self.btnGravacao)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.verticalLayout.addWidget(self.frame_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1024, 26))
        self.menuBar.setMouseTracking(True)
        self.menuBar.setStyleSheet("")
        self.menuBar.setObjectName("menuBar")
        self.menuConfigura_o = QtWidgets.QMenu(self.menuBar)
        self.menuConfigura_o.setMouseTracking(True)
        self.menuConfigura_o.setFocusPolicy(QtCore.Qt.NoFocus)
        self.menuConfigura_o.setStyleSheet("")
        self.menuConfigura_o.setToolTipsVisible(False)
        self.menuConfigura_o.setObjectName("menuConfigura_o")
        MainWindow.setMenuBar(self.menuBar)
        self.actionPCB = QtWidgets.QAction(MainWindow)
        self.actionPCB.setObjectName("actionPCB")
        self.actionConex_o = QtWidgets.QAction(MainWindow)
        self.actionConex_o.setObjectName("actionConex_o")
        self.actionCalibra_o = QtWidgets.QAction(MainWindow)
        self.actionCalibra_o.setObjectName("actionCalibra_o")
        self.actionProdu_o = QtWidgets.QAction(MainWindow)
        self.actionProdu_o.setObjectName("actionProdu_o")
        self.actionSair = QtWidgets.QAction(MainWindow)
        self.actionSair.setObjectName("actionSair")
        self.actionConfigura_o = QtWidgets.QAction(MainWindow)
        self.actionConfigura_o.setObjectName("actionConfigura_o")
        self.actionServidor = QtWidgets.QAction(MainWindow)
        self.actionServidor.setObjectName("actionServidor")
        self.menuConfigura_o.addAction(self.actionPCB)
        self.menuConfigura_o.addSeparator()
        self.menuConfigura_o.addAction(self.actionProdu_o)
        self.menuConfigura_o.addAction(self.actionCalibra_o)
        self.menuConfigura_o.addAction(self.actionConex_o)
        self.menuConfigura_o.addSeparator()
        self.menuConfigura_o.addAction(self.actionServidor)
        self.menuConfigura_o.addAction(self.actionConfigura_o)
        self.menuConfigura_o.addSeparator()
        self.menuConfigura_o.addAction(self.actionSair)
        self.menuBar.addAction(self.menuConfigura_o.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Jiga SENFIO"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Jiga - Explorer</span></p><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Tecnologia e Inovação</span></p></body></html>"))
        self.btnTestePcb.setText(_translate("MainWindow", "Teste PCB"))
        self.btnGravacao.setText(_translate("MainWindow", "Gravação"))
        self.menuConfigura_o.setTitle(_translate("MainWindow", "Menu"))
        self.actionPCB.setText(_translate("MainWindow", "PCB"))
        self.actionPCB.setIconText(_translate("MainWindow", "PCB"))
        self.actionConex_o.setText(_translate("MainWindow", "Conexão"))
        self.actionCalibra_o.setText(_translate("MainWindow", "Calibração"))
        self.actionProdu_o.setText(_translate("MainWindow", "Produção"))
        self.actionSair.setText(_translate("MainWindow", "Sair"))
        self.actionConfigura_o.setText(_translate("MainWindow", "Configuração"))
        self.actionServidor.setText(_translate("MainWindow", "Servidor"))
import designer
