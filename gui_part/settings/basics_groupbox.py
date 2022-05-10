from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class Basics(qtw.QWidget):
    '''
    Class for building the Basics Groupbox
    Inherited from QWidget.

    --------
    Methods:
    --------

    build_basics_gb(self)
    store_signal_image(self, sig_img)
    store_condition(self, chosen_condition)
    store_probe_set(self, probe_set)
    store_nr_trials(self, nr_trials)
    store_task_name(self, task_name)
    get_conditions_and_markers(self, condition, marker)
    get_if_nr_trials_checked(self, val, is_checked)

    '''
    submit_signal_imaging = qtc.pyqtSignal(dict)
    submit_condition = qtc.pyqtSignal(dict)
    submit_probe_set = qtc.pyqtSignal(dict)
    submit_nr_trials = qtc.pyqtSignal(dict)
    submit_task_name = qtc.pyqtSignal(dict)
    submit_nr_trials_to_artebox = qtc.pyqtSignal(str)


    def __init__(self, *args, **kwargs):
        super(Basics, self).__init__(*args, **kwargs)
        self.build_basics_gb()

    def build_basics_gb(self):
        '''
        Creates Basics Groupbox layout and its widgets
        '''
        basics_gb = qtw.QGroupBox('Basics')
        outer_layout = qtw.QVBoxLayout()
        outer_layout.addWidget(basics_gb)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Basics Labels
        basics_settings = [qtw.QLabel('Signal Imaging'), qtw.QLabel('Condition'), qtw.QLabel('Probe Set'),
                           qtw.QLabel('Number of Trials'), qtw.QLabel('Task Name')]

        # Corresponding Widgets
        self.signal_imaging = qtw.QComboBox()
        self.signal_imaging.addItem('Averaging over Trials')
        self.signal_imaging.addItem('Continuous')
        self.signal_imaging.setStyleSheet("QComboBox::drop-down")
        self.signal_imaging.currentTextChanged.connect(self.store_signal_image)
        self.conditions_cb = qtw.QComboBox()
        self.conditions_cb.addItem('Default')
        self.conditions_cb.setEnabled(False)
        self.conditions_cb.setStyleSheet("QComboBox::drop-down")
        self.conditions_cb.currentTextChanged.connect(self.store_condition)

        self.available_conditions = []
        self.available_markers = []

        self.probe_set = qtw.QComboBox()
        possible_probe_sets = ['12', '24', '38', '47', '50', 'Laboratory new', 'NIRx Sports old', 'NIRx Sports new']
        for probe in possible_probe_sets:
            self.probe_set.addItem(probe)
        self.probe_set.setStyleSheet("QComboBox::drop-down")
        self.probe_set.currentTextChanged.connect(self.store_probe_set)
        self.nr_trials = qtw.QLineEdit()
        self.nr_trials.textChanged.connect(self.store_nr_trials)
        self.task_name = qtw.QLineEdit()
        self.task_name.textChanged.connect(self.store_task_name)

        # Layout
        grid_layout = qtw.QGridLayout()
        grid_layout.setVerticalSpacing(5)
        grid_layout.setHorizontalSpacing(12)
        grid_layout.setContentsMargins(30, 10, 12, 12)
        for setting in range(len(basics_settings)):
            grid_layout.addWidget(basics_settings[setting], setting, 0)
            grid_layout.setAlignment(basics_settings[setting], qtc.Qt.AlignRight)
        grid_layout.addWidget(self.signal_imaging, 0, 1)
        grid_layout.addWidget(self.conditions_cb, 1, 1)
        grid_layout.addWidget(self.probe_set, 2, 1)
        grid_layout.addWidget(self.nr_trials, 3, 1)
        grid_layout.addWidget(self.task_name, 4, 1)
        basics_gb.setLayout(grid_layout)
        self.setLayout(outer_layout)

    def store_signal_image(self, sig_img):
        '''
        Stores the selected signal imaging method
        @param sig_img: selected signal imaging method in signal_imaging combobox
        '''
        self.submit_signal_imaging.emit({'signal_imaging': str(sig_img)})

    def store_condition(self, chosen_condition):
        '''
        Stores the selected condition
        @param chosen_condition: selected condition in conditions_cb combobox
        '''
        self.submit_condition.emit({'chosen_condition': str(chosen_condition)})

    def store_probe_set(self, probe_set):
        '''
        Stores selected probe set
        @param probe_set: selected probe set in probe_set combobox
        @return:
        '''
        self.submit_probe_set.emit({'probe_set': str(probe_set)})

    def store_nr_trials(self, nr_trials):
        '''
        Stores the entered number of trials
        @param nr_trials: number of trials of one condition
        '''
        try:
            if nr_trials == '':
                nr_trials = ''
            else:
                nr_trials = int(nr_trials)
            self.submit_nr_trials.emit({'nr_trials': nr_trials})
        except:
            msg_not_int = qtw.QMessageBox(qtw.QMessageBox.Warning, 'Input Error',
                                          'The entered number needs to be an integer.')
            msg_not_int.exec_()
            self.nr_trials.setText('')


    def store_task_name(self, task_name):
        '''
        Stores the define task name
        @param task_name: task name
        '''
        self.submit_task_name.emit({'task_name': str(task_name)})

    def get_conditions_and_markers(self, condition, marker):
        '''
        Gets the conditions and markers lists defined in the menu bar
        @param condition: list of conditions defined
        @param marker: list of markers defined
        '''
        if len(condition) > 0:
            self.conditions_cb.setEnabled(True)
            self.conditions_cb.clear()
            for cond in condition:
                self.conditions_cb.addItem(cond)
            self.available_markers = marker
            self.available_conditions = condition
            print(condition)
            print(marker)

    @qtc.pyqtSlot(int, bool)
    def get_if_nr_trials_checked(self, val, is_checked):
        '''
        This is for future versions
        Communicates to the checkbox allowing exlcude trials in the Artefacts Groupbox.
        There the number of trials is needed in order to allow a correct entering of trials desired to be excluded
        @param val: int, StateChanged return value
        @param is_checked: bool, if excluding trials checkbox in Artefacts Groupbox is checked (True) or not (False)
        '''
        if val is 2 and is_checked:
            self.submit_nr_trials_to_artebox.emit(str(self.nr_trials.text()))
        elif val is 2 and not is_checked:
            pass
        elif val is 0 and is_checked:
            self.submit_nr_trials_to_artebox.emit(str(self.nr_trials.text()))
        elif val is 0 and not is_checked:
            pass
        elif val is 0:
            pass