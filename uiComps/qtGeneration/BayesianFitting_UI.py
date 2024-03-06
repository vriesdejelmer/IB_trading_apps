# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIComps/QTGeneration/BayesianFittingWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 649)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.vertical_stack = QtWidgets.QVBoxLayout()
        self.vertical_stack.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.vertical_stack.setContentsMargins(20, 20, 20, 10)
        self.vertical_stack.setSpacing(10)
        self.vertical_stack.setObjectName("vertical_stack")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.list_selector = QtWidgets.QComboBox(self.centralwidget)
        self.list_selector.setObjectName("list_selector")
        self.horizontalLayout.addWidget(self.list_selector)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.ticker_selection = QtWidgets.QComboBox(self.centralwidget)
        self.ticker_selection.setObjectName("ticker_selection")
        self.horizontalLayout.addWidget(self.ticker_selection)
        self.fit_data_button = QtWidgets.QPushButton(self.centralwidget)
        self.fit_data_button.setObjectName("fit_data_button")
        self.horizontalLayout.addWidget(self.fit_data_button)
        self.vertical_stack.addLayout(self.horizontalLayout)
        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.bottom_layout.setObjectName("bottom_layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bottom_layout.addItem(spacerItem)
        self.show_fit_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_fit_button.setObjectName("show_fit_button")
        self.bottom_layout.addWidget(self.show_fit_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bottom_layout.addItem(spacerItem1)
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setObjectName("save_button")
        self.bottom_layout.addWidget(self.save_button)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bottom_layout.addItem(spacerItem2)
        self.vertical_stack.addLayout(self.bottom_layout)
        self.vertical_stack.setStretch(0, 1)
        self.gridLayout_2.addLayout(self.vertical_stack, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Trade Maker"))
        self.label_4.setText(_translate("MainWindow", "Lists:"))
        self.label.setText(_translate("MainWindow", "Ticker:"))
        self.fit_data_button.setText(_translate("MainWindow", "Fit Data"))
        self.show_fit_button.setText(_translate("MainWindow", "Toggle Fit"))
        self.save_button.setText(_translate("MainWindow", "Save"))