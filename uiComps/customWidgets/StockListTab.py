# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'optionsGraph.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5.QtGui import QBrush, QColor

from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QWidget
from uiComps.qtGeneration.StockListTab_UI import Ui_Form as StockTab

from generalFunctionality.UIFunctions import findRowForValue, getNumericItem, AlignDelegate, PriceAlignDelegate
from dataHandling.Constants import Constants



class StockListTab(QWidget):

    individual = False
    tab_name = ""
    text_updater = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        self.setupUi()
        self.setupAlignment()
        self.stock_table.setSortingEnabled(True)

        header = self.stock_table.horizontalHeader()
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)


    def setupUi(self):
        new_form = StockTab() 
        new_form.setupUi(self)
        self.getFormReferences(new_form)  

    def getFormReferences(self, new_form):
        self.stock_table = new_form.stock_table
        self.total_value_label = new_form.total_value_label
        self.unrealized_pnl_label = new_form.unrealized_pnl_label


    def setData(self, positions):

        self.stock_table.clearContents()
        self.stock_table.setRowCount(len(positions.index))
        
        index = 0
        total_mkt_value = 0.0
        unrealized_pnl = 0.0

        for _, position in positions.iterrows():
            
            mkt_value = position['PRICE'] * position['COUNT']
            
            self.stock_table.setItem(index, 0, QTableWidgetItem(position[Constants.SYMBOL]))
            self.stock_table.setItem(index, 1, getNumericItem(position['PRICE']))
            self.stock_table.setItem(index, 2, getNumericItem(position['COUNT']))
            self.stock_table.setItem(index, 3, getNumericItem(mkt_value))
            self.stock_table.setItem(index, 4, getNumericItem(position['UNREALIZED_PNL']))
            self.stock_table.setItem(index, 5, getNumericItem(position['DPNL']))

            if position['DPNL'] < 0:
                self.stock_table.item(index, 5).setForeground(QBrush(QColor(200, 0, 0)))
            elif position['DPNL'] > 0:
                self.stock_table.item(index, 5).setForeground(QBrush(QColor(0, 180, 0)))


            total_mkt_value += mkt_value
            unrealized_pnl += position['UNREALIZED_PNL']
            index +=1
            
        self.total_value_label.setText("{:.2f}".format(total_mkt_value))
        self.unrealized_pnl_label.setText("{:.2f}".format(unrealized_pnl))

    def setupAlignment(self):

        delegate = AlignDelegate(self.stock_table)
        num_delegate = PriceAlignDelegate(self.stock_table)
        self.stock_table.setItemDelegateForColumn(1, num_delegate)
        self.stock_table.setItemDelegateForColumn(2, delegate)
        self.stock_table.setItemDelegateForColumn(3, num_delegate)
        self.stock_table.setItemDelegateForColumn(4, num_delegate)
        self.stock_table.setItemDelegateForColumn(5, num_delegate)
        self.stock_table.setItemDelegateForColumn(6, num_delegate)   



