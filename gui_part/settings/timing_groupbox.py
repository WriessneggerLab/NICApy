from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class Timing(qtw.QWidget):
    '''
    Class for building the Timing Groupbox
    Inherited from QWidget.

    --------
    Methods:
    --------

    build_timing_gb(self)
    store_task_length(self, task_length)
    store_pretask_length(self, pre_length)
    store_posttask_length(self, post_length)
    store_marker_offset(self, marker_offset)

    '''
    submit_task_length = qtc.pyqtSignal(dict)
    submit_pretask_length = qtc.pyqtSignal(dict)
    submit_posttask_length = qtc.pyqtSignal(dict)
    submit_marker_offset = qtc.pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super(Timing, self).__init__(*args, **kwargs)
        self.build_timing_gb()

    def build_timing_gb(self):
        '''
        Creates Timing Groupbox layout and its widgets
        '''
        timing_gb = qtw.QGroupBox('Timing')
        outer_layout = qtw.QVBoxLayout()
        outer_layout.addWidget(timing_gb)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout = qtw.QGridLayout()
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(50, 5, 40, 0)
        timing_settings = [qtw.QLabel('Task length (s)'), qtw.QLabel('Pre-task length (s)'),
                           qtw.QLabel('Post-task length (s)')]
        self.task_length = qtw.QLineEdit()
        self.pretask_length = qtw.QLineEdit()
        self.posttask_length = qtw.QLineEdit()
        self.task_length.textChanged.connect(self.store_task_length)
        self.pretask_length.textChanged.connect(self.store_pretask_length)
        self.posttask_length.textChanged.connect(self.store_posttask_length)
        self.consider_marker_offset = qtw.QCheckBox('Consider Marker Offset')
        self.consider_marker_offset.stateChanged.connect(self.store_marker_offset)
        for Label in range(len(timing_settings)):
            grid_layout.addWidget(timing_settings[Label], Label, 0)
            grid_layout.setAlignment(timing_settings[Label], qtc.Qt.AlignRight)
        grid_layout.addWidget(self.task_length, 0, 1)
        grid_layout.addWidget(self.pretask_length, 1, 1)
        grid_layout.addWidget(self.posttask_length, 2, 1)
        grid_layout.addWidget(self.consider_marker_offset, 3, 0, 1, 2)
        timing_gb.setLayout(grid_layout)
        self.setLayout(outer_layout)

    @qtc.pyqtSlot(str)
    def store_task_length(self, task_length):
        '''
        Stores the entered task length
        @param task_length: entered input in task_length
        '''
        try:
            if task_length == '':
                task_length = ''
            else:
                task_length = int(task_length)
            self.submit_task_length.emit({'task_length': task_length})
        except:
            msg_not_int = qtw.QMessageBox(qtw.QMessageBox.Warning, 'Input Error',
                                          'The entered number needs to be an integer.')
            res = msg_not_int.exec_()
            self.task_length.setText('')

    @qtc.pyqtSlot(str)
    def store_pretask_length(self, pre_length):
        '''
        Stores the entered pre-task length
        @param pre_length: entered input in pretask_length
        '''
        try:
            if pre_length == '':
                pre_length = ''
            else:
                pre_length = int(pre_length)
            self.submit_pretask_length.emit({'pre_task_length': pre_length})
        except:
            msg_not_int = qtw.QMessageBox(qtw.QMessageBox.Warning, 'Input Error',
                                          'The entered number needs to be an integer.')
            msg_not_int.exec_()
            self.pretask_length.setText('')

    @qtc.pyqtSlot(str)
    def store_posttask_length(self, post_length):
        '''
        Stores the enterec post-task length
        @param post_length: entered input in posttask_length
        '''
        try:
            if post_length == '':
                post_length = ''
            else:
                post_length = int(post_length)
            self.submit_posttask_length.emit({'post_task_length': post_length})
        except:
            msg_not_int = qtw.QMessageBox(qtw.QMessageBox.Warning, 'Input Error',
                                          'The entered number needs to be an integer.')
            msg_not_int.exec_()
            self.posttask_length.setText('')

    @qtc.pyqtSlot(int)
    def store_marker_offset(self, marker_offset):
        '''
        Stores if consider_marker_offset is selected or not
        @param marker_offset: int, return value of stateChanged at consider_marker_offset
        '''
        if marker_offset is 0:
            marker_offset = False
        if marker_offset is 2:
            marker_offset = True
        self.submit_marker_offset.emit({'marker_offset': marker_offset})