
from dataHandling.Constants import Constants, MAIN_BAR_TYPES, DT_BAR_TYPES, MINUTES_PER_BAR
from dataHandling.DataStructures import DetailObject
from dataHandling.TradeManagement.UserDataManagement import readStockList
from datetime import datetime
from pytz import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from generalFunctionality.GenFunctions import barStartTime, barEndTime, standardBeginDateFor

import sys
import time
import numpy as np
import pandas as pd

from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QThread, Qt, QEventLoop


class BufferedDataManager(QObject):

    api_updater = pyqtSignal(str, dict)

    alternate_list = None
    partial_update = False
    max_day_diff = 3
    stocks_to_fetch = dict()
    updated_through = dict()
    initial_fetch = True

    queued_update_requests = []

    reset_signal = pyqtSignal()
    create_request_signal = pyqtSignal(DetailObject, datetime, datetime, str)
    request_update_signal = pyqtSignal(dict, str, bool)
    group_request_signal = pyqtSignal(str)
    execute_request_signal = pyqtSignal(int)


    def __init__(self, history_manager, name="BufferedManager"):
        super().__init__()

        self.name = name
        self.history_manager = history_manager
        self.data_buffers = history_manager.getDataBuffer()
        self.data_buffers.saveOn = True
        self.history_manager.addNewListener(self, self.apiUpdate)
        

    def moveToThread(self, thread):
        super().moveToThread(thread)
        self.connectSignalsToSlots()


    def connectSignalsToSlots(self):
        # print("BufferedManager.connectSignalsToSlots")
        self.reset_signal.connect(self.history_manager.cancelActiveRequests, Qt.QueuedConnection)
        self.create_request_signal.connect(self.history_manager.createRequestsForContract, Qt.QueuedConnection)
        self.request_update_signal.connect(self.history_manager.requestUpdates, Qt.QueuedConnection)
        self.group_request_signal.connect(self.history_manager.groupCurrentRequests, Qt.QueuedConnection)
        self.execute_request_signal.connect(self.history_manager.iterateHistoryRequests, Qt.QueuedConnection)
        
        # print("BufferedManager.connectSignalsToSlots finished")

    
    ################ LIST HANDLING

    def setStockList(self, buffering_stocks):
        print(f"BufferedManager.setStockList is performed on {int(QThread.currentThreadId())}")
        self.initial_fetch = True
        self._buffering_stocks = buffering_stocks.copy()
        self.data_buffers.loadBuffers(self._buffering_stocks)


    ################ CALLBACK

    @pyqtSlot(str, dict)
    def apiUpdate(self, signal, data_dict):
        if signal == Constants.HISTORICAL_GROUP_COMPLETE:
            if len(self.stocks_to_fetch) != 0:
                self.fetchNextStock()
            elif self.partial_update:
                self.requestUpdates(update_list=self.update_list)
                self.partial_update = False
            else:
                self.api_updater.emit(Constants.ALL_DATA_LOADED, dict())
                self.initial_fetch = False
        elif signal == Constants.HISTORICAL_UPDATE_COMPLETE:
            print("1) DO WE MAKE IT HERE?")
            if len(self.queued_update_requests) > 0:
                print("2) AND VIA HERE???")
                request = self.queued_update_requests.pop(0)
                self.requestUpdates(update_bar=request['bar_type'], keep_up_to_date=request['keep_up_to_date'], update_list=request['update_list'])
            else:
                self.api_updater.emit(Constants.ALL_DATA_LOADED, dict())
                self.initial_fetch = False



    ################ CREATING AND TRIGGERING HISTORIC REQUESTS

    def fetchLatestStockDataWithCancelation(self, bar_types=DT_BAR_TYPES):
        print(f"BufferedManager.fetchLatestStockDataWithCancelation on thread: {int(QThread.currentThreadId())}")
        self.history_manager.cleanup_done_signal.connect(lambda: self.fetchLatestStockData(bar_types, True), Qt.QueuedConnection)
        self.reset_signal.emit()
        

    @pyqtSlot()
    @pyqtSlot(list)
    def fetchLatestStockData(self, bar_types=DT_BAR_TYPES, needs_disconnect=False):
        print(f"BufferedManager.fetchLatestStockData on thread: {int(QThread.currentThreadId())}")
        if needs_disconnect: self.history_manager.cleanup_done_signal.disconnect()

        self.history_manager.process_owner = self

        self.stocks_to_fetch, self.update_list = self.splitRequestsForUpdateType()

        # print(f"We have {len(self.stocks_to_fetch)} tickers to fetch and {len(self.update_list)} to update")

        if len(self.stocks_to_fetch) > 0:
            self.history_manager._is_buffering = True
            self.fetchNextStock(bar_types=bar_types)
            if len(self.update_list) > 0:
                self.partial_update = True

        if len(self.update_list) > 0:
                self.requestUpdates(update_list=self.update_list)


    def fetchHistStockData(self, bar_types, date_range=None, selected_uid=None):
        self.history_manager.process_owner = self

        self.stocks_to_fetch = dict()
        if selected_uid is None:
            for uid, value in self._buffering_stocks.items():
                self.stocks_to_fetch[uid] = value      
        else:
            self.stocks_to_fetch[selected_uid] = self._buffering_stocks[selected_uid]
        if len(self.stocks_to_fetch) > 0:
            self.history_manager._is_buffering = True
            self.fetchNextStock(bar_types, full_fetch=True)
            

    def splitRequestsForUpdateType(self):
        stocks_to_fetch = dict()
        update_list = dict()
        for uid, value in self._buffering_stocks.items():
            if self.allRangesDownloaded(uid):
                last_timestamp = self.data_buffers.getIndexAtPos(uid, Constants.DAY_BAR, pos=-1)
                if self.isRecent(last_timestamp):
                    update_list[uid] = value
                else:
                    stocks_to_fetch[uid] = value
            else:
                stocks_to_fetch[uid] = value

        return stocks_to_fetch, update_list


    def allRangesDownloaded(self, uid, bar_types=MAIN_BAR_TYPES):

        for bar_type in bar_types:
            if not self.data_buffers.bufferExists(uid, bar_type):
                
                if bar_type != Constants.FOUR_HOUR_BAR:
                    return False
        return True


    def isRecent(self, timestamp):
        current_dateTime = datetime.now(timezone(Constants.NYC_TIMEZONE)).replace(microsecond=0)
        
        day_diff = (current_dateTime-timestamp).days
        return day_diff < self.max_day_diff


    def hasDataInLast(self, minutes, uid, bar_type):
        now_time = datetime.now(timezone(Constants.NYC_TIMEZONE))
        time_cutoff = now_time - timedelta(minutes=minutes)
        if self.data_buffers.bufferExists(uid, bar_type):
            return (self.data_buffers.getLastIndexLabel(uid, bar_type) >= (time_cutoff))
        return False


    def fetchNextStock(self, bar_types=MAIN_BAR_TYPES, full_fetch=False):
        # print("BufferedManager.fetchNextStock")
        uid, value = self.stocks_to_fetch.popitem()
        details = DetailObject(symbol=value[Constants.SYMBOL], exchange=value['exchange'], numeric_id=uid)

        for bar_type in bar_types:
            date_ranges = self.getDataRanges(uid, bar_type, full_fetch)
            for begin_date, end_date in date_ranges:
                self.create_request_signal.emit(details, begin_date, end_date, bar_type)

        if full_fetch:
            if len(self.stocks_to_fetch) > 0:
                self.fetchNextStock(bar_types=bar_types, full_fetch=full_fetch)
            else:
                # print("Or here")
                self.execute_request_signal.emit(11_000)
        else:
            # print("Via here")
            self.group_request_signal.emit(uid)
            self.execute_request_signal.emit(2_000)


    @pyqtSlot(str, bool)
    def requestUpdates(self, update_bar=Constants.ONE_MIN_BAR, keep_up_to_date=False, update_list=None, needs_disconnect=False):
        print(f"BufferedManager.requestUpdates {update_bar}")

        if needs_disconnect: self.history_manager.cleanup_done_signal.disconnect()
        
        if update_list is None:
            update_list = self._buffering_stocks.copy()

        if self.smallThanFiveMin(update_bar):
            self.requestSmallUpdates(update_bar, keep_up_to_date, update_list)
        else:
            now_time = datetime.now(timezone(Constants.NYC_TIMEZONE))
            for uid in update_list:
                update_list[uid]['begin_date'] = self.getBeginDate(uid, update_bar, now_time)
            
            self.request_update_signal.emit(update_list, update_bar, keep_up_to_date) #, keep_up_to_date)


    def requestSmallUpdates(self, update_bar, keep_up_to_date, update_list):
        now_time = datetime.now(timezone(Constants.NYC_TIMEZONE))
        five_min_update_list = dict()
        for uid in update_list:
            begin_date = self.getBeginDate(uid, Constants.FIVE_MIN_BAR, now_time)
            total_seconds = int((now_time-begin_date).total_seconds())
            if total_seconds > 10800:
                five_min_update_list[uid] = update_list[uid]
                five_min_update_list[uid]['begin_date'] = begin_date

        
        for uid in update_list:
            update_list[uid]['begin_date'] = now_time - relativedelta(minutes=180)
        
        if len(five_min_update_list) > 0:
            self.request_update_signal.emit(five_min_update_list, Constants.FIVE_MIN_BAR, False)
            self.queued_update_requests.append({'bar_type': update_bar, 'update_list': update_list, 'keep_up_to_date': keep_up_to_date})
        else:
            self.request_update_signal.emit(update_list, update_bar, keep_up_to_date)


    ################ DATE AND RANGE HANDLING


    def getBeginDate(self, uid, bar_type, end_date):        
        begin_date = None
        if self.data_buffers.bufferExists(uid, bar_type):
            existing_ranges = self.data_buffers.getRangesForBuffer(uid, bar_type)
            if len(existing_ranges) > 0:
                begin_date = existing_ranges[-1][1]
                return begin_date

        if begin_date is None:
            return standardBeginDateFor(end_date, bar_type)


    def smallThanFiveMin(self, bar_type):
        return ((bar_type == Constants.ONE_MIN_BAR) or (bar_type == Constants.TWO_MIN_BAR) or (bar_type == Constants.THREE_MIN_BAR))


    def getDataRanges(self, uid, bar_type, full_fetch=False):
        end_date = datetime.now(timezone(Constants.NYC_TIMEZONE)).replace(microsecond=0)

        if full_fetch:
            return self.getFullRanges(uid, bar_type, end_date)
        else:
            return self.getStandardRanges(uid, bar_type, end_date)
        


    def getStandardRanges(self, uid, bar_type, end_date):
        standard_begin_date = standardBeginDateFor(end_date, bar_type)
        if self.data_buffers.bufferExists(uid, bar_type):
            existing_ranges = self.data_buffers.getRangesForBuffer(uid, bar_type)
            if (existing_ranges[-1][1] > standard_begin_date):
                return [(existing_ranges[-1][1], end_date)] 

        return [(standard_begin_date, end_date)]


    def getFullRanges(self, uid, bar_type, end_date):
        if uid in self.history_manager.earliest_date_by_uid:
            earliest_date = self.history_manager.earliest_date_by_uid[uid]
        else:
            now = datetime.now(timezone('America/New_York'))
            earliest_date = now - relativedelta(years=10)

        if (uid, bar_type) in self.existing_buffers:
            begin_date = earliest_date
            existing_ranges = self.existing_buffers[uid, bar_type].attrs['ranges']
            missing_ranges = self.determineMissingRanges(existing_ranges, (begin_date, end_date))
            missing_ranges = self.combineAdjacentRanges(missing_ranges)
            return missing_ranges
        else:
            return [(earliest_date, end_date)]


    def combineAdjacentRanges(self, missing_ranges):
        last_range = missing_ranges[-1]

        difference = last_range[1] - last_range[0]
        if difference.days == 0:
            missing_ranges.pop()

        return missing_ranges


    def determineMissingRanges(self, existing_ranges, new_range):
        start_new, end_new = new_range
        missing_ranges = []
        
        # Add the start of the new range to the missing ranges
        missing_ranges.append((start_new, end_new))
        for start_existing, end_existing in sorted(existing_ranges):
            for index, (start_missing, end_missing) in enumerate(missing_ranges):
                # If the existing range is entirely within a missing range
                if start_existing >= start_missing and end_existing <= end_missing:
                    del missing_ranges[index]
                    if start_existing > start_missing:
                        missing_ranges.append((start_missing, start_existing))
                    if end_existing < end_missing:
                        missing_ranges.append((end_existing, end_missing))
                    break
                # If the existing range overlaps the start of a missing range
                elif start_existing <= start_missing and end_existing > start_missing and end_existing <= end_missing:
                    missing_ranges[i] = (end_existing, end_missing)
                    break
                # If the existing range overlaps the end of a missing range
                elif start_existing >= start_missing and start_existing < end_missing and end_existing >= end_missing:
                    missing_ranges[i] = (start_missing, start_existing)
                    break
                    
        return sorted(missing_ranges)


    @pyqtSlot()
    def cancelUpdates(self):
        print("We ask for cancelling")
        if self.history_manager.is_updating:
            print("We trigger a reset in history_manager")
            self.reset_signal.emit()


    ################ DATA PROCESSING
