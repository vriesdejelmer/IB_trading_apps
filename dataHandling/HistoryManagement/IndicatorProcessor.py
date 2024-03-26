import json
from dataHandling.Constants import Constants, MAIN_BAR_TYPES, DT_BAR_TYPES, MINUTES_PER_BAR, RESAMPLING_BARS
import pandas as pd
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject, Qt
import itertools
from generalFunctionality.GenFunctions import addRSIsEMAs, getLowsHighsCount

class IndicatorProcessor(QObject):

    last_uid_update = dict()
    indicators = set(['rsi', 'steps'])

    finished = pyqtSignal()

    _previous_values = dict()
    indicator_updater = pyqtSignal(str, dict)
    rsi_bar_types = DT_BAR_TYPES
    _tracking_stocks = dict()
    step_bar_types = DT_BAR_TYPES

    def __init__(self, data_buffers):
        super().__init__()
        self.data_buffers = data_buffers
        print(type(self.data_buffers))
        

    def addIndicators(self, indicators):
        self.indicators.update(indicators)

    def run(self):
        self.data_buffers.buffer_updater.connect(self.bufferUpdate, Qt.QueuedConnection)


    @pyqtSlot(dict)
    def setTrackingList(self, stock_list):
        self._tracking_stocks = stock_list
        

    def isUpdatable(self):
        for stock in self._stock_list:
            if not self.buffered_manager.allRangesUpToDate(stock):
                return False

        return True


    @pyqtSlot(str, dict)
    def bufferUpdate(self, signal, sub_signal):
        print(f"IndicatorProcessor.bufferUpdate {signal}")
        if signal == Constants.HAS_NEW_DATA:
            uid = sub_signal['uid']
            if uid in self._tracking_stocks:
                if 'bars' in sub_signal:
                    bars = sub_signal['bars']
                else:
                    bars = None
                if 'updated_from' in sub_signal:
                    updated_from = sub_signal['updated_from']
                else:
                    updated_from = None

                bars = [bar_type for bar_type in bars if self.hasUpdated(uid, bar_type)]
                if len(bars) > 0:
                    self.updateIndicators(updated_uids=[uid], bar_types=bars, updated_from=updated_from)
                    self.updatePrevious([uid], bars)

        elif signal == Constants.DATA_LOADED_FROM_FILE:
            updated_uids = [uid for uid in sub_signal['uids'] if uid in self._tracking_stocks]
            if len(updated_uids) > 0:
                self.updateIndicators(updated_uids)
                self.updatePrevious(updated_uids)

    
    def updatePrevious(self, uids, bar_types=DT_BAR_TYPES):
        for uid in uids:
            for bar_type in bar_types:
                if self.data_buffers.bufferExists(uid, bar_type):
                    self._previous_values[uid, bar_type] = self.data_buffers.getLatestRow(uid, bar_type)
    

    def hasUpdated(self, uid, bar_type):
        if self.data_buffers.bufferExists(uid, bar_type):
            latest_row = self.data_buffers.getLatestRow(uid, bar_type)
            if (uid, bar_type) in self._previous_values:
                previous_row = self._previous_values[uid, bar_type]
                same_index_label = previous_row.name == latest_row.name
                same_values = (previous_row[Constants.CLOSE] == latest_row[Constants.CLOSE]).all()
                return same_index_label and same_values
        return True


    def updateIndicators(self, updated_uids=None, bar_types=None, indicator_type=None, updated_from=None):
        print("IndicatorProcessor.updated_uids")
        if 'rsi' in self.indicators:
            self.computeRSIs(updated_uids=updated_uids, updated_bar_types=bar_types, from_indices=updated_from)

        if 'steps' in self.indicators:
            self.computeSteps(updated_uids=updated_uids, updated_bar_types=bar_types)
            
    
    def computeSteps(self, updated_uids=None, updated_bar_types=None):
        print("IndicatorProcessor.computeSteps")
        if updated_uids is None:
            updated_uids = self.getTrackingUIDs()

        if updated_bar_types is None:
            bar_types = self.step_bar_types
        else:
            bar_types = [bar for bar in updated_bar_types if bar in self.step_bar_types]

        for uid, bar_type in itertools.product(updated_uids, bar_types):
            if self.data_buffers.bufferExists(uid, bar_type):
                stock_frame = self.data_buffers.getBufferFor(uid, bar_type)
                
                low_move, high_move, inner_bar_specs = getLowsHighsCount(stock_frame)

                new_value_dict = {'UpSteps': low_move['count'], 'DownSteps': high_move['count'], 'UpLevel': low_move['level'] , 'DownLevel': high_move['level'], 'UpApex': low_move['apex'], 'DownApex': high_move['apex'], 'UpMove': low_move['move'], 'DownMove': high_move['move'], 'InnerCount': inner_bar_specs['count']}
                self.data_buffers.setIndicatorValues(uid, bar_type, new_value_dict)
                self.indicator_updater.emit(Constants.HAS_NEW_VALUES, {'uid': uid, 'bar_type': bar_type, 'update_type': 'steps'})

        

    def computeRSIs(self, updated_uids=None, updated_bar_types=None, from_indices=None):
        print(f"IndicatorProcessor.computeRSIs {updated_uids} {updated_bar_types}")
        if updated_uids is None:
            updated_uids = self.getTrackingUIDs()
        if updated_bar_types is None:
            bar_types = self.rsi_bar_types
        else:
            bar_types = [bar for bar in updated_bar_types if bar in self.rsi_bar_types]
                
        for uid, bar_type in itertools.product(updated_uids, bar_types):
            starting_index = None
            if (from_indices is not None) and (bar_type in from_indices):
                starting_index = from_indices[bar_type]
            if self.data_buffers.bufferExists(uid, bar_type):
                stock_frame = self.data_buffers.getBufferFor(uid, bar_type)
                if len(stock_frame) > 14:
                    rsi_padded_frame = addRSIsEMAs(stock_frame, starting_index)
                    self.data_buffers.setBufferFor(uid, bar_type, rsi_padded_frame)
                    self.indicator_updater.emit(Constants.HAS_NEW_VALUES, {'uid': uid, 'bar_type': bar_type, 'update_type': 'rsi'})


    def getRSIColumn(self, uid, bar_type):
        return self.data_buffers.getColumnFor(uid, bar_type, 'rsi')

    def getStepValues(self, uid, bar_type):
        
        up_move = self.data_buffers.getIndicatorValues(uid, bar_type, ['UpSteps', 'UpLevel', 'UpApex','UpMove'])
        down_move = self.data_buffers.getIndicatorValues(uid, bar_type, ['DownSteps', 'DownLevel', 'DownApex','DownMove'])
        return up_move, down_move



    def getTrackingUIDs(self):
        return [key for key in self._tracking_stocks.keys()]
          