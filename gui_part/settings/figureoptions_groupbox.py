from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class FigureOptions(qtw.QWidget):
    '''
    Class for building the Figure Options Groupbox
    Inherited from QWidget.

    --------
    Methods:
    --------

    build_figopt_gb(self)
    store_biosig_figs(self, state_changed, is_checked)
    store_spectra_figs(self, state_changed, is_checked)
    store_single_conc_ch_figs(self, state_changed, is_checked)
    store_std_plot(self, state_changed, is_checked)
    store_freq_limit(self, freq_limit)
    store_conc_limit_lower(self, lower)
    store_conc_limit_upper(self, upper)

    '''

    submit_biosig_figs = qtc.pyqtSignal(dict)
    submit_spectra_figs = qtc.pyqtSignal(dict)
    submit_single_conc_ch_figs = qtc.pyqtSignal(dict)
    submit_std_signal = qtc.pyqtSignal(dict)
    submit_freq_limit = qtc.pyqtSignal(dict)
    submit_conc_limit_lower = qtc.pyqtSignal(dict)
    submit_conc_limit_upper = qtc.pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super(FigureOptions, self).__init__(*args, **kwargs)
        self.build_figopt_gb()

    def build_figopt_gb(self):
        '''
        Creates the Figure Options Groupbox layout and its widgets
        '''
        fig_options_gb = qtw.QGroupBox('Figure Options')
        outer_layout = qtw.QVBoxLayout()
        outer_layout.addWidget(fig_options_gb)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        self.generate_biosig_figs = qtw.QCheckBox('Generate Biosignals Figures')
        self.generate_biosig_figs.stateChanged.connect(
            lambda val: self.store_biosig_figs(val, self.generate_biosig_figs.isChecked()))
        self.generate_spectra_figs = qtw.QCheckBox('Generate Spectra Figures')
        self.generate_spectra_figs.stateChanged.connect(
            lambda val: self.store_spectra_figs(val, self.generate_spectra_figs.isChecked()))
        self.generate_single_conc_ch_figs = qtw.QCheckBox('Generate single Conc. Change Figures')
        self.generate_single_conc_ch_figs.stateChanged.connect(
            lambda val: self.store_single_conc_ch_figs(val, self.generate_single_conc_ch_figs.isChecked()))
        self.plot_std_signal = qtw.QCheckBox('Plot STD Signal')
        self.plot_std_signal.stateChanged.connect(
            lambda val: self.store_std_plot(val, self.plot_std_signal.isChecked()))
        self.generate_topoplot_figs = qtw.QCheckBox('Generate Head Topoplot Figures')
        self.generate_topoplot_figs.setEnabled(False)
        self.frequency_limit_l = qtw.QLabel('Frequency Limit (Hz)')
        nr_topoplot_figs_l = qtw.QLabel('Nr. Topoplot Figures')
        nr_topoplot_figs_l.setEnabled(False)
        conc_range_l = qtw.QLabel('Conc. Range (mM*mm)')
        self.frequency_limit = qtw.QLineEdit()
        self.frequency_limit.setEnabled(False)
        self.frequency_limit.setStyleSheet('background: #F0F0F0')
        self.frequency_limit.textChanged.connect(self.store_freq_limit)
        self.nr_topoplot_figs = qtw.QLineEdit()
        self.conc_range_lower = qtw.QLineEdit()
        self.conc_range_lower.textChanged.connect(self.store_conc_limit_lower)
        self.conc_range_upper = qtw.QLineEdit()
        self.conc_range_upper.textChanged.connect(self.store_conc_limit_upper)
        self.nr_topoplot_figs.setEnabled(False)
        self.conc_range_lower.setEnabled(False)
        self.conc_range_upper.setEnabled(False)
        self.nr_topoplot_figs.setStyleSheet('background: #F0F0F0')
        self.conc_range_lower.setStyleSheet('background: #F0F0F0')
        self.conc_range_upper.setStyleSheet('background: #F0F0F0')

        grid_layout = qtw.QGridLayout()
        grid_layout.setVerticalSpacing(7)
        grid_layout.setContentsMargins(10, 5, 10, 0)
        grid_layout.addWidget(self.generate_biosig_figs, 0, 0, 1, 2)
        grid_layout.addWidget(self.generate_spectra_figs, 1, 0)
        grid_layout.addWidget(self.frequency_limit_l, 2, 0)
        grid_layout.setAlignment(self.frequency_limit_l, qtc.Qt.AlignRight)
        grid_layout.addWidget(self.frequency_limit, 2, 1, 1, 3)
        grid_layout.addWidget(self.generate_single_conc_ch_figs, 3, 0, 1, 4)
        grid_layout.addWidget(conc_range_l, 4, 0)
        grid_layout.setAlignment(conc_range_l, qtc.Qt.AlignRight)
        grid_layout.addWidget(self.conc_range_lower, 4, 1)
        grid_layout.addWidget(qtw.QLabel('-'), 4, 2)
        grid_layout.addWidget(self.conc_range_upper, 4, 3)
        grid_layout.addWidget(self.plot_std_signal, 5, 0)
        grid_layout.addWidget(self.generate_topoplot_figs, 6, 0, 1, 2)
        grid_layout.addWidget(nr_topoplot_figs_l, 7, 0)
        grid_layout.setAlignment(nr_topoplot_figs_l, qtc.Qt.AlignRight)
        grid_layout.addWidget(self.nr_topoplot_figs, 7, 1, 1, 3)
        fig_options_gb.setLayout(grid_layout)
        self.setLayout(outer_layout)

    @qtc.pyqtSlot(int, bool)
    def store_biosig_figs(self, state_changed, is_checked):
        '''
        Stores if generate biosignals is checked
        @param state_changed: int, return value 0 or 2 if state of checkbox changed (2) or not (0)
        @param is_checked: bool, if checkbox is checked
        '''
        if state_changed is 0 and is_checked:
            self.submit_biosig_figs.emit({'generate_biosig_figures': is_checked})
        elif state_changed is 0 and not is_checked:
            self.submit_biosig_figs.emit({'generate_biosig_figures': False})
        elif state_changed is 2 and is_checked:
            self.submit_biosig_figs.emit({'generate_biosig_figures': is_checked})
        elif state_changed is 2 and not is_checked:
            self.submit_biosig_figs.emit({'generate_biosig_figures': False})

    @qtc.pyqtSlot(int, bool)
    def store_spectra_figs(self, state_changed, is_checked):
        '''
        Stores if generate spectra figures is checked and handles enabling and disabling of frequency spectra input
        @param state_changed: int, return value 0 or 2 if state of checkbox changed (2) or not (0)
        @param is_checked: bool, if checkbox is checked
        '''
        if state_changed is 0 and is_checked:
            self.submit_spectra_figs.emit({'generate_spectra_figures': is_checked})
            self.frequency_limit.setEnabled(True)
            self.frequency_limit.setStyleSheet('background: white')
        elif state_changed is 0 and not is_checked:
            self.submit_spectra_figs.emit({'generate_spectra_figures': False})
            self.frequency_limit.setEnabled(False)
            self.frequency_limit.setStyleSheet('background: #F0F0F0')
            self.frequency_limit.setText('')
        elif state_changed is 2 and is_checked:
            self.submit_spectra_figs.emit({'generate_spectra_figures': is_checked})
            self.frequency_limit.setEnabled(True)
            self.frequency_limit.setStyleSheet('background: white')
        elif state_changed is 2 and not is_checked:
            self.submit_spectra_figs.emit({'generate_spectra_figures': False})
            self.frequency_limit.setEnabled(False)
            self.frequency_limit.setStyleSheet('background: #F0F0F0')
            self.frequency_limit.setText('')

    @qtc.pyqtSlot(int, bool)
    def store_single_conc_ch_figs(self, state_changed, is_checked):
        '''
        Stores if generate single concentration change figures is checked and handles enabling and disabling of lower
        and upper concentration range input
        @param state_changed: int, return value 0 or 2 if state of checkbox changed (2) or not (0)
        @param is_checked: bool, if checkbox is checked
        '''
        if state_changed is 0 and is_checked:
            self.submit_single_conc_ch_figs.emit({'generate_single_conc_change_figures': is_checked})
            self.conc_range_lower.setEnabled(True)
            self.conc_range_lower.setStyleSheet('background: white')
            self.conc_range_upper.setEnabled(True)
            self.conc_range_upper.setStyleSheet('background: white')
        elif state_changed is 0 and not is_checked:
            self.submit_single_conc_ch_figs.emit({'generate_single_conc_change_figures': False})
            self.conc_range_lower.setEnabled(False)
            self.conc_range_lower.setText('')
            self.conc_range_lower.setStyleSheet('background: #F0F0F0')
            self.conc_range_upper.setEnabled(False)
            self.conc_range_upper.setText('')
            self.conc_range_upper.setStyleSheet('background: #F0F0F0')
        elif state_changed is 2 and is_checked:
            self.submit_single_conc_ch_figs.emit({'generate_single_conc_change_figures': is_checked})
            self.conc_range_lower.setEnabled(True)
            self.conc_range_lower.setStyleSheet('background: white')
            self.conc_range_upper.setEnabled(True)
            self.conc_range_upper.setStyleSheet('background: white')
        elif state_changed is 2 and not is_checked:
            self.submit_single_conc_ch_figs.emit({'generate_single_conc_change_figures': False})
            self.conc_range_lower.setEnabled(False)
            self.conc_range_lower.setText('')
            self.conc_range_lower.setStyleSheet('background: #F0F0F0')
            self.conc_range_upper.setEnabled(False)
            self.conc_range_upper.setText('')
            self.conc_range_upper.setStyleSheet('background: #F0F0F0')

    @qtc.pyqtSlot(int, bool)
    def store_std_plot(self, state_changed, is_checked):
        '''
        Stores if generate std plots is checked
        @param state_changed: int, return value 0 or 2 if state of checkbox changed (2) or not (0)
        @param is_checked: bool, if checkbox is checked
        '''
        if state_changed is 0 and is_checked:
            self.submit_std_signal.emit({'generate_std_plot': is_checked})
        elif state_changed is 0 and not is_checked:
            self.submit_std_signal.emit({'generate_std_plot': False})
        elif state_changed is 2 and is_checked:
            self.submit_std_signal.emit({'generate_std_plot': is_checked})
        elif state_changed is 2 and not is_checked:
            self.submit_std_signal.emit({'generate_std_plot': False})

    @qtc.pyqtSlot(str)
    def store_freq_limit(self, freq_limit):
        '''
        Stores entered frequency limit
        @param freq_limit: str, entered frequency limit
        '''
        try:
            freq_limit = float(freq_limit)
            self.submit_freq_limit.emit({'freq_limit_spectra_figures': float(freq_limit)})
        except:
            self.submit_freq_limit.emit({'freq_limit_spectra_figures': ''})
            self.msg_wrong_format = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input format',
                                                    'Only int or float numbers are allowed.')
            rej = self.msg_wrong_format.exec_()

    @qtc.pyqtSlot(str)
    def store_conc_limit_lower(self, lower):
        '''
        Stores lower concentration change boundary
        @param lower: str, lower concentration change boundary
        '''
        self.submit_conc_limit_lower.emit({'conc_range_lower': str(lower)})

    @qtc.pyqtSlot(str)
    def store_conc_limit_upper(self, upper):
        '''
        Stores upper concentration change boundary
        @param upper: str, upper concentration change boundary
        '''
        self.submit_conc_limit_upper.emit({'conc_range_upper': str(upper)})