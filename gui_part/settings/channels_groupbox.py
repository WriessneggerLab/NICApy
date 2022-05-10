from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class Channels(qtw.QWidget):
    '''
    Class for building the Channels Groupbox
    Inherited from QWidget.

    --------
    Methods:
    --------

    build_channels_gb(self)
    get_loaded_checked_channels_exclude(self, excl_channel_list)
    get_loaded_checked_channels_displayed(self, disp_channel_list)
    mark_all_chans(self, checked)
    mark_none_chans(self, checked)
    check_chan_checked(self, checked, text)
    switch_mode_exclude(self, clicked)
    switch_mode_display(self, clicked)
    build_excl_chans_key(self)
    allow_excluding_channels(self, allow)
    allow_display_channels(self, allow)

    '''
    submit_excluded_channs = qtc.pyqtSignal(dict)
    submit_displayed_channs = qtc.pyqtSignal(dict)
    submit_if_displayed = qtc.pyqtSignal()
    submit_if_excluded = qtc.pyqtSignal()
    submit_allow_excl_channs = qtc.pyqtSignal(bool)
    submit_allow_displayed_channs = qtc.pyqtSignal(bool)
    submit_temporary_displayed_channs = qtc.pyqtSignal(list, list)

    def __init__(self, *args, **kwargs):
        super(Channels, self).__init__(*args, **kwargs)
        self.build_channels_gb()

    def build_channels_gb(self):
        '''
        Creates Channels Groupbox layout and its widgets
        '''
        channels_gb = qtw.QGroupBox('Channels')
        outer_layout = qtw.QVBoxLayout()
        outer_layout.addWidget(channels_gb)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout = qtw.QGridLayout()
        grid_layout.setSpacing(5)

        self.all_channels = []
        for i in range(0, 61):
            ch_nr = "%s" % format(i + 1)
            self.all_channels.append(qtw.QCheckBox("Ch" + ch_nr.zfill(2)))

        # the following has been tried with a for-loop, but did not work, maybe this can be implemented differently
        self.excluded_channs = []
        self.displayed_channs = []
        self.all_channels[0].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[0].text()))
        self.all_channels[0].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[1].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[1].text()))
        self.all_channels[1].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[2].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[2].text()))
        self.all_channels[2].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[3].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[3].text()))
        self.all_channels[3].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[4].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[4].text()))
        self.all_channels[4].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[5].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[5].text()))
        self.all_channels[5].stateChanged.connect(self.build_excl_chans_key)

        self.all_channels[6].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[6].text()))
        self.all_channels[6].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[7].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[7].text()))
        self.all_channels[7].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[8].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[8].text()))
        self.all_channels[8].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[9].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[9].text()))
        self.all_channels[9].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[10].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[10].text()))
        self.all_channels[10].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[11].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[11].text()))
        self.all_channels[11].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[12].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[12].text()))
        self.all_channels[12].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[13].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[13].text()))
        self.all_channels[13].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[14].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[14].text()))
        self.all_channels[14].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[15].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[15].text()))
        self.all_channels[15].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[16].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[16].text()))
        self.all_channels[16].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[17].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[17].text()))
        self.all_channels[17].stateChanged.connect(self.build_excl_chans_key)

        self.all_channels[18].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[18].text()))
        self.all_channels[18].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[19].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[19].text()))
        self.all_channels[19].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[20].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[20].text()))
        self.all_channels[20].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[21].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[21].text()))
        self.all_channels[21].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[22].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[22].text()))
        self.all_channels[22].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[23].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[23].text()))
        self.all_channels[23].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[24].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[24].text()))
        self.all_channels[24].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[25].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[25].text()))
        self.all_channels[25].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[26].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[26].text()))
        self.all_channels[26].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[27].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[27].text()))
        self.all_channels[27].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[28].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[28].text()))
        self.all_channels[28].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[29].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[29].text()))
        self.all_channels[29].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[30].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[30].text()))
        self.all_channels[30].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[31].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[31].text()))
        self.all_channels[31].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[32].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[32].text()))
        self.all_channels[32].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[33].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[33].text()))
        self.all_channels[33].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[34].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[34].text()))
        self.all_channels[34].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[35].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[35].text()))
        self.all_channels[35].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[36].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[36].text()))
        self.all_channels[36].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[37].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[37].text()))
        self.all_channels[37].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[38].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[38].text()))
        self.all_channels[38].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[39].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[39].text()))
        self.all_channels[39].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[40].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[40].text()))
        self.all_channels[40].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[41].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[41].text()))
        self.all_channels[41].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[42].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[42].text()))
        self.all_channels[42].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[43].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[43].text()))
        self.all_channels[43].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[44].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[44].text()))
        self.all_channels[44].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[45].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[45].text()))
        self.all_channels[45].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[46].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[46].text()))
        self.all_channels[46].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[47].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[47].text()))
        self.all_channels[47].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[48].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[48].text()))
        self.all_channels[48].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[49].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[49].text()))
        self.all_channels[49].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[50].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[50].text()))
        self.all_channels[50].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[51].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[51].text()))
        self.all_channels[51].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[52].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[52].text()))
        self.all_channels[52].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[53].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[53].text()))
        self.all_channels[53].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[54].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[54].text()))
        self.all_channels[54].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[55].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[55].text()))
        self.all_channels[55].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[56].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[56].text()))
        self.all_channels[56].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[57].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[57].text()))
        self.all_channels[57].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[58].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[58].text()))
        self.all_channels[58].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[59].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[59].text()))
        self.all_channels[59].stateChanged.connect(self.build_excl_chans_key)
        self.all_channels[60].stateChanged.connect(
            lambda value: self.check_chan_checked(value, self.all_channels[60].text()))
        self.all_channels[60].stateChanged.connect(self.build_excl_chans_key)

        # for chan in self.all_channels:
        #   chan.stateChanged.connect(lambda value: self.check_chan_checked(value))
        # chan.stateChanged.connect(self.build_excl_chans_key)

        self.all_channels.append(qtw.QCheckBox('All'))
        self.all_channels.append(qtw.QCheckBox('None'))
        self.all_channels[61].stateChanged.connect(self.mark_all_chans)
        self.all_channels[62].stateChanged.connect(self.mark_none_chans)

        for row in range(0, 9):
            for col in range(0, 7):
                grid_layout.addWidget(self.all_channels[row * 7 + col], row, col)

        grid_layout.setContentsMargins(10, 0, 0, 0)
        grid_layout.setVerticalSpacing(10)
        grid_layout.setHorizontalSpacing(5)
        v_layout = qtw.QVBoxLayout()
        channel_options = qtw.QGroupBox('Channel Options')
        self.display_channels = qtw.QRadioButton('Display Channels')
        self.display_channels.setChecked(True)
        self.exclude_channels = qtw.QRadioButton('Exclude Channels')
        self.exclude_channels.setEnabled(False)
        self.exclude_channels.clicked.connect(self.switch_mode_exclude)
        self.display_channels.clicked.connect(self.switch_mode_display)

        h_layout = qtw.QHBoxLayout()
        h_layout.addWidget(self.display_channels)
        h_layout.addWidget(self.exclude_channels)
        channel_options.setLayout(h_layout)
        v_layout.addLayout(grid_layout)
        v_layout.addWidget(channel_options)
        channels_gb.setLayout(v_layout)
        self.setLayout(outer_layout)

    def get_loaded_checked_channels_exclude(self, excl_channel_list):
        '''
        Get excluded channels specified in the loaded properties json file
        @param excl_channel_list: list including channels to be excluded
        '''
        if len(excl_channel_list) is 61:
            self.all_channels[61].setChecked(True)
        else:
            for chan_nr in excl_channel_list:
                self.all_channels[chan_nr - 1].setChecked(True)

    def get_loaded_checked_channels_displayed(self, disp_channel_list):
        '''
        Get single displayed channels specified in the loaded properties json file
        @param disp_channel_list: list including channels to be displayed as single
        '''
        if len(disp_channel_list) is 61:
            self.all_channels[61].setChecked(True)
        else:
            for chan_nr in disp_channel_list:
                self.all_channels[chan_nr - 1].setChecked(True)

    @qtc.pyqtSlot(int)
    def mark_all_chans(self, state_changed):
        '''
        Marks all channels available as checked. In this version it always marks all 61 channels. If a probe set with
        fewer channels is selected, that will be then taken into account in the check_probeset method in model_part
        @param state_changed: int, return value of stateChanged
        '''
        if state_changed == 2 and self.exclude_channels.isChecked():
            self.all_channels[62].setChecked(False)
            index_list = []
            for indx, chan in enumerate(self.all_channels[0:61]):
                chan.setChecked(True)
                index_list.append(indx + 1)
            self.excluded_channs = sorted(index_list)
        if state_changed == 2 and self.display_channels.isChecked():
            self.all_channels[62].setChecked(False)
            index_list = []
            for indx, chan in enumerate(self.all_channels[0:61]):
                chan.setChecked(True)
                index_list.append(indx + 1)
            self.displayed_channs = sorted(index_list)
        self.build_excl_chans_key()

    @qtc.pyqtSlot(int)
    def mark_none_chans(self, state_changed):
        '''
        Marks all channels available as unchecked. In this version it always unchecks all 61 channels. If a probe set
        with fewer channels is selected, that will be then taken into account in the check_probeset method in model_part
        @param state_changed: int, return value of stateChanged
        '''
        if state_changed == 2 and self.exclude_channels.isChecked():
            self.all_channels[61].setChecked(False)
            for indx, chan in enumerate(self.all_channels[0:61]):
                chan.setChecked(False)
            self.excluded_channs.clear()
        if state_changed == 2 and self.display_channels.isChecked():
            self.all_channels[61].setChecked(False)
            for indx, chan in enumerate(self.all_channels[0:61]):
                chan.setChecked(False)
            self.displayed_channs.clear()

    def check_chan_checked(self, state_changed, text):
        '''
        Checks if a single channels has been selected. (Can be for exclusion or displaying)
        @param state_changed: int, return value 0 or 2 if state of checkbox changed (2) or not (0)
        @param text: text of corresponding channel, e.g. Ch1
        '''
        indx = int(text.lstrip('Ch'))

        if self.exclude_channels.isChecked():
            if state_changed == 0:
                if indx in self.excluded_channs:
                    self.excluded_channs.remove(indx)

            if state_changed == 2:
                self.all_channels[62].setChecked(False)
                self.excluded_channs.append(indx) if indx not in self.excluded_channs else self.excluded_channs

        if self.display_channels.isChecked():
            if state_changed == 0:
                if indx in self.displayed_channs:
                    self.displayed_channs.remove(indx)

            if state_changed == 2:
                self.all_channels[62].setChecked(False)
                self.displayed_channs.append(indx) if indx not in self.displayed_channs else self.displayed_channs

    def switch_mode_exclude(self, clicked):
        '''
        Communicates if the radio button Exclude is checked and hence checked channels will be added to excluded
        channels
        @param clicked: bool, True if radio button Exclude is checked
        '''
        if clicked:
            for chan in self.displayed_channs:
                self.all_channels[chan - 1].setChecked(False)
            for chan in self.excluded_channs:
                self.all_channels[chan - 1].setChecked(True)

    def switch_mode_display(self, clicked):
        '''
        Communicates if the radio button Display is checked and hence checked channels will be added to displayed
        channels
        @param clicked: bool, True if radio button Display is checked
        '''
        if clicked:
            for chan in self.excluded_channs:
                self.all_channels[chan - 1].setChecked(False)
            for chan in self.displayed_channs:
                self.all_channels[chan - 1].setChecked(True)

    def build_excl_chans_key(self):
        '''
        Submits selected channels to properties
        '''
        self.submit_excluded_channs.emit(
            {'excluded_channels': sorted(list(set(self.excluded_channs)))})
        self.submit_displayed_channs.emit(
            {'displayed_channels': sorted(list(set(self.displayed_channs)))})

    def allow_excluding_channels(self, allow):
        '''
        Handles enabling and disabling the radio buttons of Display and Exclude channels
        @param allow: bool, returned from Artefacts Groupbox if exclude channels checkbox is checked or not
        '''
        if allow:
            self.exclude_channels.setEnabled(True)
            self.exclude_channels.setChecked(True)
            for channs in self.displayed_channs:
                self.all_channels[channs - 1].setChecked(False)

        if not allow:
            self.display_channels.setEnabled(True)
            self.display_channels.setChecked(True)
            self.exclude_channels.setEnabled(False)
            for excl_channs in self.excluded_channs:
                self.all_channels[excl_channs - 1].setChecked(False)
            self.excluded_channs.clear()

            for disp_channs in self.displayed_channs:
                self.all_channels[disp_channs - 1].setChecked(True)
        self.build_excl_chans_key()

    def allow_display_channels(self, allow):
        '''
        Handles enabling and disabling the radio buttons of Display and Exclude channels
        @param allow: bool, returned from Artefacts Groupbox if exclude channels checkbox is checked or not
        '''
        if not allow:
            for channs in self.displayed_channs:
                self.all_channels[channs - 1].setChecked(True)
            self.excluded_channs.clear()

        if allow:
            # self.display_channels.setEnabled(False)
            self.exclude_channels.setEnabled(True)
            for channs in range(len(self.all_channels)):
                self.all_channels[channs].setChecked(False)

        self.build_excl_chans_key()