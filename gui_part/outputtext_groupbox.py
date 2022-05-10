from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
import os
from data_sharing_objects.status_singleton import Status
from data_sharing_objects.data_singleton import Data

class OutputText(qtw.QWidget):
    '''
    Class to create the Output Text Groupbox
    Inherited from QWidget.

    --------
    Methods:
    --------

    build_output_gb(self)
    add_text(self, text_list)
    write_output_to_file(self)

    '''
    data = Data()
    status = Status()

    def __init__(self, *args, **kwargs):
        super(OutputText, self).__init__(*args, **kwargs)
        self.build_output_gb()

    def build_output_gb(self):
        '''
        Creates Output Text Groupbox layout and its widgets
        '''
        output_gb = qtw.QGroupBox('Output Text')
        output_gb.setProperty("cssClass", "outer")
        outer_layout = qtw.QVBoxLayout()
        outer_layout.addWidget(output_gb)
        outer_layout.setContentsMargins(10, 0, 10, 5)
        inner_layout = qtw.QVBoxLayout()
        self.text_field = qtw.QTextEdit()
        self.text_field.setReadOnly(True)
        inner_layout.addWidget(self.text_field)
        output_gb.setLayout(inner_layout)
        self.setLayout(outer_layout)

    @qtc.pyqtSlot(list)
    def add_text(self, text_list):
        '''
        Adds text to the Output Box
        @param text_list: list including the output to show
        '''
        for text in text_list:
            self.text_field.append(str(text))

    @qtc.pyqtSlot()
    def write_output_to_file(self):
        '''
        Writes the output text to a text file. Only after a standard single analysis and not after Grand Average
        analysis.
        '''
        if not hasattr(self.status, 'grand_average'):
            output_text = self.text_field.toPlainText()
            with open(os.path.join(self.data.analysis_path, self.data.file_name + '_Output_File.txt'), 'w') as f:
                f.writelines(output_text)