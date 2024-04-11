
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

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QThread
from PyQt5.QtWidgets import QMainWindow, QAbstractButton, QTableView
from dataHandling.Constants import Constants
from .OrderDataModel import OrderDataModel, StairDataModel, SpinBoxDelegate, ButtonDelegate, CheckBoxDelegate
from .TradingWindow import TradingWindow

from ibapi.contract import Contract

from .TickerProcessor import LiveTickerProcessor

from dataHandling.UserDataManagement import readStockList, getStockListNames


class TradeMaker(TradingWindow):
    
    latest_bid = 0
    latest_ask = 0
    latest_trade = 0

    is_tracking_steps = False
    fields_need_updating = True

    cancel_all_signal = pyqtSignal()
    cancel_order_by_row = pyqtSignal(int)
    cancel_stair_by_row = pyqtSignal(int)
    set_ticker_signal = pyqtSignal(tuple, set)
    step_prop_update_signal = pyqtSignal(dict)
    set_bar_signal = pyqtSignal(str)
    place_complex_signal = pyqtSignal(Contract, str, int, float, dict)
    place_combo_signal = pyqtSignal(Contract, str, int, float, float, float)
    place_stair_order = pyqtSignal(Contract, str, str)
    kill_stair_order = pyqtSignal()


    def __init__(self, order_manager, history_manager, symbol_manager):
        super().__init__()
        self.loadStockLists()
        self.order_manager = order_manager
        self.history_manager = history_manager
        self.symbol_manager = symbol_manager

        self.data_buffers = history_manager.getDataBuffer()
        self.history_manager.api_updater.connect(self.apiUpdate)
        self.history_manager.mostRecentFirst = True
        self.symbol_manager.api_updater.connect(self.contractUpdate, Qt.QueuedConnection)

        self.order_buffer = self.order_manager.getOrderBuffer()
        self.stair_tracker = self.order_manager.getStairTracker()
        self.order_manager.setDataObject(self.data_buffers)
        
        self.prepTickerProcessor(history_manager)
        self.setupOrderTable(self.order_buffer)
        self.setupStairTable(self.stair_tracker)
        self.setBaseGuiValues()

        
        self.connectSignalSlots()
        
        self.product_label.setText(self.stock_list[self.selected_key]['long_name']) 
        
    
        # self.order_manager.open_order_request.emit()
        self.tickerSelection(0)
        self.processor_thread.start()


    def setupStairTable(self, stair_tracker):

        column_headers = ['Name', 'Action', 'Count', 'Trigger', 'Limit', 'Stopping']
        self.step_prop_update_signal.connect(stair_tracker.updateCurrentStepProperty, Qt.QueuedConnection)

        self.step_checkbox_delegate = CheckBoxDelegate(self.step_order_table)
        # self.step_checkbox_delegate.check_click_signal.connect(self.stairCheck, Qt.QueuedConnection)
        self.step_order_table.setItemDelegate(self.step_checkbox_delegate)

        self.step_stop_delegate = ButtonDelegate('Stop Tracking' ,self.step_order_table)
        self.step_stop_delegate.button_click_signal.connect(self.stopTrackingStair)
        self.step_order_table.setItemDelegateForColumn(4, self.step_stop_delegate)

        self.step_int_spin_box_delegate = SpinBoxDelegate('int_spin_box')
        self.step_double_spin_box_delegate = SpinBoxDelegate('double_spin_box')
        self.step_order_table.setItemDelegateForColumn(column_headers.index('Count'), self.step_int_spin_box_delegate)
        self.step_order_table.setItemDelegateForColumn(column_headers.index('Trigger'), self.step_double_spin_box_delegate)
        self.step_order_table.setItemDelegateForColumn(column_headers.index('Limit'), self.step_double_spin_box_delegate)

        self.stair_model = StairDataModel(stair_tracker, column_headers)
        self.stair_model.stair_edit_update.connect(stair_tracker.updateStepProperty, Qt.QueuedConnection)
        self.step_order_table.setSelectionMode(QTableView.NoSelection)
        self.step_order_table.setModel(self.stair_model)


    def setupOrderTable(self, order_buffer):
        column_headers = ['Order ID', 'Symbol', 'Action', 'Count', 'Limit', 'Stop level', 'Status']
        self.int_spin_box_delegate = SpinBoxDelegate('int_spin_box')
        self.double_spin_box_delegate = SpinBoxDelegate('double_spin_box')
        self.order_table.setItemDelegateForColumn(column_headers.index('Count'), self.int_spin_box_delegate)
        self.order_table.setItemDelegateForColumn(column_headers.index('Limit'), self.double_spin_box_delegate)
        self.order_table.setItemDelegateForColumn(column_headers.index('Stop level'), self.double_spin_box_delegate)
        
        self.cancel_delegate = ButtonDelegate('Cancel' ,self.order_table)
        self.cancel_delegate.button_click_signal.connect(self.cancelOrderByRow)
        self.order_table.setItemDelegateForColumn(len(column_headers), self.cancel_delegate)

        self.order_model = OrderDataModel(order_buffer, column_headers)
        self.order_model.order_edit_update.connect(self.order_manager.orderEdit, Qt.QueuedConnection)
        self.order_table.setModel(self.order_model)


    def prepTickerProcessor(self, history_manager):
        self.selected_key = next(iter(self.stock_list))
        self.selected_symbol = self.stock_list[self.selected_key][Constants.SYMBOL]
        self.data_processor = LiveTickerProcessor(history_manager)
        self.processor_thread = QThread()
        self.data_processor.moveToThread(self.processor_thread)
        self.processor_thread.started.connect(self.data_processor.run)
        

    def connectSignalSlots(self):
        self.data_processor.data_updater.connect(self.dataUpdate, Qt.QueuedConnection)

        self.set_ticker_signal.connect(self.data_processor.setTicker, Qt.QueuedConnection)
        self.set_bar_signal.connect(self.data_processor.setBarType, Qt.QueuedConnection)
        self.cancel_all_signal.connect(self.order_manager.cancelAllOrders, Qt.QueuedConnection)
        self.cancel_order_by_row.connect(self.order_manager.cancelOrderByRow, Qt.QueuedConnection)
        self.cancel_stair_by_row.connect(self.order_manager.cancelStairByRow, Qt.QueuedConnection)
        self.place_complex_signal.connect(self.order_manager.placeOrder, Qt.QueuedConnection)
        self.place_combo_signal.connect(self.order_manager.placeOcoOrder, Qt.QueuedConnection)
        self.place_stair_order.connect(self.order_manager.openStairTrade, Qt.QueuedConnection)
        self.kill_stair_order.connect(self.order_manager.killStairTrade, Qt.QueuedConnection)

        self.stair_tracker.tracking_updater.connect(self.trackingUpdate, Qt.QueuedConnection)
        


    @pyqtSlot(str, dict)
    def apiUpdate(self, signal, sub_signal):
        if signal == Constants.UNDERLYING_PRICE_UPDATE:
            if sub_signal['type'] == Constants.ASK:
                self.ask_price_button.setText(str(sub_signal['price']))
                self.latest_ask = sub_signal['price']
            elif sub_signal['type'] == Constants.LAST:
                self.last_price_button.setText(str(sub_signal['price']))
                self.latest_trade = sub_signal['price']
                self.price_label.setText(str(sub_signal['price']))
            elif sub_signal['type'] == Constants.BID:
                self.bid_price_button.setText(str(sub_signal['price']))
                self.latest_bid = sub_signal['price']
    

    def checkIfStairTradable(self):
        if self.is_tracking_steps:
            self.step_button.setEnabled(True)
        elif self.data_buffers.bufferExists(self.selected_key, self.selected_bar_type):
            last_two_bars = self.data_buffers.getBarsFromIntIndex(self.selected_key, self.selected_bar_type, -2)
            if self.step_action_type == Constants.BUY and (last_two_bars.iloc[0][Constants.HIGH] < last_two_bars.iloc[1][Constants.HIGH]):
                self.step_button.setEnabled(False)
            elif self.step_action_type == Constants.SELL and (last_two_bars.iloc[1][Constants.LOW] < last_two_bars.iloc[0][Constants.LOW]):
                self.step_button.setEnabled(False)
            else:
                self.step_button.setEnabled(True)


    @pyqtSlot(str, dict)
    def dataUpdate(self, signal, sub_signal):
        if (self.selected_key == sub_signal['uid']) and (self.selected_bar_type in sub_signal['bars']):
            if signal == Constants.HISTORICAL_DATA_READY:
                if self.data_buffers.bufferExists(self.selected_key, self.selected_bar_type):
                    bars = self.data_buffers.getBufferFor(self.selected_key, self.selected_bar_type)
                    self.trade_plot.setHistoricalData(bars.iloc[:-1])
                    self.trade_plot.addNewBars(bars.iloc[[-1]], bars.index[-1])
                    if self.fields_need_updating:
                        self.fillOutPriceFields(include_profit_loss=True)
                        self.fields_need_updating = False
            elif signal == Constants.HAS_NEW_DATA:
                if self.data_buffers.bufferExists(self.selected_key, self.selected_bar_type):
                    if self.selected_bar_type in sub_signal['updated_from']:
                        from_index = sub_signal['updated_from'][self.selected_bar_type]
                        bars = self.data_buffers.getBarsFromLabelIndex(self.selected_key, self.selected_bar_type, from_index)
                        if self.tab_widget.tabText(self.tab_widget.currentIndex()) == "Stairstep":
                            self.checkIfStairTradable()

                        self.trade_plot.addNewBars(bars, from_index)


    def selectedContract(self, contractDetails):
        self.current_selection = contractDetails
            

    def cancelOrderByRow(self, row_index):
        self.cancel_order_by_row.emit(row_index)


    def stopTrackingStair(self, row_index):
        self.cancel_stair_by_row.emit(row_index)


    def stairCheck(self, row_index):
        print(f"TradeMaker.stairCheck {row_index}")


    def returnSelection(self):
        if self.current_selection is not None:
            self.selected_key = str(self.current_selection.numeric_id)
            self.selected_symbol = self.current_selection.symbol
            stock_inf = {Constants.SYMBOL: self.current_selection.symbol, 'long_name': self.current_selection.long_name, 'exchange': self.current_selection.exchange, 'sec_type': self.symbol_manager.sec_type, 'currency': self.current_selection.currency}
            self.product_label.setText(self.current_selection.long_name)
            self.set_ticker_signal.emit((self.selected_key, stock_inf), self.getActiveUids())
            self.checkTracking()
            self.fields_need_updating = True
            self.stair_tracker.propagate_to_current = False


    def tickerSelection(self, value):
        print("TradeMaker.tickerSelection do we get here early?")
        ordered_keys = list(self.stock_list.keys())
        self.selected_key = ordered_keys[value]
        self.selected_symbol = self.stock_list[self.selected_key][Constants.SYMBOL]
        self.product_label.setText(self.stock_list[self.selected_key]['long_name'])
        self.set_ticker_signal.emit((self.selected_key, self.stock_list[self.selected_key]), self.getActiveUids())
        self.checkTracking()
        self.fields_need_updating = True
        self.stair_tracker.propagate_to_current = False


    def checkTracking(self):
        if (self.selected_key, self.selected_bar_type) in self.stair_tracker.getActiveKeys():
            self.trackingUpdate("Stair Opened", {'uid': self.selected_key, 'bar_type': self.selected_bar_type})

    @pyqtSlot(str, dict)
    def trackingUpdate(self, signal, sub_signal):
        if signal == "Stair Opened":
            self.step_button.setText("Cancel Track")
            self.is_tracking_steps = True
        elif signal == "Stair Killed":
            self.step_button.setText("Open Stair")
            self.is_tracking_steps = False


    def getActiveUids(self):
        active_keys = self.stair_tracker.getActiveKeys()
        return set([uid for uid, _ in active_keys])
        

    def barSelection(self, new_bar_type):
        self.step_bar_label.setText(new_bar_type)
        self.selected_bar_type = new_bar_type
        self.set_bar_signal.emit(new_bar_type)
        self.checkTracking()
        self.stair_tracker.propagate_to_current = False


    def cancelAllTrades(self):
        self.cancel_all_signal.emit()


    def loadStockLists(self):
        self.stock_lists = getStockListNames()
        self.list_selector.blockSignals(True)
        for _, list_name in self.stock_lists:
            self.list_selector.addItem(list_name)
        self.list_selector.blockSignals(False)
        self.loadNewStockList(0)


    def listSelectionChange(self, radio_button):
        if radio_button == self.list_radio:
            self.setEnablingForLayout(self.list_layout, True, self.list_radio)
            self.setEnablingForLayout(self.symbol_layout, False, self.symbol_radio)
        elif radio_button == self.symbol_radio:
            self.setEnablingForLayout(self.list_layout, False, self.list_radio)
            self.setEnablingForLayout(self.symbol_layout, True, self.symbol_radio)
            

    def setEnablingForLayout(self, layout, enabled, exception):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() and item.widget() != exception:
                item.widget().setEnabled(enabled)


    def resetTickerList(self):
        self.ticker_selection.blockSignals(True)
        self.ticker_selection.clear()
        for uid, stock_inf in self.stock_list.items():
            self.ticker_selection.addItem(stock_inf[Constants.SYMBOL])
        self.ticker_selection.blockSignals(False)


    @pyqtSlot(bool)
    def makeMarket(self, checked):
        print(f"TradeMaker.makeMarket {checked}")
        self.market_ordering = checked


    def loadNewStockList(self, index):            
        self.stock_list = self.getStockList(index)
        self.resetTickerList()


    def getStockList(self, for_index):            
            file_name, _ = self.stock_lists[for_index]

            if file_name is not None:
                return readStockList(file_name)
            
            return []


    def listSelection(self, value):
        self.loadNewStockList(value)


    def getCurrentContract(self):
        contract = Contract()
        contract.symbol = self.selected_symbol
        contract.secType = Constants.STOCK
        contract.conId = self.selected_key
        contract.exchange = "SMART"
        return contract


