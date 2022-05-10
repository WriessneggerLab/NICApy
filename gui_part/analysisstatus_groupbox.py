from PyQt5 import QtWidgets as qtw
from data_sharing_objects.data_singleton import Data
from data_sharing_objects.status_singleton import Status


class AnalysisStatus(qtw.QWidget):
    '''
    Class for building the Analysis Status Groupbox
    Inherited from QWidget.

    --------
    Methods:
    --------

    build_anastatus_gb(self)
    update_analysis_status(self, status_changed)
    check_analysis_status(self, temp_stat)

    '''
    data = Data()
    status = Status()

    def __init__(self, *args, **kwargs):
        super(AnalysisStatus, self).__init__(*args, **kwargs)
        self.build_anastatus_gb()

    def build_anastatus_gb(self):
        '''
        Creates the layout of the Analysis Status Groupbox and its widgets
        '''
        analysis_status_gb = qtw.QGroupBox('Analysis Status')
        analysis_status_gb.setProperty("cssClass", "outer")
        self.initial_status = 'Select an Analysis Path and Load your Data-Files'
        self.analysis_status_label = qtw.QLabel(self.initial_status)  # self.initial_status
        self.analysis_status_label.setProperty("cssClass", "display")
        self.analysis_status_label.setStyleSheet('color: green')
        self.analysis_status_label.setWordWrap(True)

        # Layout
        inner_layout = qtw.QVBoxLayout()
        inner_layout.addWidget(self.analysis_status_label)
        analysis_status_gb.setLayout(inner_layout)
        outer_layout = qtw.QVBoxLayout()
        outer_layout.addWidget(analysis_status_gb)
        outer_layout.setContentsMargins(10, 0, 5, 0)
        self.setLayout(outer_layout)

    def update_analysis_status(self, status_changed):
        '''
        Updates the analysis status if it gets changed and sets the text for the analysis status shown inside the GUI
        @param status_changed: bool, True if status changed or False if not
        '''
        # status_changed: is True when something happened during file selecting process
        if status_changed:
            temporary_status = self.analysis_status_label.text()
            current_status = self.check_analysis_status(temporary_status)
            self.analysis_status_label.setText(current_status)

    def check_analysis_status(self, temp_stat):
        '''
        Checks the analysis status in order to decide which status should be shown inside the GUI
        @param temp_stat: temporary status tracks if path and files were opened and selected
        '''
        text_analysis_status = ['Ready to start Grand Average', 'Select an Analysis Path',
                                'Ready to start Analysis', 'Load your Data-Files',
                                'Select an Analysis Path and Load your Data-Files']
        analysis_status = temp_stat

        if hasattr(self.status, 'grand_average'):
            if hasattr(self.status, 'analysis_path_main'):
                analysis_status = text_analysis_status[0]
            else:
                analysis_status = text_analysis_status[1]
        else:
            if hasattr(self.status, 'xdf') and hasattr(self.status, 'hdr') and hasattr(self.status,
                                                                                       'analysis_path_main'):
                analysis_status = text_analysis_status[2]
            else:
                if hasattr(self.status, 'xdf') and hasattr(self.status, 'hdr') and not hasattr(self.status,
                                                                                               'analysis_path_main'):
                    analysis_status = text_analysis_status[1]
                elif not hasattr(self.status, 'xdf') and not hasattr(self.status, 'hdr') and hasattr(self.status,
                                                                                                     'analysis_path_main'):
                    analysis_status = text_analysis_status[3]
                elif not hasattr(self.status, 'xdf') and not hasattr(self.status, 'hdr') and not hasattr(self.status,
                                                                                                         'analysis_path_main'):
                    analysis_status = text_analysis_status[4]

        return analysis_status