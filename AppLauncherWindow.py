# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'optionsGraph.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5.QtWidgets import QMainWindow
from uiComps.qtGeneration.AppLauncher_UI import Ui_MainWindow as AppLauncher_UI
from dataHandling.Constants import Constants


class AppLauncherWindow(QMainWindow, AppLauncher_UI):

    def __init__(self):
        QMainWindow.__init__(self)
        AppLauncher_UI.__init__(self)

        self.setupUi(self)
        self.toggleAppButtons(False)
        self.setupActions()
        

    def toggleAppButtons(self, enabled, interface=Constants.IB_SOURCE):
        if interface == Constants.IB_SOURCE:
            for button in self.ib_group.buttons():
                button.setEnabled(enabled)
            for button in self.general_history_group.buttons():
                button.setEnabled(enabled)
        elif interface == Constants.FINAZON_SOURCE:
            for button in self.ib_group.buttons():
                button.setEnabled(False)
            for button in self.general_history_group.buttons():
                button.setEnabled(enabled)



    def setupActions(self):
        self.connect_button.clicked.connect(self.openConnection)
        self.open_option_pos.clicked.connect(self.openOptionPosApp)
        self.open_option_viz.clicked.connect(self.openOptionVizApp)
        self.open_stocks.clicked.connect(self.openStocksApp)
        self.open_poly_downloader.clicked.connect(self.openDataDetailsApp)
        self.open_movers.clicked.connect(self.openMoversApp)
        # self.open_fitter.clicked.connect(self.openFittingApp)
        # self.open_analysis.clicked.connect(self.openAnalysisApp)
        self.open_man_trader.clicked.connect(self.openManualTraderApp)
        # self.open_auto_trader.clicked.connect(self.openAutoTraderApp)
        self.fetch_rates.clicked.connect(self.downloadShortRateData)
        self.open_list_manager.clicked.connect(self.openListManager)
        self.open_comparisons.clicked.connect(self.openComparisonApp)
        self.open_alert_system.clicked.connect(self.openAlertApp)
        self.trading_type_group.buttonClicked.connect(self.connectionSelection)
        self.data_group.buttonClicked.connect(self.dataSelection)