class SelectableTabWidget(StockListTab):

    list_updater = pyqtSignal(str, dict)
    position_types = dict()
    split_counts = dict()

    def __init__(self):
        super().__init__()
        self.stock_table.insertColumn(0)
        self.stock_table.setHorizontalHeaderItem(0, QTableWidgetItem('Type'))
        self.stock_table.insertColumn(1)
        self.stock_table.setHorizontalHeaderItem(1, QTableWidgetItem('Invest Count'))
        self.stock_table.insertColumn(2)
        self.stock_table.setHorizontalHeaderItem(2, QTableWidgetItem('ID'))
        self.stock_table.insertColumn(9)
        self.stock_table.setHorizontalHeaderItem(9, QTableWidgetItem('Trade PP'))
        
        header = self.stock_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        

    def setupAlignment(self):

        delegate = AlignDelegate(self.stock_table)
        num_delegate = PriceAlignDelegate(self.stock_table)
        self.stock_table.setItemDelegateForColumn(4, num_delegate)
        self.stock_table.setItemDelegateForColumn(5, num_delegate)
        self.stock_table.setItemDelegateForColumn(6, num_delegate)   



    def setData(self, positions):

        self.stock_table.clearContents()
        self.stock_table.setRowCount(len(positions.index))
        
        index = 0

        for _, position in positions.iterrows():
            
            numeric_id = position['ID']
            widget, radio_group = self.getRadioButtonGroup(numeric_id)
            
            self.stock_table.setCellWidget(index, 0, widget)
            
            count_edit = self.getCountWidget(numeric_id)
            self.stock_table.setCellWidget(index, 1, count_edit)

            self.stock_table.setItem(index, 2, QTableWidgetItem(numeric_id))
            self.stock_table.setItem(index, 3, QTableWidgetItem(position[Constants.SYMBOL]))
            self.stock_table.setItem(index, 5, getNumericItem(position['COUNT']))

            price_edit = self.getPriceWidget(numeric_id)
            self.stock_table.setCellWidget(index, 9, price_edit)

            index +=1

        self.stock_table.resizeRowsToContents()

    def getCountWidget(self, numeric_id):
        count_edit = QtWidgets.QLineEdit()
        count_edit.setEnabled(self.position_types[numeric_id] == "Split")
        count_edit.setAlignment(QtCore.Qt.AlignRight)  
        count_edit.setObjectName(numeric_id)
        count_edit.setPlaceholderText("0")
        if numeric_id in self.split_counts:
            count_edit.setText(str(self.split_counts[numeric_id]))
        count_edit.textChanged.connect(lambda text: self.splitUpdate(text, numeric_id))
        return count_edit        


    def getPriceWidget(self, numeric_id):
        price_edit = QtWidgets.QLineEdit()
        price_edit.setEnabled(self.position_types[numeric_id] == "Split")
        price_edit.setAlignment(QtCore.Qt.AlignRight)  
        price_edit.setObjectName(numeric_id)
        price_edit.setPlaceholderText("0.0")
        if numeric_id in self.purchase_price:
            price_edit.setText(str(self.purchase_price[numeric_id]))
        price_edit.textChanged.connect(lambda text: self.purchasePriceUpdate(text, numeric_id))
        return price_edit        


    def splitUpdate(self, text, numeric_id):
        self.split_counts[numeric_id] = int(text)
        self.list_updater.emit(Constants.LIST_SELECTION_UPDATE, dict())


    def purchasePriceUpdate(self, text, numeric_id):
        self.purchase_price[numeric_id] = float(text)
        self.list_updater.emit(Constants.LIST_SELECTION_UPDATE, dict())


    def typeSelection(self, button, selection, numeric_id):
        if selection:
            self.position_types[numeric_id] = button.text()
            self.list_updater.emit(Constants.LIST_SELECTION_UPDATE, dict())

            if button.text() == "Split":
                index = findRowForValue(self.stock_table, numeric_id, 2)
                line_edit = self.stock_table.cellWidget(index, 1)
                line_edit.setEnabled(True)
        

    def selectButton(self, id, group):
        for button in group.buttons():
            button.setChecked(button.text() == id)


    def getRadioButtonGroup(self, numeric_id):
        layout = QtWidgets.QHBoxLayout()
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        radio_group = QtWidgets.QButtonGroup(widget)
        r_trade = QtWidgets.QRadioButton("Trade")
        radio_group.addButton(r_trade)
        r_split = QtWidgets.QRadioButton("Split")
        radio_group.addButton(r_split)
        r_invest = QtWidgets.QRadioButton("Invest")
        radio_group.addButton(r_invest)

        self.selectButton(self.position_types[numeric_id], radio_group)
        radio_group.buttonToggled.connect(lambda button, selection: self.typeSelection(button, selection, numeric_id))

        layout.addWidget(r_trade)
        layout.addWidget(r_split)
        layout.addWidget(r_invest)

        radio_group.setObjectName(numeric_id)
        widget.setObjectName(numeric_id)

        return widget, radio_group

    # def selectionChange(self, value):
    #     self.selected_ids = []
    #     for row in range(self.options_table.rowCount()):
    #         checkbox = self.options_table.cellWidget(row, 0)
    #         if checkbox.isChecked():
    #             self.selected_ids.append(int(self.options_table.item(row, 1).text()))

        self.list_updater.emit(Constants.LIST_SELECTION_UPDATE, dict())
