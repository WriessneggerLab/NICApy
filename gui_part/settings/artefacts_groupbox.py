from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class Artefacts(qtw.QWidget):
    '''
    Class for building the Artefacts Groupbox
    Inherited from QWidget.

    --------
    Methods:
    --------

    build_artefacts_gb
    communicate_meth_excl_channs(self, val, is_checked)
    nr_trials_checked(self, val, is_checked)
    get_nr_trials(self, nr_trials)
    enter_nr_trials(self, nr_trials)
    check_input_ok(self, single, grouped, nr_trials)
    cancel_input_nr_trials_dialog(self)
    show_nr_trials_warning(self)
    get_optode_failure(self)
    optode_dialog(self)
    check_input_optode(self, failed, replace)
    cancel_input_optode_dialog(self)

    '''

    submit_method_excluded_channels = qtc.pyqtSignal(bool)
    submit_excluded_trials = qtc.pyqtSignal(dict)
    submit_nr_trials_to_check_func = qtc.pyqtSignal(int)
    submit_nr_trials_checked = qtc.pyqtSignal(int, bool)
    submit_nr_trials_checked_try = qtc.pyqtSignal(int)
    submit_optode_failure_val = qtc.pyqtSignal(dict)
    submit_optode_failure_list = qtc.pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super(Artefacts, self).__init__(*args, **kwargs)
        self.build_artefacts_gb()

    def build_artefacts_gb(self):
        '''
        Creates the Artefacts Groupbox layout and its widgets
        '''
        artefacts_gb = qtw.QGroupBox('Artefacts')
        outer_layout = qtw.QVBoxLayout()
        outer_layout.addWidget(artefacts_gb)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout = qtw.QGridLayout()
        grid_layout.setSpacing(8)
        grid_layout.setContentsMargins(30, 0, 30, 0)
        grid_layout.addWidget(qtw.QLabel('Exclude:'), 0, 0)
        self.trials = qtw.QCheckBox('Trials')
        self.trials.setEnabled(False)
        self.trials.stateChanged.connect(
            lambda val: self.nr_trials_checked(val, self.trials.isChecked()))
        self.channels = qtw.QCheckBox('Channels')
        self.channels.stateChanged.connect(
            lambda val: self.communicate_meth_excl_channs(val, self.channels.isChecked()))
        self.cons_opt_failure = qtw.QCheckBox('Consider Optode Failure')
        self.cons_opt_failure.released.connect(self.get_optode_failure)
        grid_layout.addWidget(self.trials, 0, 1)
        grid_layout.addWidget(self.channels, 0, 2)
        grid_layout.addWidget(self.cons_opt_failure, 1, 0, 1, 3)
        artefacts_gb.setLayout(grid_layout)
        self.setLayout(outer_layout)

    @qtc.pyqtSlot(int, bool)
    def communicate_meth_excl_channs(self, val, is_checked):
        '''
        Communicates if channels checkbox for excluding channels is checked or not
        @param val: int, value of status_changed
        @param is_checked: bool, value if exclude channels checkbox is checked
        '''
        if val == 0 and not is_checked:
            excl_channs = False
            self.submit_method_excluded_channels.emit(excl_channs)
        elif val == 0 and is_checked:
            excl_channs = True
            self.submit_method_excluded_channels.emit(excl_channs)
        elif val == 2 and is_checked:
            excl_channs = True
            self.submit_method_excluded_channels.emit(excl_channs)
        elif val == 2 and not is_checked:
            excl_channs = False
            self.submit_method_excluded_channels.emit(excl_channs)

    @qtc.pyqtSlot(int, bool)
    def nr_trials_checked(self, val, is_checked):
        '''
        Excluding trials is not implemented yet. This method is for future versions.
        Communicates if trials is checked for trial exclusion
        @param val: int, value of status_changed
        @param is_checked: bool, value if exclude trials checkbox is checked
        '''
        if val == 0 and not is_checked:
            self.submit_excluded_trials.emit({'excluded_trials': 0})  # add to properties
        elif val == 0 and is_checked:
            self.submit_excluded_trials.emit(
                {'excluded_trials': int(str(self.trials.text()))})
        elif val == 2 and is_checked:
            # val is True
            self.submit_nr_trials_checked.emit(val, is_checked)
        elif val == 2 and not is_checked:
            self.submit_excluded_trials.emit({'excluded_trials': 0})

    @qtc.pyqtSlot(str)
    def get_nr_trials(self, nr_trials):
        '''
        Excluding trials is not implemented yet. This method is for future versions.
        Get nr of trials from basics box
        @param nr_trials: int, number of trials per condition used in the experiment
        '''
        if nr_trials is '' or nr_trials is "" or nr_trials is None:
            self.show_nr_trials_warning()
        else:
            self.enter_nr_trials(nr_trials)

    def enter_nr_trials(self, nr_trials):
        '''
        Excluding trials is not implemented yet. This method is for future versions.
        Opens dialog to enter desired number of trials to be excluded
        @param nr_trials: number of trials desired to be excluded
        '''
        self.input_nr_trials = qtw.QDialog()
        self.input_nr_trials.setWindowTitle('Exclude Trials')
        outer_layout = qtw.QVBoxLayout()
        outer_layout.setSpacing(5)
        self.ok_button = qtw.QPushButton('Ok')
        self.cancel_button = qtw.QPushButton('Cancel')
        self.input_nr_trials.setLayout(outer_layout)
        self.nr_trials_single = []
        self.nr_trials_grouped = []

        single_name = qtw.QLabel('Select single Trials (Input Example: 1,3,7)')
        self.enter_single = qtw.QLineEdit()
        self.enter_single.setStyleSheet('min-height: 15px; max-height: 15px')
        grouped_name = qtw.QLabel('Select a group of Trials (Input Example: 9-13)')
        self.enter_grouped = qtw.QLineEdit()
        self.enter_grouped.setStyleSheet('min-height: 15px; max-height: 15px')
        outer_layout.addWidget(single_name, 0)
        outer_layout.addWidget(self.enter_single, 1)
        outer_layout.addWidget(grouped_name, 2)
        outer_layout.addWidget(self.enter_grouped, 3)

        self.ok_button.clicked.connect(self.input_nr_trials.accept)
        self.cancel_button.clicked.connect(self.input_nr_trials.reject)

        bottom_layout = qtw.QHBoxLayout()
        bottom_layout.addWidget(self.ok_button, 0)
        bottom_layout.addWidget(self.cancel_button, 1)
        outer_layout.addLayout(bottom_layout)
        result = self.input_nr_trials.exec_()
        if result is 1:
            self.check_input_ok(str(self.enter_single.text()), str(self.enter_grouped.text()), nr_trials)
        if result is 0:
            self.cancel_input_nr_trials_dialog()

    def check_input_ok(self, single, grouped, nr_trials):
        '''
        Excluding trials is not implemented yet. This method is for future versions.
        Checks if the entered input is ok.
        @param single: str, string of number of trials if only one single number is defined
        @param grouped: str, string of number of trials if only more numbers are defined
        @param nr_trials: number of trials for the selected condition
        '''
        if grouped is '' and single is not '' or grouped is "" and single is not "":
            try:
                single_nrs = [int(num) for num in single.split(',')]
                trials_excluded = single_nrs
                if any(tr > int(nr_trials) for tr in trials_excluded):
                    self.input_to_big = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input',
                                                        'Input nr exceeds nr of trials.')
                    self.input_to_big.exec_()

                else:
                    self.submit_excluded_trials.emit({'excluded_trials': trials_excluded})

            except:
                self.msg_wrong_format = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input format',
                                                        'Check input format again.')
                self.msg_wrong_format.exec_()

        elif single is '' and grouped is not '' or single is "" and grouped is not "":
            try:
                grouped_nrs = [int(boundaries) for boundaries in grouped.split('-')]
                trials_excluded = [trials for trials in range(grouped_nrs[0], grouped_nrs[1] + 1)]
                if any(tr > int(nr_trials) for tr in trials_excluded):
                    self.input_to_big = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input',
                                                        'Input nr exceeds nr of trials.')
                    self.input_to_big.exec_()

                else:
                    self.submit_excluded_trials.emit({'excluded_trials': trials_excluded})

            except:
                self.msg_wrong_format.exec_()

        else:
            self.msg_only_one_input = qtw.QMessageBox(qtw.QMessageBox.Warning, 'Wrong Input',
                                                      'Only one of the two lines can be filled.')
            self.msg_only_one_input.exec_()

    def cancel_input_nr_trials_dialog(self):
        '''
        Excluding trials is not implemented yet. This method is for future versions.
        Returns if Cancel is pressed during exclude trials dialog.
        '''
        self.input_nr_trials.reject

    def show_nr_trials_warning(self):
        '''
        Excluding trials is not implemented yet. This method is for future versions.
        Shows warning if something is wrong during exclude trials dialog
        '''
        msg_nr_trials_missing = qtw.QMessageBox()
        msg_nr_trials_missing.setText('Please, enter first an integer number of trials!')
        msg_nr_trials_missing.setInformativeText('Continue with clicking ok')
        msg_nr_trials_missing.setIcon(qtw.QMessageBox.Warning)
        msg_nr_trials_missing.exec_()

    @qtc.pyqtSlot()
    def get_optode_failure(self):
        '''
        Checks if consider optode failure is selected by hand, because otherwise signal conflicts arise between by hand
        selection or by loading optode failure from settings
        '''
        if self.cons_opt_failure.isChecked():
            self.optode_dialog()
        else:
            self.submit_optode_failure_val.emit({'optode_failure_val': False})
            self.submit_optode_failure_list.emit({'optode_failure_list': [[], [[]]]})

    def optode_dialog(self):
        '''
        Creates consider optode failure dialog
        '''
        text_info = 'Each failed Channel must have a set of Channels to interpolate the failed Channel. E.g.: Failed Channels = "3,5"; Channels to interpolate = "1-17,17-21". Channel 3 will be interpolated with the Channels 1-17, Channel 5 with 17-21).'
        self.optode_info = qtw.QMessageBox(qtw.QMessageBox.Information, 'Help Consider Optode Failure', text_info)
        self.optode_info.exec_()
        self.optode_failure_input = qtw.QDialog()
        self.optode_failure_input.setWindowTitle('Consider Optode Failure')
        outer_layout = qtw.QVBoxLayout()
        outer_layout.setSpacing(5)
        ok_button = qtw.QPushButton('Ok')
        cancel_button = qtw.QPushButton('Cancel')
        self.optode_failure_input.setLayout(outer_layout)
        self.failed_optodes = []
        self.replacing_optodes = []

        optode_name = qtw.QLabel('Failed Channels (e.g.: 3,5)')
        self.enter_failed_channs = qtw.QLineEdit()
        self.enter_failed_channs.setStyleSheet('min-height: 15px; max-height: 15px')
        replace_name = qtw.QLabel('Channels to interpolate (e.g.: 1-17, 17-21')
        self.enter_replace_channs = qtw.QLineEdit()
        self.enter_replace_channs.setStyleSheet('min-height: 15px; max-height: 15px')
        outer_layout.addWidget(optode_name, 0)
        outer_layout.addWidget(self.enter_failed_channs, 1)
        outer_layout.addWidget(replace_name, 2)
        outer_layout.addWidget(self.enter_replace_channs, 3)

        ok_button.clicked.connect(self.optode_failure_input.accept)
        cancel_button.clicked.connect(self.optode_failure_input.reject)

        bottom_layout = qtw.QHBoxLayout()
        bottom_layout.addWidget(ok_button, 0)
        bottom_layout.addWidget(cancel_button, 1)
        outer_layout.addLayout(bottom_layout)
        result = self.optode_failure_input.exec_()
        if result is 1:
            self.check_input_optode(str(self.enter_failed_channs.text()), str(self.enter_replace_channs.text()))
        if result is 0:
            self.cancel_input_optode_dialog()

    def check_input_optode(self, failed, replace):
        '''
        Checks the entered input in the consider optode dialog
        @param failed: str, string of the channels considered for optode failure
        @param replace: str, string of the channels considered for raplicing the channels considered for optode failure
        '''
        if failed is '' and replace is '' or failed is '' and replace is not '' or failed is not '' and replace is '':
            self.msg_wrong_format = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input',
                                                    'Please fill in both lines.')
            rej = self.msg_wrong_format.exec_()
        else:
            try:
                failed_optodes = [int(num) for num in failed.split(',')]
                replace_optodes = [repl for repl in replace.split(',')]
                replace_intervals = [[int(boundaries) for boundaries in outerlist.split('-')] for outerlist in
                                     replace_optodes]
                replace_optodes = [[interv for interv in range(outer[0], outer[1] + 1)] for outer in replace_intervals]
                self.submit_optode_failure_val.emit({'optode_failure_val': True})
                self.submit_optode_failure_list.emit({'optode_failure_list': [failed_optodes, replace_optodes]})

            except:
                self.msg_wrong_format = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input format',
                                                        'Check input format again.')
                self.msg_wrong_format.exec_()

    def cancel_input_optode_dialog(self):
        '''
        Returns when Cancel is pressed during consider optode failure dialog
        '''
        self.optode_failure_input.reject
        self.cons_opt_failure.setChecked(False)