#############################

    def placeOrder(self):
        contract = self.getCurrentContract()
        action = self.action_type
        count = self.count_field.value()
        limit_price = float(self.limit_field.text())

        close_dict = dict()
        if self.profit_take_on:
            close_dict['profit_limit'] = float(self.profit_limit_field.text()) 
        if self.stop_loss_on:
            close_dict['stop_trigger'] = float(self.stop_trigger_field.text()) 
            close_dict['stop_limit'] = float(self.stop_limit_field.text()) 

        self.place_complex_signal.emit(contract, action, count, limit_price, close_dict)
        

    def placeOcoOrder(self):
        contract = self.getCurrentContract()
        action = self.combo_action_type
        count = self.count_field.value()
        profit_limit = float(self.combo_limit_field.text())
        stop_trigger = float(self.combo_sl_trigger_field.text())
        stop_limit = float(self.combo_stop_limit_field.text()) if self.combo_sl_check.isChecked() else None
        self.place_combo_signal.emit(contract, action, count, profit_limit, stop_trigger, stop_limit)
        

    def placeStepOrder(self):
        if not self.is_tracking_steps:
            contract = self.getCurrentContract()
            action = self.step_action_type
            self.place_stair_order.emit(contract, action, self.selected_bar_type)
            self.stair_tracker.propagate_to_current = True
        else:
            self.order_manager.killStairTrade()

    
