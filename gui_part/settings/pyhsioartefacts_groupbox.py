from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class PhysiologicalArtefacts(qtw.QWidget):
    '''
    Class for building the Physiological Artefacts Groupbox
    Inherited from QWidget.

    --------
    Methods:
    --------

    build_phyartef_gb(self)
    allow_physio_artefacts(self, correction_types)
    store_mayer_lower(self, mayer_lower)
    store_mayer_upper(self, mayer_upper)
    store_mayer_corr_band(self, mayer_corr_band)
    store_resp_lower(self, resp_lower)
    store_resp_upper(self, resp_upper)
    store_resp_corr_band(self, resp_corr_band)

    '''

    submit_resp_lower = qtc.pyqtSignal(dict)
    submit_resp_upper = qtc.pyqtSignal(dict)
    submit_resp_corr_band = qtc.pyqtSignal(dict)
    submit_mayer_lower = qtc.pyqtSignal(dict)
    submit_mayer_upper = qtc.pyqtSignal(dict)
    submit_mayer_corr_band = qtc.pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super(PhysiologicalArtefacts, self).__init__(*args, **kwargs)
        self.build_phyartef_gb()

    def build_phyartef_gb(self):
        '''
        Creates Physiological Artefacts Groupbox layout and its widgets
        '''
        phys_arte_gb = qtw.QGroupBox('Physiological Artefacts')
        outer_layout = qtw.QVBoxLayout()
        outer_layout.addWidget(phys_arte_gb)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout = qtw.QGridLayout()
        phys_arte_settings = [qtw.QLabel('Mayer Waves'), qtw.QLabel('Respiration Peak')]
        search_window_l = qtw.QLabel('Search Window (Hz)')
        correction_band_l = qtw.QLabel('Correction Band (Hz)')
        self.mayer_lower = qtw.QLineEdit()
        self.mayer_upper = qtw.QLineEdit()
        self.mayer_corr_band = qtw.QLineEdit()
        self.mayer_corr_band.setContentsMargins(40, 0, 40, 0)
        self.mayer_line = [self.mayer_lower, self.mayer_upper, self.mayer_corr_band]
        self.mayer_lower.textChanged.connect(self.store_mayer_lower)
        self.mayer_upper.textChanged.connect(self.store_mayer_upper)
        self.mayer_corr_band.textChanged.connect(self.store_mayer_corr_band)

        self.resppeak_lower = qtw.QLineEdit()
        self.resppeak_upper = qtw.QLineEdit()
        self.resppeak_corr_band = qtw.QLineEdit()
        self.resppeak_lower.textChanged.connect(self.store_resp_lower)
        self.resppeak_upper.textChanged.connect(self.store_resp_upper)
        self.resppeak_corr_band.textChanged.connect(self.store_resp_corr_band)
        self.resppeak_corr_band.setContentsMargins(40, 0, 40, 0)
        self.resppeak_line = [self.resppeak_lower, self.resppeak_upper, self.resppeak_corr_band]
        self.artefact_matrix = [self.mayer_line, self.resppeak_line]
        for line in self.artefact_matrix:
            for field in line:
                field.setReadOnly(True)
                field.setStyleSheet('background: #F0F0F0')
        grid_layout.setSpacing(5)
        grid_layout.setContentsMargins(30, 5, 10, 2)
        for setting in range(len(phys_arte_settings)):
            grid_layout.addWidget(phys_arte_settings[setting], setting + 1, 0)
            grid_layout.setAlignment(phys_arte_settings[setting], qtc.Qt.AlignRight)
            grid_layout.addWidget(qtw.QLabel('-'), setting + 1, 2)
        grid_layout.addWidget(search_window_l, 0, 1, 1, 3)
        grid_layout.setAlignment(search_window_l, qtc.Qt.AlignCenter)
        grid_layout.addWidget(correction_band_l, 0, 4, 1, 1)
        grid_layout.setAlignment(correction_band_l, qtc.Qt.AlignCenter)
        grid_layout.addWidget(self.mayer_lower, 1, 1)
        grid_layout.addWidget(self.mayer_upper, 1, 3)
        grid_layout.addWidget(self.mayer_corr_band, 1, 4)
        grid_layout.addWidget(self.resppeak_lower, 2, 1)
        grid_layout.addWidget(self.resppeak_upper, 2, 3)
        grid_layout.addWidget(self.resppeak_corr_band, 2, 4)
        phys_arte_gb.setLayout(grid_layout)
        self.setLayout(outer_layout)

    @qtc.pyqtSlot(list)  # delete this line if it does not work anymore
    def allow_physio_artefacts(self, correction_types):
        '''
        Gets input of Signal Processing Groupbox and allows if parameters can be entered or not according the currently
        correction method
        @param correction_types: list of bool values according mayer and respiration parameters getting from Signal
        Processing Groupbox
        '''
        for index, correction_type in enumerate(correction_types):
            if correction_type:
                for field in self.artefact_matrix[index]:
                    field.setReadOnly(False)
                    field.setStyleSheet('background: white')
            else:
                for field in self.artefact_matrix[index]:
                    field.setReadOnly(True)
                    field.setStyleSheet('background: #F0F0F0')
                    field.setText('')

    @qtc.pyqtSlot(str)
    def store_mayer_lower(self, mayer_lower):
        '''
        Stores lower frequency of Mayer interval and checks for correct input
        @param mayer_lower: str, entered lower frequency of Mayer interval
        '''
        try:
            if mayer_lower == '':
                mayer_lower = ''
            else:
                mayer_lower = float(mayer_lower)
            self.submit_mayer_lower.emit({'mayer_lower': mayer_lower})
        except:
            self.submit_mayer_lower.emit({'mayer_lower': ''})
            self.msg_wrong = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input format',
                                                   'Only int or float numbers are allowed.')
            self.msg_wrong.exec_()
            self.mayer_lower.setText('')

    @qtc.pyqtSlot(str)
    def store_mayer_upper(self, mayer_upper):
        '''
        Stores upper frequency of Mayer interval and checks for correct input
        @param mayer_upper: str, entered upper frequency of Mayer interval
        '''
        try:
            if mayer_upper == '':
                mayer_upper = ''
            else:
                mayer_upper = float(mayer_upper)
            self.submit_mayer_upper.emit({'mayer_upper': mayer_upper})
        except:
            self.submit_mayer_upper.emit({'mayer_upper': ''})
            self.msg_wrong = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input format',
                                                   'Only int or float numbers are allowed.')
            self.msg_wrong.exec_()
            self.mayer_upper.setText('')

    @qtc.pyqtSlot(str)
    def store_mayer_corr_band(self, mayer_corr_band):
        '''
        Stores correction band for Mayer correction and checks for correct input
        @param mayer_corr_band: str, entered correction band for Mayer correction
        '''
        try:
            if mayer_corr_band == '':
                mayer_corr_band = ''
            else:
                mayer_corr_band = float(mayer_corr_band)
            self.submit_mayer_corr_band.emit({'mayer_corr_band': mayer_corr_band})
        except:
            self.submit_mayer_corr_band.emit({'mayer_corr_band': ''})
            self.msg_wrong = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input format',
                                                   'Only int or float numbers are allowed.')
            self.msg_wrong.exec_()
            self.mayer_corr_band.setText('')

    @qtc.pyqtSlot(str)
    def store_resp_lower(self, resp_lower):
        '''
        Stores lower frequency of Respiration interval and checks for correct input
        @param resp_lower: str, entered lower frequency of Respiration interval
        '''
        try:
            if resp_lower == '':
                resp_lower = ''
            else:
                resp_lower = float(resp_lower)
            self.submit_resp_lower.emit({'resp_lower': resp_lower})
        except:
            self.submit_resp_lower.emit({'resp_lower': ''})
            self.msg_wrong = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input format',
                                                   'Only int or float numbers are allowed.')
            self.msg_wrong.exec_()
            self.resppeak_lower.setText('')

    @qtc.pyqtSlot(str)
    def store_resp_upper(self, resp_upper):
        '''
        Stores upper frequency of Respiration interval and checks for correct input
        @param resp_upper: str, entered upper frequency of Respiration interval
        '''
        try:
            if resp_upper == '':
                resp_upper = ''
            else:
                resp_upper = float(resp_upper)
            self.submit_resp_upper.emit({'resp_upper': resp_upper})
        except:
            self.submit_resp_upper.emit({'resp_upper': ''})
            self.msg_wrong = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input format',
                                                   'Only int or float numbers are allowed.')
            self.msg_wrong.exec_()
            self.resppeak_upper.setText('')

    @qtc.pyqtSlot(str)
    def store_resp_corr_band(self, resp_corr_band):
        '''
        Stores correction band for Respiration correction and checks for correct input
        @param resp_corr_band: str, entered correction band for Respiration correction
        '''
        try:
            if resp_corr_band == '':
                resp_corr_band = ''
            else:
                resp_corr_band = float(resp_corr_band)
            self.submit_resp_corr_band.emit({'resp_corr_band': resp_corr_band})
        except:
            self.submit_resp_corr_band.emit({'resp_corr_band': resp_corr_band})
            self.msg_wrong = qtw.QMessageBox(qtw.QMessageBox.Information, 'Wrong input format',
                                                   'Only int or float numbers are allowed.')
            self.msg_wrong.exec_()
            self.resppeak_corr_band.setText('')