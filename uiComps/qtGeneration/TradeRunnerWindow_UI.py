
# Copyright (c) 2024 Jelmer de Vries
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation in its latest version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIComps/QTGeneration/TradeRunnerWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.bar_selector = QtWidgets.QComboBox(self.tab)
        self.bar_selector.setObjectName("bar_selector")
        self.gridLayout_2.addWidget(self.bar_selector, 6, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 6, 0, 1, 1)
        self.sel_all_button = QtWidgets.QPushButton(self.tab)
        self.sel_all_button.setObjectName("sel_all_button")
        self.gridLayout_2.addWidget(self.sel_all_button, 3, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 2, 1, 1)
        self.list_selector = QtWidgets.QComboBox(self.tab)
        self.list_selector.setObjectName("list_selector")
        self.gridLayout_2.addWidget(self.list_selector, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.strategy3_radio = QtWidgets.QCheckBox(self.tab)
        self.strategy3_radio.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.strategy3_radio.setObjectName("strategy3_radio")
        self.gridLayout_2.addWidget(self.strategy3_radio, 10, 2, 1, 1)
        self.strategy4_radio = QtWidgets.QCheckBox(self.tab)
        self.strategy4_radio.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.strategy4_radio.setObjectName("strategy4_radio")
        self.gridLayout_2.addWidget(self.strategy4_radio, 10, 3, 1, 1)
        self.strategy2_radio = QtWidgets.QCheckBox(self.tab)
        self.strategy2_radio.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.strategy2_radio.setObjectName("strategy2_radio")
        self.gridLayout_2.addWidget(self.strategy2_radio, 10, 1, 1, 1)
        self.stairstep_radio = QtWidgets.QCheckBox(self.tab)
        self.stairstep_radio.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.stairstep_radio.setObjectName("stairstep_radio")
        self.gridLayout_2.addWidget(self.stairstep_radio, 10, 0, 1, 1)
        self.data_toggle_button = QtWidgets.QPushButton(self.tab)
        self.data_toggle_button.setObjectName("data_toggle_button")
        self.gridLayout_2.addWidget(self.data_toggle_button, 13, 3, 1, 1)
        self.load_model_button = QtWidgets.QPushButton(self.tab)
        self.load_model_button.setObjectName("load_model_button")
        self.gridLayout_2.addWidget(self.load_model_button, 13, 2, 1, 1)
        self.perform_prep_button = QtWidgets.QPushButton(self.tab)
        self.perform_prep_button.setObjectName("perform_prep_button")
        self.gridLayout_2.addWidget(self.perform_prep_button, 13, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.tab_3)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel_trades_button = QtWidgets.QPushButton(self.tab_3)
        self.cancel_trades_button.setObjectName("cancel_trades_button")
        self.horizontalLayout.addWidget(self.cancel_trades_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.trade_toggle_button = QtWidgets.QPushButton(self.tab_3)
        self.trade_toggle_button.setObjectName("trade_toggle_button")
        self.horizontalLayout.addWidget(self.trade_toggle_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.timeEdit_2 = QtWidgets.QTimeEdit(self.tab_2)
        self.timeEdit_2.setMaximumTime(QtCore.QTime(20, 0, 0))
        self.timeEdit_2.setMinimumTime(QtCore.QTime(4, 0, 0))
        self.timeEdit_2.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
        self.timeEdit_2.setTimeSpec(QtCore.Qt.TimeZone)
        self.timeEdit_2.setTime(QtCore.QTime(20, 0, 0))
        self.timeEdit_2.setObjectName("timeEdit_2")
        self.gridLayout_3.addWidget(self.timeEdit_2, 4, 4, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout_3.addWidget(self.radioButton_2, 3, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout_3.addWidget(self.doubleSpinBox, 0, 1, 1, 1)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.gridLayout_3.addWidget(self.doubleSpinBox_2, 0, 3, 1, 1)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.gridLayout_3.addWidget(self.doubleSpinBox_3, 0, 5, 1, 1)
        self.radioButton_3 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout_3.addWidget(self.radioButton_3, 3, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 3, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 2, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout_3.addWidget(self.radioButton, 3, 3, 1, 1)
        self.timeEdit = QtWidgets.QTimeEdit(self.tab_2)
        self.timeEdit.setMaximumTime(QtCore.QTime(20, 0, 0))
        self.timeEdit.setMinimumTime(QtCore.QTime(4, 0, 0))
        self.timeEdit.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
        self.timeEdit.setTimeSpec(QtCore.Qt.TimeZone)
        self.timeEdit.setObjectName("timeEdit")
        self.gridLayout_3.addWidget(self.timeEdit, 4, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 4, 0, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_3.addWidget(self.checkBox_2, 1, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_3.addWidget(self.checkBox, 1, 3, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 4, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Auto Trader"))
        self.label_5.setText(_translate("MainWindow", "Bar Type"))
        self.sel_all_button.setText(_translate("MainWindow", "Uncheck All"))
        self.label_4.setText(_translate("MainWindow", "Ticker selection:"))
        self.label_3.setText(_translate("MainWindow", "Trading list:"))
        self.strategy3_radio.setText(_translate("MainWindow", "Strategy 3"))
        self.strategy4_radio.setText(_translate("MainWindow", "Strategy 4"))
        self.strategy2_radio.setText(_translate("MainWindow", "Strategy 2"))
        self.stairstep_radio.setText(_translate("MainWindow", "StairStep Trading"))
        self.data_toggle_button.setText(_translate("MainWindow", "Track Data!"))
        self.load_model_button.setText(_translate("MainWindow", "Load Models"))
        self.perform_prep_button.setText(_translate("MainWindow", "Perform Preprocessing"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Running"))
        self.cancel_trades_button.setText(_translate("MainWindow", "Cancel All!"))
        self.trade_toggle_button.setText(_translate("MainWindow", "Trade!"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Active Trades"))
        self.radioButton_2.setText(_translate("MainWindow", "Up"))
        self.label_8.setText(_translate("MainWindow", "Profit Margin"))
        self.label_6.setText(_translate("MainWindow", "Open Margin"))
        self.radioButton_3.setText(_translate("MainWindow", "Down"))
        self.label.setText(_translate("MainWindow", "Direction:"))
        self.label_7.setText(_translate("MainWindow", "Stop loss Margin"))
        self.radioButton.setText(_translate("MainWindow", "Both"))
        self.label_2.setText(_translate("MainWindow", "Trading Window"))
        self.checkBox_2.setText(_translate("MainWindow", "Use limit"))
        self.checkBox.setText(_translate("MainWindow", "Use limit"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Strategy Params"))