###################### level autosetting

    def setLevelsFromChart(self, high_low, price_level):

        price_margin = 0.1
        tab_name = self.tab_widget.tabText(self.tab_widget.currentIndex())

        print(f"TradeMaker.setLevels for {tab_name}")

        if tab_name == "General Order":
            if self.action_type == Constants.BUY and high_low == Constants.HIGH:
                self.profit_limit_field.setValue(price_level)
                self.profit_take_check.setChecked(True)
            elif self.action_type == Constants.BUY and high_low == Constants.LOW:
                self.stop_trigger_field.setValue(price_level-price_margin)
                self.stop_limit_field.setValue(price_level-(price_margin*2))
                self.stop_loss_check.setChecked(True)
                self.stop_limit_check.setChecked(True)
            elif self.action_type == Constants.SELL and high_low == Constants.HIGH:
                self.stop_trigger_field.setValue(price_level+price_margin)
                self.stop_limit_field.setValue(price_level+(price_margin*2))
                self.stop_loss_check.setChecked(True)
                self.stop_limit_check.setChecked(True)
            elif self.action_type == Constants.SELL and high_low == Constants.LOW:
                self.profit_limit_field.setValue(price_level)
                self.profit_take_check.setChecked(True)
        elif tab_name == "OCO":
            if self.combo_action_type == Constants.SELL and high_low == Constants.HIGH:
                self.combo_limit_field.setValue(price_level-price_margin)
            elif self.combo_action_type == Constants.SELL and high_low == Constants.LOW:
                self.combo_sl_trigger_field.setValue(price_level-price_margin)
                self.combo_stop_limit_field.setValue(price_level-(price_margin*2))
            elif self.combo_action_type == Constants.BUY and high_low == Constants.HIGH:
                self.combo_sl_trigger_field.setValue(price_level+price_margin)
                self.combo_stop_limit_field.setValue(price_level+(price_margin*2))
            elif self.combo_action_type == Constants.BUY and high_low == Constants.LOW:
                self.combo_limit_field.setValue(price_level+price_margin)
        elif tab_name == "Stairstep":
            self.step_profit_price_spin.setValue(price_level)
            self.step_profit_price_radio.setChecked(True)


    def fillOutPriceFields(self, button=None, include_profit_loss=False):
        print("TradeMaker.fillOutPriceFields")
        if button == self.ask_price_button:
            limit_price = self.latest_ask
        elif button == self.bid_price_button:
            limit_price = self.latest_bid
        else:
            limit_price = self.latest_trade
        
        self.limit_field.setValue(limit_price)

        if include_profit_loss:
            if self.action_type == Constants.BUY:
                price_offset = 1
            else:
                price_offset = -1
            
            self.profit_limit_field.setValue(limit_price+price_offset)
            self.stop_trigger_field.setValue(limit_price-price_offset)
            self.stop_limit_field.setValue(limit_price-(price_offset*2))

            self.combo_limit_field.setValue(limit_price+price_offset)
            self.combo_sl_trigger_field.setValue(limit_price-price_offset)
            self.combo_stop_limit_field.setValue(limit_price-(price_offset*2))
        

    @pyqtSlot(QAbstractButton, bool)
    def buySellSelection(self, button, value):
        print("TradeMaker.buySellSelection")
        if button == self.buy_radio and value:
            self.action_type = Constants.BUY
            self.combo_sell_radio.setChecked(True)
            self.submit_button.setText(Constants.BUY)
        elif button == self.sell_radio and value:
            self.action_type = Constants.SELL
            self.combo_buy_radio.setChecked(True)
            self.submit_button.setText(Constants.SELL)
 

    def comboBuySellSelection(self, button, value):
        if button == self.combo_buy_radio and value:
            self.combo_action_type = Constants.BUY
            self.oco_button.setText("Place Buy")
        elif button == self.combo_sell_radio and value:
            self.combo_action_type = Constants.SELL
            self.oco_button.setText("Place Sell")


    def stepBuySellSelection(self, button, value):
        if button == self.step_buy_radio and value:
            self.step_action_type = Constants.BUY
            self.step_entry_trigger_offset_box.setValue(0.01)
            self.step_entry_limit_offset_box.setValue(0.1)
            self.step_stop_trigger_offset_box.setValue(-0.1)
            self.step_stop_limit_offset_box.setValue(-0.1)
        elif button == self.step_sell_radio and value:
            self.step_action_type = Constants.SELL
            self.step_entry_trigger_offset_box.setValue(-0.01)
            self.step_entry_limit_offset_box.setValue(-0.1)
            self.step_stop_trigger_offset_box.setValue(0.1)
            self.step_stop_limit_offset_box.setValue(0.1)

        self.checkIfStairTradable()


    def stepProfitSelection(self, button, value):
        if button == self.step_profit_factor_radio and value:
            self.step_profit_type = 'Factor'
        elif button == self.step_profit_offset_radio and value:
            self.step_profit_type = 'Offset'
        elif button == self.step_profit_price_radio and value:
            self.step_profit_type = 'Price'

        self.step_prop_update_signal.emit({'profit_type': self.step_profit_type})
        print(f"We set it to: {self.step_profit_type}")
        

    def stopLimitCheck(self, value):
        print(f"TradeMaker.stopLimitCheck {value} {Qt.Checked}")
        self.stop_limit_on = (value == Qt.Checked)
        
        if self.stop_limit_on:
            self.stop_loss_on = True
            self.stop_loss_check.setChecked(self.stop_loss_on)

    def stoplossCheck(self, value):
        print("TradeMaker.stoplossCheck")
        self.stop_loss_on = value

        # if not self.stop_loss_on:
        #     self.stop_limit_check.setChecked(self.stop_limit_on)


    def profitTakeCheck(self, value):
        self.profit_take_on = value
        self.profit_limit_field.setEnabled(value)


    def stepProfitTakeCheck(self, value):
        self.step_profit_take = value
        self.step_prop_update_signal.emit({'profit_take_on': value})
        self.step_profit_factor_spin.setEnabled(value)
        self.step_profit_offset_spin.setEnabled(value)
        self.step_profit_price_spin.setEnabled(value)
        self.step_profit_factor_radio.setEnabled(value)
        self.step_profit_offset_radio.setEnabled(value)
        self.step_profit_price_radio.setEnabled(value)

        
    def stepStoplossCheck(self, value):
        self.step_stop_loss = value
        self.step_prop_update_signal.emit({'stop_loss_on': value})
        self.step_stop_limit_offset_box.setEnabled(value)
        self.step_stop_limit_label.setEnabled(value)

        self.step_stop_trigger_offset_box.setEnabled(value)
        self.step_stop_trigger_label.setEnabled(value)


        #TODO this should be in super
    def accepts(self, value):
        return False


    def stepLevelChange(self, updated_offset, level_type):
        self.step_prop_update_signal.emit({level_type: updated_offset})
    

    def closeEvent(self, *args, **kwargs):
        super().closeEvent(*args, **kwargs)
        self.history_manager.finished.emit()
        self.symbol_manager.finished.emit()
        # self.order_manager.finished.emit()

        


