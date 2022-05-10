from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from data_sharing_objects.status_singleton import Status

class StartAnalysis(qtw.QWidget):
    '''
    Class for building the Start Analysis Button Groupbox
    Inherited from QWidget.

    --------
    Methods:
    --------

    build_start_ana_gb(self)
    update_start_analysis(self, status_changed)
    check_start_analysis_button(self)

    '''
    status = Status()

    def __init__(self, *args, **kwargs):
        super(StartAnalysis, self).__init__(*args, **kwargs)
        self.build_start_ana_gb()

    def build_start_ana_gb(self):
        '''
        Creates the Start Analysis Button Groupbox including its widgets
        '''
        self.start_analysis_button = qtw.QPushButton('Start Analysis')
        self.start_analysis_button.setContentsMargins(0, 0, 0, 0)
        self.initial_mode = False  # False
        self.start_analysis_button.setEnabled(self.initial_mode)
        outer_layout = qtw.QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(self.start_analysis_button)
        self.setLayout(outer_layout)

    @qtc.pyqtSlot(bool)
    def update_start_analysis(self, status_changed):
        '''
        Sets the Start Analysis button enable or disabled depending on the current status, meaning if all files are
        loaded
        starting an analysis
        @param status_changed: bool, True if status changed
        '''
        if status_changed:
            current_mode = self.check_start_analysis_button()
            self.start_analysis_button.setEnabled(current_mode)


    def check_start_analysis_button(self):
        '''
        Checks the current status and returns True or False if the Start Analysis Button should be enabled or disabled
        '''
        if hasattr(self.status, 'grand_average'):
            if hasattr(self.status, 'analysis_path_main'):
                pushbutton_mode = True
            else:
                pushbutton_mode = False
        else:
            if hasattr(self.status, 'xdf') and hasattr(self.status, 'hdr') and hasattr(self.status,
                                                                                       'analysis_path_main'):
                pushbutton_mode = True

            else:
                pushbutton_mode = False
        return pushbutton_mode