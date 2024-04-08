
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

# Form implementation generated from reading ui file 'optionsGraph.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
import numpy as np
from dataHandling.Constants import Constants, OptionConstrType
from dataHandling.DataStructures import DetailObject
from .VisualizationWindow import VisualizationWindow
import pandas as pd


def floatFromString(str_flt, default=0.0):
    try:
        return float(str_flt)
    except ValueError:
        return default


class OptionVisualization(VisualizationWindow):

    option_type = Constants.CALL
    order_type = Constants.BUY
    constr_type = OptionConstrType.single
    first_price = False

    current_selection = None

    last_price = None
    _underlying_price = None

    reqAllStrikesSignal = pyqtSignal(list)
    make_selection_signal = pyqtSignal(DetailObject)

    reqByStrike = pyqtSignal(float, bool)
    reqByStrikeAutoExecute = pyqtSignal(float)
    reqByExp = pyqtSignal(str, bool)
    reqByExpAutoExecute = pyqtSignal(str)


    min_strike_signal = pyqtSignal(float)
    max_strike_signal = pyqtSignal(float)
    min_expiration_signal = pyqtSignal(int)
    max_expiration_signal = pyqtSignal(int)


    constr_change_signal = pyqtSignal(str, str, str, list, list)


    def __init__(self, option_data_manager, symbol_manager):
        super().__init__()

        print(f"OptionVisualization.__init__ init {int(QThread.currentThreadId())}")
        self.option_data_manager = option_data_manager
        self.symbol_manager = symbol_manager
        
        self.connectOptionManager(option_data_manager)
    
        self.symbol_manager.api_updater.connect(self.contractUpdate, Qt.QueuedConnection)


        self.connectSignals()
        self.resetInputBoxes(self.constr_type)
        # self.setDefaults(self.option_type)
        

    def connectOptionManager(self, option_data_manager):
        option_data_manager.api_updater.connect(self.apiUpdate, Qt.QueuedConnection)
        self.strike_comp_frame = self.option_data_manager.strike_comp_frame #ComputableStrikeFrame(None, self.option_type)
        self.strike_comp_frame.frame_updater.connect(self.processingUpdate, Qt.QueuedConnection)
        self.exp_comp_frame = option_data_manager.exp_comp_frame #ComputableExpirationFrame(None, self.option_type)
        self.exp_comp_frame.frame_updater.connect(self.processingUpdate, Qt.QueuedConnection)
        self.all_option_frame = option_data_manager.getBufferedFrame()   #Computable2DDataFrame(None, self.option_type)
        self.all_option_frame.connectCallback(self.processingUpdate)


    def connectSignals(self):
        self.make_selection_signal.connect(self.option_data_manager.makeStockSelection, type=Qt.QueuedConnection)
        self.reqAllStrikesSignal.connect(self.option_data_manager.requestForAllStrikesAndExpirations, type=Qt.QueuedConnection)
        self.reqByStrike.connect(self.option_data_manager.requestOptionDataForStrike, type=Qt.QueuedConnection)
        self.reqByStrikeAutoExecute.connect(self.option_data_manager.requestOptionDataForStrike, type=Qt.QueuedConnection)

        self.reqByExp.connect(self.option_data_manager.requestOptionDataForExpiration, type=Qt.QueuedConnection)
        self.reqByExpAutoExecute.connect(self.option_data_manager.requestOptionDataForExpiration, type=Qt.QueuedConnection)

        self.min_strike_signal.connect(self.option_data_manager.setMinimumStrike, type=Qt.QueuedConnection)
        self.max_strike_signal.connect(self.option_data_manager.setMaximumStrike, type=Qt.QueuedConnection)
        self.min_expiration_signal.connect(self.option_data_manager.setMinimumExpiration, type=Qt.QueuedConnection)
        self.max_expiration_signal.connect(self.option_data_manager.setMaximumExpiration, type=Qt.QueuedConnection)

        self.flush_button.clicked.connect(self.option_data_manager.flushData, type=Qt.QueuedConnection)
        self.reset_button.clicked.connect(self.option_data_manager.resetWholeChain, type=Qt.QueuedConnection)

        self.constr_change_signal.connect(self.option_data_manager.structureSelectionChanged, type=Qt.QueuedConnection)
        

    def structureSelectionChanged(self, value):
        self.constr_type = OptionConstrType(value)
        self.resetInputBoxes(self.constr_type)
        self.constructionPropsChange()


    def resetInputBoxes(self, constr_type):        
        self.setOffsetDefaults(constr_type)
        self.setRatioDefaults(constr_type)
        

    def getCurrentOffsets(self):
        upper_offset = floatFromString(self.upper_offset_box.currentText(), default=0.0)
        lower_offset = floatFromString(self.upper_offset_box.currentText(), default=0.0)
        return [upper_offset, lower_offset]


    def getCurrentRatios(self):
        base_ratio = self.base_ratio_box.value()
        upper_ratio = self.upper_ratio_box.value()
        lower_ratio = self.lower_ratio_box.value()
        return [base_ratio, upper_ratio, lower_ratio]


    def findPrefferedOffset(self, strike_diffs, preferred_values):
        for value in preferred_values:
            index = np.where(strike_diffs == value)
            if len(index[0]) > 0:
                return (index[0][0], value)
        return None


    def getStrikeDifferences(self):
        active_strikes = self.all_option_frame.getAvailableStrikes().values
        strike_diffs = (active_strikes[:, None] - active_strikes).ravel()
        strike_diffs = np.unique(np.abs(strike_diffs))
        strike_diffs = strike_diffs[strike_diffs > 0]
        strike_diffs_str = [str(val) for val in strike_diffs]
        return strike_diffs, strike_diffs_str


    def setOffsetDefaults(self, constr_type):
        self.upper_offset_box.blockSignals(True)
        self.lower_offset_box.blockSignals(True)
    
        self.upper_offset_box.clear()
        self.upper_offset_box.setEnabled(False)
        self.lower_offset_box.setEnabled(False)
        if constr_type != OptionConstrType.single:
            strike_diffs, strike_diffs_str = self.getStrikeDifferences()
            self.upper_offset_box.addItems(strike_diffs_str)
            self.upper_offset_box.setEnabled(True)
            
            pref_pair = None
            if constr_type == OptionConstrType.vertical_spread or constr_type == OptionConstrType.iron_condor:
                preffered_diffs = Constants.PREFFERED_DIFFS_SMALL
                pref_pair = self.findPrefferedOffset(strike_diffs, preffered_diffs)
            elif constr_type == OptionConstrType.butterfly:
                preffered_diffs = Constants.PREFFERED_DIFFS_LARGE
                pref_pair = self.findPrefferedOffset(strike_diffs, preffered_diffs)

            if pref_pair is not None:
                self.upper_offset_box.setCurrentIndex(pref_pair[0])    
            
            if (constr_type == OptionConstrType.iron_condor) or (constr_type == OptionConstrType.split_butterfly):
                self.lower_offset_box.setEnabled(True)
                self.lower_offset_box.addItems(strike_diffs_str)
                if pref_pair is not None:
                    self.lower_offset_box.setCurrentIndex(pref_pair[0])

        self.upper_offset_box.blockSignals(False)
        self.lower_offset_box.blockSignals(False)
        


    def setRatioDefaults(self, constr_type):
        
        self.upper_ratio_box.blockSignals(True)
        self.base_ratio_box.blockSignals(True)
        self.lower_ratio_box.blockSignals(True)
        

        if constr_type == OptionConstrType.butterfly:
            ratios = [1,2,1]
        else:
            ratios = [1,1,1]

        self.upper_ratio_box.setEnabled(False)
        self.lower_ratio_box.setEnabled(False)
        if constr_type != OptionConstrType.single:
            self.upper_ratio_box.setEnabled(True)
            self.lower_ratio_box.setEnabled(True)
        
        self.upper_ratio_box.setValue(ratios[0])
        self.base_ratio_box.setValue(ratios[1])
        self.lower_ratio_box.setValue(ratios[2])
        self.upper_ratio_box.blockSignals(False)
        self.base_ratio_box.blockSignals(False)
        self.lower_ratio_box.blockSignals(False)
        


    def radioAllSelection(self, value):
        if self.premium_a_radio.isChecked():
            self.all_option_frame.setPriceType('premium')
        elif self.price_a_radio.isChecked():
            self.all_option_frame.setPriceType('price')
        elif self.rel_premium_a_radio.isChecked():
            self.all_option_frame.setPriceType('relative premium')
                                
        
    def radioStrikeSelection(self, value):
        if self.premium_s_radio.isChecked():
            #self.strike_comp_frame.setPremium(True)
            self.strike_plot.setPremium(True)
            pass
        elif self.price_s_radio.isChecked():
            #self.strike_comp_frame.setPremium(False)
            self.strike_plot.setPremium(False)
        #self.strike_plot.updatePlot(self.strike_comp_frame)
        


    def snapshotChange(self, value):
        self.option_data_manager.snapshot = value


    def selectedContract(self, contractDetails):
        self.symbol_label.setText(contractDetails.long_name + ' (' + contractDetails.exchange + ')')
        self.current_selection = contractDetails
            

    def returnSelection(self):
        if self.current_selection is not None:
            self.make_selection_signal.emit(self.current_selection)
            self.first_price = True
            self.updateOptionGUI([],[])
            self.current_selection = None


    @pyqtSlot(str, dict)
    def apiUpdate(self, signal, sub_signal):
        #print(f"OptionVisualization.apiUpdate: {signal}")
        if signal == Constants.OPTION_INFO_LOADED:
            self.updateOptionGUI(sub_signal['expirations'], sub_signal['strikes'])
        elif signal == Constants.OPTION_PRICE_UPDATE:
            pd.set_option('display.max_rows', None)
            if 'strike_frame' in sub_signal:
                self.processNewStrikeData(sub_signal['strike_frame'])
            if 'expiration_frame' in sub_signal:
                self.processNewExpData(sub_signal['expiration_frame'])
        elif signal == Constants.OPTIONS_LOADED:
            self.fetch_all_button.setEnabled(True)
