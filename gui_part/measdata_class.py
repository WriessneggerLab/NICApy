from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from data_sharing_objects.data_singleton import Data
from data_sharing_objects.status_singleton import Status
from data_sharing_objects.xdf_class import Xdf


class MeasurementData(qtw.QWidget):
    '''
    Class for building the Measurement Data Groupbox
    Inherited from QWidget.

    --------
    Methods:
    --------

    build_measdata_gb(self)
    update_hdr_labels_text(self, hdr_name, hdr_path)
    update_xdf_labels(self, xdf_names, xdf_path)
    clear_hdr_and_xdf(self)
    get_selected_xdf_files(self)

    '''
    data = Data()
    status = Status()
    submit_enable_clear = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(MeasurementData, self).__init__(*args, **kwargs)
        self.build_measdata_gb()

    def build_measdata_gb(self):
        '''
        Creates the Measurement Data Groupbox layout and its widgets
        '''
        # Outer Groupbox Measurement Data
        meas_data_outer = qtw.QGroupBox('Measurement Data')
        meas_data_outer.setProperty("cssClass", "outer")

        # Inner Groupboxes
        hdr_path_gb = qtw.QGroupBox('HDR File Path')
        self.hdr_path_label = qtw.QLabel()
        self.hdr_path_label.setWordWrap(True)
        self.hdr_path_label.setProperty("cssClass", "displayfiles")
        hdr_path_layout = qtw.QVBoxLayout()
        hdr_path_layout.addWidget(self.hdr_path_label)
        hdr_path_gb.setLayout(hdr_path_layout)

        hdr_name = qtw.QGroupBox('HDR File Name')
        self.hdr_name_label = qtw.QLabel()
        self.hdr_name_label.setProperty("cssClass", "displayfiles")
        self.hdr_name_label.setWordWrap(True)
        hdr_name_layout = qtw.QVBoxLayout()
        hdr_name_layout.addWidget(self.hdr_name_label)
        hdr_name.setLayout(hdr_name_layout)

        xdf_path = qtw.QGroupBox('XDF File(s) Path')
        self.xdf_path_label = qtw.QLabel()
        self.xdf_path_label.setProperty("cssClass", "displayfiles")
        self.xdf_path_label.setWordWrap(True)
        xdf_path_layout = qtw.QVBoxLayout()
        xdf_path_layout.addWidget(self.xdf_path_label)
        xdf_path.setLayout(xdf_path_layout)

        xdf_name = qtw.QGroupBox('XDF File Name(s)')
        xdf_name_layout = qtw.QVBoxLayout()

        self.multiple_selection_list = qtw.QListWidget()
        self.multiple_selection_list.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)
        self.multiple_selection_list.itemSelectionChanged.connect(self.get_selected_xdf_files)

        xdf_name_layout.addWidget(qtw.QLabel('Multiple Selection with holding CTRL/STRG'))
        xdf_name_layout.addWidget(self.multiple_selection_list)
        xdf_name_layout.setSpacing(2)
        xdf_name_layout.setContentsMargins(10, 5, 10, 10)
        xdf_name.setLayout(xdf_name_layout)

        outer_layout = qtw.QVBoxLayout()
        outer_layout.addWidget(meas_data_outer)
        outer_layout.setContentsMargins(10, 5, 5, 0)
        inner_layout = qtw.QVBoxLayout()
        inner_layout.addWidget(hdr_path_gb)
        inner_layout.addWidget(hdr_name)
        inner_layout.addWidget(xdf_path)
        inner_layout.addWidget(xdf_name)
        inner_layout.setStretch(0, 2)
        inner_layout.setStretch(1, 2)
        inner_layout.setStretch(2, 2)
        inner_layout.setStretch(3, 5)
        inner_layout.setContentsMargins(5, 5, 5, 5)
        meas_data_outer.setLayout(inner_layout)
        self.setLayout(outer_layout)

    @qtc.pyqtSlot(str, str)
    def update_hdr_labels_text(self, hdr_name, hdr_path):
        '''
        Updates and sets the hdr name and path inside the GUI
        @param hdr_name:
        @param hdr_path:
        '''
        self.hdr_name_label.clear()
        self.hdr_path_label.clear()
        self.hdr_name_label.setText(hdr_name)
        self.hdr_path_label.setText(hdr_path)
        self.submit_enable_clear.emit(True)

    @qtc.pyqtSlot(list, str)
    def update_xdf_labels(self, xdf_names, xdf_path):
        '''
        Updates and sets the xdf name and path inside the GUI
        @param xdf_names:
        @param xdf_path:
        '''
        self.xdf_path_label.clear()
        self.xdf_path_label.setText(xdf_path)
        self.multiple_selection_list.clear()
        self.multiple_selection_list.addItems(xdf_names)
        self.submit_enable_clear.emit(True)

    @qtc.pyqtSlot()
    def clear_hdr_and_xdf(self):
        '''
        Deletes the hdr and xdf names and paths in the data object and as well inside the GUI
        '''
        self.hdr_name_label.clear()
        self.hdr_path_label.clear()
        self.multiple_selection_list.clear()
        self.xdf_path_label.clear()
        if hasattr(self.data, 'xdf'):
            self.data.delete_item('xdf')
        if hasattr(self.data, 'hdr'):
            self.data.delete_item('hdr')
        if hasattr(self.data, 'temporary_path_all'):
            self.data.delete_item('temporary_path_all')
        if hasattr(self.data, 'temp_path_hdr'):
            self.data.delete_item('temp_path_hdr')
        if hasattr(self.data, 'temp_path_xdf'):
            self.data.delete_item('temp_path_xdf')
        if hasattr(self.data, 'xdf'):
            self.status.delete_item('xdf')
        if hasattr(self.data, 'hdr'):
            self.status.delete_item('hdr')

        self.submit_enable_clear.emit(False)

    @qtc.pyqtSlot()
    def get_selected_xdf_files(
            self):  # for now xdf-filenames need to be sorted already in the folder before loading them
        '''
        Gets which xdf files are selected
        '''
        if self.multiple_selection_list.count() != 0:
            if not hasattr(self.data, 'xdf'):
                self.data.xdf = Xdf()
            items = []
            for item in list(self.multiple_selection_list.selectedItems()):
                items.append(self.multiple_selection_list.item(self.multiple_selection_list.row(item)).text())
            items = sorted(items)
            # print(items)
            self.data.xdf.update({'selected_xdf_files': items})
            self.submit_enable_clear.emit(True)
