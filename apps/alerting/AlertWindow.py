
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

from uiComps.qtGeneration.Alert_UI import Ui_MainWindow as Alert_UI
from uiComps.customWidgets.CheckableComboBox import CheckableComboBox
from dataHandling.Constants import Constants
from uiComps.generalUIFunctionality import ProcessorWindow

class AlertWindow(ProcessorWindow, Alert_UI):

    time_frame_names = ['all', '1m', '2m', '3m', '5m', '15m', '1h', '4h', '1d']
    bar_type_conv = {'1m': Constants.ONE_MIN_BAR,'2m': Constants.TWO_MIN_BAR,'3m': Constants.THREE_MIN_BAR,'5m': Constants.FIVE_MIN_BAR,'15m': Constants.FIFTEEN_MIN_BAR,'1h': Constants.HOUR_BAR,'4h': Constants.FOUR_HOUR_BAR,'1d': Constants.DAY_BAR}
    frequency_choices = ['1s', '10s', '1m']
    
    def __init__(self):
        ProcessorWindow.__init__(self)
        Alert_UI.__init__(self)
        
        self.setupUi()

        self.setupActions()
                

    def setupUi(self):
        super().setupUi(self) #TODO this seems wrong....
        print("So we aint getting here first?")
        self.comp_checkable_lists = CheckableComboBox()
        self.processing_props_layout.layout().addWidget(self.comp_checkable_lists, 0, 2, 1, 1)
        self.update_frequency_box.addItems(self.frequency_choices)
        self.update_frequency_box.setCurrentIndex(self.frequency_choices.index('1m'))
    


    def crossCheckChange(self, value):
        clicked_check_box = self.sender()

        if clicked_check_box == self.cross_box_all:
            for tf in self.time_frame_names:
                self.widgetFor(f"cross_box_{tf}").setCheckState(self.cross_box_all.checkState())

        self.updateCheckListFor("cross_box", "cross_checks")
        
    

    def reversalCheckChange(self, value):
        clicked_check_box = self.sender()

        if clicked_check_box == self.reversal_box_all:
            for tf in self.time_frame_names:
                self.widgetFor(f"reversal_box_{tf}").setCheckState(self.reversal_box_all.checkState())

        self.updateCheckListFor("reversal_box", "reversal_checks")
        

    def upCheckChange(self, value):
        clicked_check_box = self.sender()

        if clicked_check_box == self.up_check_all:
            for tf in self.time_frame_names:
                self.widgetFor(f"up_check_{tf}").setCheckState(self.up_check_all.checkState())

        self.updateCheckListFor("up_check", "up_checks")



    def downCheckChange(self, value):
        clicked_check_box = self.sender()

        if clicked_check_box == self.down_check_all:
            for tf in self.time_frame_names:
                self.widgetFor(f"down_check_{tf}").setCheckState(self.down_check_all.checkState())

        self.updateCheckListFor("down_check", "down_checks")


    def lowerRsiChange(self, value):
        clicked_spin_box = self.sender()

        if clicked_spin_box == self.lower_spin_all:
            for tf in self.time_frame_names:
                self.widgetFor(f"lower_spin_{tf}").setValue(value)

        self.updateThresholds("lower_spin", "cross_down_threshold")


    def upperRsiChange(self, value):
        clicked_spin_box = self.sender()

        if clicked_spin_box == self.higher_spin_all:
            for tf in self.time_frame_names:
                self.widgetFor(f"higher_spin_{tf}").setValue(value)

        self.updateThresholds("higher_spin", "cross_up_threshold")


    def downThresholdChange(self, value):
        clicked_spin_box = self.sender()

        if clicked_spin_box == self.down_spin_all:
            for tf in self.time_frame_names:
                self.widgetFor(f"down_spin_{tf}").setValue(value)

        self.updateThresholds("down_spin", "step_down_threshold")



    def upThresholdChange(self, value):
        clicked_spin_box = self.sender()

        if clicked_spin_box == self.up_spin_all:
            for tf in self.time_frame_names:
                self.widgetFor(f"up_spin_{tf}").setValue(value)

        self.updateThresholds("up_spin", "step_up_threshold")


    def setupActions(self):
        self.data_listen_checkbox.stateChanged.connect(self.toggleDataListening)
        self.rotation_button.clicked.connect(self.startUpdating)
        self.list_selection_button.clicked.connect(self.toggleSelection)
        self.comp_checkable_lists.activated.connect(self.listSelection)

        self.update_frequency_box.currentTextChanged.connect(self.updateFrequencyUpdate)

        for tf in self.time_frame_names:
            self.widgetFor(f"cross_box_{tf}").toggled.connect(self.crossCheckChange)
            self.widgetFor(f"reversal_box_{tf}").toggled.connect(self.reversalCheckChange)
            self.widgetFor(f"up_check_{tf}").toggled.connect(self.upCheckChange)
            self.widgetFor(f"down_check_{tf}").toggled.connect(self.downCheckChange)
            self.widgetFor(f"lower_spin_{tf}").valueChanged.connect(self.lowerRsiChange)
            self.widgetFor(f"higher_spin_{tf}").valueChanged.connect(self.upperRsiChange)
            self.widgetFor(f"up_spin_{tf}").valueChanged.connect(self.upThresholdChange)
            self.widgetFor(f"down_spin_{tf}").valueChanged.connect(self.downThresholdChange)
            

    def widgetFor(self, button_name):
        return getattr(self, button_name)
        

