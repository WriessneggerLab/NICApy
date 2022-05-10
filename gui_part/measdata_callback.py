from PyQt5 import QtCore as qtc
import os
from data_sharing_objects.data_singleton import Data
from data_sharing_objects.status_singleton import Status
from data_sharing_objects.xdf_class import Xdf
from data_sharing_objects.hdr_class import Hdr


class MenuMeasurementDataLoadHDR_Callback(qtc.QObject):
    '''
    Class for writing the selected paths and names of hdr, xdf and analysis path to data object and submits the strings
    in order Measurement Data object in order to show them inside the GUI
    Inherited from QObject.

    --------
    Methods:
    --------

    set_analysis_path(self, folder_name)
    show_hdr_file(self, hdr_file)
    show_xdf_file(self, xdf_files)

    '''

    submit_hdr_name_and_path = qtc.pyqtSignal(str, str)
    submit_xdf_name_and_path = qtc.pyqtSignal(list, str)
    submit_ana_status_and_mode = qtc.pyqtSignal(bool)
    submit_anapath_properties = qtc.pyqtSignal(dict)
    submit_hdr_name_dict = qtc.pyqtSignal(dict)
    submit_hdr_path_dict = qtc.pyqtSignal(dict)
    submit_xdf_name_dict = qtc.pyqtSignal(dict)
    submit_xdf_path_dict = qtc.pyqtSignal(dict)

    error = qtc.pyqtSignal(str)
    data = Data()
    status = Status()

    @qtc.pyqtSlot(str)
    def set_analysis_path(self, folder_name):
        '''
        Adds the selected analysis path to the data object and adds a bool value to status object for keeping track of
        the status
        Submits status_changed to analysis status groupbox and folder_name to properties
        @param folder_name: path where analysis path will be created
        '''
        # folder_name: name of the folder chosen by the user

        if folder_name:
            self.data.add(analysis_path_main=folder_name)
            self.status.add(analysis_path_main=True)
            status_changed = True
            self.submit_ana_status_and_mode.emit(status_changed)
            # self.submit_anapath_properties.emit({'analysis_path': folder_name})

    @qtc.pyqtSlot(str)
    def show_hdr_file(self, hdr_file):
        '''
        Adds the selected hdr file to the data object and adds a bool value to status object for keeping track of
        the status
        It also updates the temporary path in order to open the file dialog when loading as a next step the xdf file
        Submits status_changed to analysis status groupbox and hdr name and path to load_files to show inside the GUI
        @param hdr_file: path of the hdr file, consists of the path and the filename
        '''
        # hdr_file: hdr file selected by the user
        self.data.hdr = Hdr()
        hdr_name = os.path.basename(os.path.normpath(hdr_file))
        hdr_path = os.path.dirname(os.path.normpath(hdr_file))

        if not hdr_name.endswith('.hdr'):
            print('The type of the selected file must be HDR!')  # TODO: make QWarning with QMessage
        else:  # selection was ok
            self.data.hdr.update({'name': hdr_name})
            self.data.hdr.update({'path': hdr_path})
            self.data.add(temporary_path_all=hdr_path)
            self.data.add(temp_path_hdr=hdr_path)
            self.status.add(hdr=True)
            status_changed = True
        self.submit_hdr_name_and_path.emit(hdr_name, hdr_path)
        self.submit_ana_status_and_mode.emit(status_changed)
        # self.submit_hdr_name_dict.emit({'hdr_name': hdr_name})
        # self.submit_hdr_path_dict.emit({'hdr_path': hdr_path})

    @qtc.pyqtSlot(list)
    def show_xdf_file(self, xdf_files):
        '''
        Adds the selected xdf file to the data object and adds a bool value to status object for keeping track of
        the status
        It also updates the temporary path in order to open the file dialog when loading as a next step the hdr file
        Submits status_changed to analysis status groupbox and xdf name and path to load_files to show inside the GUI
        @param xdf_files: list including paths of the xdf files, consist of the path and the filenames
        '''
        # xdf_files: files selected by the user, could be multiple
        # but in this version of NICApy only one xdf can be analysed

        xdf_path = os.path.dirname(
            os.path.normpath(xdf_files[0]))  # path is always (has to be) the same for all xdf files of same run
        xdf_names = []
        for names in range(len(xdf_files)):
            xdf_names.append(os.path.basename(os.path.normpath(xdf_files[names])))
            if not xdf_names[names].endswith('.xdf'):
                print('The type of the selected file(s) must be XDF!')
                return
            # TODO: make QWarning and exit the function back to the filedialog

        false_input = [xdf_files[wrong_files] for wrong_files in range(len(xdf_files)) if
                       not xdf_files[wrong_files].endswith('.xdf')]
        listbox_max = len(xdf_names)

        # if not xdf_path:  # selection cancel
        #  None
        if false_input:  # type of file(s) is not xdf
            print('The type of the selected file(s) must be XDF!')
        else:  # selection was ok
            if not hasattr(self.data, 'xdf'):
                self.data.xdf = Xdf()
            self.data.xdf.update({'name': xdf_names})
            self.data.xdf.update({'path': xdf_path})
            self.data.add(temporary_path_all=xdf_path)
            self.data.add(temp_path_xdf=xdf_path)
            self.status.add(xdf=True)
            self.data.xdf.update(selected=True)
            status_changed = True
        self.submit_xdf_name_and_path.emit(xdf_names, xdf_path)
        self.submit_ana_status_and_mode.emit(status_changed)
        # self.submit_xdf_name_dict.emit({'xdf_name(s)': xdf_names})
        # self.submit_xdf_path_dict.emit({'xdf_path': xdf_path})