#            self.strike_plot.setStrikeLine(self._underlying_price)
            self.setGUIValues(self.all_option_frame.getBoundaries())
        elif signal == Constants.PROGRESS_UPDATE:
            if sub_signal['open_requests'] == 0:
                self.statusbar.showMessage(f"All {sub_signal['request_type']} requests completed")
            else:
                self.statusbar.showMessage(f"{sub_signal['open_requests']} of {sub_signal['total_requests']} {sub_signal['request_type']} requests left")

        elif signal == Constants.UNDERLYING_PRICE_UPDATE:
            if self.first_price:
                self.strike_plot.addPriceLine()
            self.updatePrice(sub_signal['price'])
            if self.first_price:
                self.first_price = False
        

    def findClosest(self, value, element_list):
        np_list = np.array(element_list)
        index = np.abs(np_list - value).argmin()
        return np_list[index]


    @pyqtSlot(str, dict)
    def processingUpdate(self, signal, sub_signal):
        print(f"What be goin' on? {sub_signal}")
        if signal == Constants.DATA_DID_CHANGE:

            if sub_signal['key'] == '2D_frame':
                self.strike_grouped_plot.resetData(self.all_option_frame)
                self.exp_grouped_plot.resetData(self.all_option_frame)
                self.price_est_plot.resetData(self.all_option_frame)

            
            if sub_signal['key'] == '1D_frame':
                self.strike_plot.updatePlot(self.strike_comp_frame)
                self.expiration_plot.updatePlot(self.exp_comp_frame)
    
        
    def requestLiveUpdates(self, current_selection):
        print(f"OptionVisualization requestLiveUpdates {int(QThread.currentThreadId())}")
        print(self.expiration_pairs)
        dates_by_days = {item[0]: item[2] for item in self.expiration_pairs}
        if current_selection['plot_type'] == 'expiration_grouped':
            self.reqByExp.emit(dates_by_days[current_selection['key']], False)
            self.reqByStrikeAutoExecute.emit(current_selection['x_value'])
            self.plot_widget.setCurrentIndex(3)
        elif current_selection['plot_type'] == 'strike_grouped':
            self.reqByExp.emit(dates_by_days[current_selection['x_value']], False)
            self.reqByStrikeAutoExecute.emit(current_selection['key'])
            self.plot_widget.setCurrentIndex(3)
        

    def requestPL(self, current_selection):
        print(f"We want to showPL {current_selection}")
        self.plot_widget.setCurrentIndex(4)
        self.all_option_frame.setSelectedStrike(current_selection['x_value'], current_selection['key'], current_selection['y_value'])
    

    def updatePrice(self, price):
        self._underlying_price = price
        if self.last_price is not None:
            if self.last_price > price:
                self.price_label.setText('<font color="red">' + str(price) + '</font>')
            else:
                self.price_label.setText('<font color="green">' + str(price) + '</font>')
        else:
            self.price_label.setText(str(price))

        self.last_price = price
        self.updatePlotPrice(price)


    def expirationSelectionChange(self, value):
        print("Same here akdslmfalkdmf")
        self.option_data_manager.updateExpirationSelection(value)


    def updateStrikeSelection(self, selected_strike):
        print("Who should control the strike selection?")
        self.selected_strike = selected_strike
        # # self.base_selection_box.setStrike(selected_strike)
        # # base_index = self.base_selection_box.findText(str(selected_strike), QtCore.Qt.MatchFixedString)
        # # if base_index >= 0:
        # #     self.base_selection_box.setCurrentIndex(base_index)
        
        # offsets = self.option_data_manager.getStrikes() - selected_strike
        # self.offset_selection_box.clear()
        # self.offset_selection_box.addItems(map(str, offsets))
        # offset_index = self.offset_selection_box.findText(str("0.0"), QtCore.Qt.MatchFixedString)

        # self.offset_selection_box.setCurrentIndex(offset_index)

        # offset = float(self.offset_selection_box.currentText())
        # if self.option_type == OptionConstrType.vertical_spread and offset != 0:
        #     self.option_data_manager.requestSpreadsDataByExp(self.selected_strike, offset)
        # else:
        


    def strikePriceChange(self, value):
        print(f"This one is triggered {value} and thus screwing things up")
        #self.strike_plot.setStrikeLine(float(value))


    def constructionPropsChange(self):
        self.constr_change_signal.emit(self.option_type, self.order_type, self.constr_type.value, self.getCurrentOffsets(), self.getCurrentRatios())
            

    def fetchAllStrikes(self):
        self.fetch_all_button.setEnabled(False)
        option_types = []
        if self.call_selection.isChecked():
            option_types.append(Constants.CALL)
        if self.put_selection.isChecked():
            option_types.append(Constants.PUT)
        self.reqAllStrikesSignal.emit(option_types)


    def callPutAction(self, value):
        if value == self.put_radio: new_type = Constants.PUT
        if value == self.call_radio: new_type = Constants.CALL
        if new_type != self.option_type:
            self.option_type = new_type
            self.constructionPropsChange()
            
 
    
    def buySellAction(self, value):
        if value == self.buy_radio:
            self.order_type = Constants.BUY
            self.constructionPropsChange()
        elif value == self.sell_radio:
            self.order_type = Constants.SELL
            self.constructionPropsChange()


        #TODO this should be in super
    def accepts(self, value):
        return False




    # def processNewStrikeData(self, strike_frame):
    #     self.strike_comp_frame.setData(strike_frame.copy())
    #     self.strike_comp_frame.setUnderlyingPrice(self._underlying_price)
    #     if self.strike_comp_frame.has_data:
            
            


    # def processNewExpData(self, expiration_frame):
    #     self.exp_comp_frame.setData(expiration_frame.copy())
    #     self.exp_comp_frame.setUnderlyingPrice(self._underlying_price)
    #     if self.exp_comp_frame.has_data:
    #         self.expiration_plot.updatePlot(self.exp_comp_frame)
    

    # def processAllData(self, all_frame):
    #     print("OptionVisualization.processAllData")
    #     self.all_option_frame.setUnderlyingPrice(self._underlying_price)
    #     self.all_option_frame.setData(all_frame.copy())
        