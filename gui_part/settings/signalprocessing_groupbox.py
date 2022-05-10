from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class SignalProcessing(qtw.QWidget):
    '''
    Class for building the Signal Processing Groupbox
    Inherited from QWidget.

    --------
    Methods:
    --------

    build_sigproc_gb(self)
    change_anylsis_method(self, current_method)
    change_correction_mode(self, current_mode)
    store_sig_ana_method(self, sig_ana_method)
    store_corr_mode(self, corr_mode)
    store_mayer_source(self, mayer_source)
    store_baseline(self, state_changed, is_checked)
    store_notch(self, state_changed, is_checked)
    store_cut_off(self, cut_off)

    '''
    submit_possible_artefact_correction = qtc.pyqtSignal(list)
    submit_sig_ana_method = qtc.pyqtSignal(dict)
    submit_corr_mode = qtc.pyqtSignal(dict)
    submit_mayer_source = qtc.pyqtSignal(dict)
    submit_baseline = qtc.pyqtSignal(dict)
    submit_notch = qtc.pyqtSignal(dict)
    submit_low_pass = qtc.pyqtSignal(dict)
    submit_cut_off = qtc.pyqtSignal(dict)
    submit_mayer_on_or_off = qtc.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(SignalProcessing, self).__init__(*args, **kwargs)
        self.build_sigproc_gb()

    def build_sigproc_gb(self):
        '''
        Creates Signal Processing Groupbox layout and its widgets
        '''
        sig_proc_gb = qtw.QGroupBox('Signal Processing')

        outer_layout = qtw.QVBoxLayout()
        outer_layout.addWidget(sig_proc_gb)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Labels
        sig_proc_settings = [qtw.QLabel('Signal Analysis Method'), qtw.QLabel('Correction Mode'),
                             qtw.QLabel('Mayer Waves Source')]

        # Widgets
        self.sig_ana_cb = qtw.QComboBox()
        analysis_methods = ['TF (Transfer Function Models)', 'CAR (Common Average Reference)']
        self.sig_ana_cb.addItems(analysis_methods)
        self.sig_ana_cb.setStyleSheet("QComboBox::drop-down")
        self.sig_ana_cb.currentIndexChanged[str].connect(self.change_anylsis_method)
        self.sig_ana_cb.currentTextChanged.connect(self.store_sig_ana_method)

        self.corr_mode_cb = qtw.QComboBox()
        correction_modes = ['Uncorrected', 'Respiration', 'Mayer Waves', 'Mayer and Respiration']
        for mode in correction_modes:
            self.corr_mode_cb.addItem(mode)
        self.corr_mode_cb.currentIndexChanged[str].connect(self.change_correction_mode)
        self.corr_mode_cb.setStyleSheet("QComboBox::drop-down")
        self.corr_mode_cb.currentTextChanged.connect(self.store_corr_mode)
        self.mayer_waves_cb = qtw.QComboBox()
        self.mayer_waves_cb.addItem('Heart Rate')
        self.mayer_waves_cb.setEnabled(False)
        self.mayer_waves_cb.setStyleSheet("QComboBox::drop-down")
        # self.mayer_waves_cb.currentTextChanged.connect(self.store_mayer_source)
        self.baseline_removal_chb = qtw.QCheckBox('Baseline Removal')
        self.baseline_removal_chb.stateChanged.connect(
            lambda val: self.store_baseline(val, self.baseline_removal_chb.isChecked()))
        self.notch_filter_chb = qtw.QCheckBox('Notch Filter')
        self.notch_filter_chb.stateChanged.connect(lambda val: self.store_notch(val, self.notch_filter_chb.isChecked()))
        self.low_pass_chb = qtw.QCheckBox('Low-pass Filter')
        self.low_pass_chb.stateChanged.connect(lambda val: self.store_low_pass(val, self.low_pass_chb.isChecked()))
        cut_off_label = qtw.QLabel('Cut-off Frequency (Hz)')
        self.cut_off_le = qtw.QLineEdit()
        self.cut_off_le.setEnabled(False)
        self.cut_off_le.setStyleSheet('background: #F0F0F0')
        self.cut_off_le.textChanged.connect(self.store_cut_off)

        # Layout
        grid_layout = qtw.QGridLayout()
        grid_layout.setHorizontalSpacing(12)
        grid_layout.setVerticalSpacing(8)
        grid_layout.setContentsMargins(40, 12, 20, 10)
        for setting in range(len(sig_proc_settings)):
            grid_layout.addWidget(sig_proc_settings[setting], setting, 0)
            grid_layout.setAlignment(sig_proc_settings[setting], qtc.Qt.AlignRight)
        grid_layout.addWidget(self.sig_ana_cb, 0, 1)
        grid_layout.addWidget(self.corr_mode_cb, 1, 1)
        grid_layout.addWidget(self.mayer_waves_cb, 2, 1)
        grid_layout.addWidget(self.baseline_removal_chb, 3, 0)
        grid_layout.addWidget(self.notch_filter_chb, 3, 1)
        grid_layout.addWidget(self.low_pass_chb, 4, 0)
        lower_right_layout = qtw.QHBoxLayout()
        lower_right_layout.setContentsMargins(0, 0, 0, 0)
        lower_right_layout.addWidget(cut_off_label)
        lower_right_layout.addWidget(self.cut_off_le)
        grid_layout.addLayout(lower_right_layout, 4, 1)
        sig_proc_gb.setLayout(grid_layout)
        self.setLayout(outer_layout)

    @qtc.pyqtSlot(str)
    def change_anylsis_method(self, current_method):
        '''
        Controls the enabling and disabling of the corresponding settings according the current selected analysis method
        @param current_method: current method selected in sig_ana_cb
        '''
        if current_method == 'TF (Transfer Function Models)':
            self.corr_mode_cb.setEnabled(True)
            self.corr_mode_cb.setCurrentIndex(0)
        elif current_method == 'CAR (Common Average Reference)':
            self.corr_mode_cb.setEnabled(False)
            self.corr_mode_cb.setCurrentIndex(0)
            self.mayer_waves_cb.setEnabled(False)

    @qtc.pyqtSlot(str)
    def change_correction_mode(self, current_mode):
        '''
        Checks the enabling and disabling behaviour of the entering parameters for physiological artefact removal
        according the correction mode selected in corr_mode_cb and emits the checkings to gui_part.settings
        @param current_mode: currently selected correction mode in corr_mode_cb
        '''
        enable_resp_peak = False
        enable_mayer = False
        if current_mode == 'Uncorrected':
            self.mayer_waves_cb.setEnabled(False)
            self.submit_mayer_source.emit({'mayer_waves_source': ''})
        elif current_mode == 'Respiration':
            self.mayer_waves_cb.setEnabled(False)
            enable_resp_peak = True
            self.submit_mayer_source.emit({'mayer_waves_source': ''})
        elif current_mode == 'Mayer Waves':
            self.mayer_waves_cb.setEnabled(True)
            enable_mayer = True
            self.submit_mayer_source.emit({'mayer_waves_source': str(self.mayer_waves_cb.currentText())})
        elif current_mode == 'Mayer and Respiration':
            self.mayer_waves_cb.setEnabled(True)
            enable_resp_peak = True
            enable_mayer = True
            self.submit_mayer_source.emit({'mayer_waves_source': str(self.mayer_waves_cb.currentText())})

        self.submit_possible_artefact_correction.emit([enable_mayer, enable_resp_peak])

    @qtc.pyqtSlot(str)
    def store_sig_ana_method(self, sig_ana_method):
        '''
        Stores signal analysis method
        @param sig_ana_method: selected signal analysis method
        '''
        self.submit_sig_ana_method.emit(
            {'signal_analysis_method': str(sig_ana_method)})

    @qtc.pyqtSlot(str)
    def store_corr_mode(self, corr_mode):
        '''
        Stores correction method
        @param corr_mode: selected correction method
        '''
        self.submit_corr_mode.emit({'correction_mode': str(corr_mode)})

    @qtc.pyqtSlot(str)
    def store_mayer_source(self, mayer_source):
        '''
        Stores Mayer waves source. Only Heart Rate is available at the moment.
        @param mayer_source: selected Mayer waves source. At the moment is always Heart Rate
        '''
        self.submit_mayer_source.emit({'mayer_waves_source': str(mayer_source)})

    @qtc.pyqtSlot(int, bool)
    def store_baseline(self, state_changed, is_checked):
        '''
        Stores if baseline removal is checked
        @param state_changed: int, return value 0 or 2 if state of checkbox changed (2) or not (0)
        @param is_checked: bool, if baseline removal checkbox is checked
        '''
        if state_changed == 0 and is_checked:
            self.submit_baseline.emit({'baseline': is_checked})
        elif state_changed == 0 and not is_checked:
            self.submit_baseline.emit({'baseline': False})
        elif state_changed == 2 and is_checked:
            self.submit_baseline.emit({'baseline': is_checked})
        elif state_changed == 2 and not is_checked:
            self.submit_baseline.emit({'baseline': False})

    @qtc.pyqtSlot(int, bool)
    def store_notch(self, state_changed, is_checked):
        '''
        Stores if noch frequency removal is checked
        @param state_changed: int, return value 0 or 2 if state of checkbox changed (2) or not (0)
        @param is_checked: bool, if notch frequency removal checkbox is checked
        '''
        if state_changed == 0 and is_checked:
            self.submit_notch.emit({'notch': is_checked})
        elif state_changed == 0 and not is_checked:
            self.submit_notch.emit({'notch': False})
        elif state_changed == 2 and is_checked:
            self.submit_notch.emit({'notch': is_checked})
        elif state_changed == 2 and not is_checked:
            self.submit_notch.emit({'notch': False})

    @qtc.pyqtSlot(int, bool)
    def store_low_pass(self, state_changed, is_checked):
        '''
        Stores if applying a low-pass filter is checked and handles the enabling and disabling of the corresponding
        cut-off frequency line entry
        @param state_changed: int, return value 0 or 2 if state of checkbox changed (2) or not (0)
        @param is_checked: bool, if low-pass filter checkbox is checked
        '''
        if state_changed == 0 and is_checked:
            self.submit_low_pass.emit({'low_pass': is_checked})
            self.cut_off_le.setEnabled(True)
            self.cut_off_le.setStyleSheet('background: white')
        elif state_changed == 0 and not is_checked:
            self.submit_low_pass.emit({'low_pass': False})
            self.cut_off_le.setEnabled(False)
            self.cut_off_le.setStyleSheet('background: #F0F0F0')
            self.cut_off_le.setText('')
        elif state_changed == 2 and is_checked:
            self.submit_low_pass.emit({'low_pass': is_checked})
            self.cut_off_le.setEnabled(True)
            self.cut_off_le.setStyleSheet('background: white')
        elif state_changed == 2 and not is_checked:
            self.submit_low_pass.emit({'low_pass': False})
            self.cut_off_le.setEnabled(False)
            self.cut_off_le.setStyleSheet('background: #F0F0F0')
            self.cut_off_le.setText('')

    @qtc.pyqtSlot(str)
    def store_cut_off(self, cut_off):
        '''
        Stores the entered cut-off frequency and checks for correct input
        @param cut_off: str, entered cut-off frequency
        '''
        # check if double
        try:
            if cut_off == '':
                cut_off = ''
            else:
                cut_off = float(cut_off)
            self.submit_cut_off.emit({'cut_off_frequency': cut_off})
        except:
            self.msg_wrong_input = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input format',
                                                   'Only int or float numbers are allowed.')
            self.msg_wrong_input.exec_()
            self.cut_off_le.setText('')
