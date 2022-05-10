from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
import os
import webbrowser
import json
from data_sharing_objects.data_singleton import Data
from data_sharing_objects.status_singleton import Status


class MenuBar(qtw.QMenuBar):
    '''
    Class containing all the menu bar widgets and all its features
    Inherited from QMenuBar

    --------
    Methods:
    --------

    file_menu(self)
    meas_data_menu(self)
    user_settings_menu(self)
    grand_average_menu(self)
    statistics_menu(self)
    open_path(self)
    update_enable_clear(self, enable)
    ttest_dialog(self)
    get_filename_for_ttest(self)
    show_ttest_output(self, ttest_output)
    save_settings_as(self, properties)
    load_settings(self)
    prepare_for_ga_start(self)
    prepare_for_ga_stop(self)
    get_analysis_path(self)
    get_hdr_file(self)
    get_xdf_file(self)
    def_conditions(self)
    input_cond_and_marker(self, number)
    create_new_cond_and_marker
    cancel_cond_dialog(self)
    communicate_condition_and_marker(self, condition, marker)
    show_cond_marker_warning(self, number)
    def_ROIs_dialog(self)
    input_rois(self, number)
    create_new_rois(self, roi, num)
    cancel_roi_dialog(self)
    show_roi_warning(self, number)

    '''
    data = Data()
    status = Status()
    start_path = os.path.dirname(os.path.realpath(__file__))
    data.add(nica_directory_path=start_path)

    submit_hdr_file = qtc.pyqtSignal(str)
    submit_xdf_files = qtc.pyqtSignal(list)
    submit_analysis_path = qtc.pyqtSignal(str)
    submit_status = qtc.pyqtSignal(bool)
    submit_condition_and_marker_to_gui = qtc.pyqtSignal(list, list)
    submit_cond_and_marker = qtc.pyqtSignal(object, object)
    submit_markers = qtc.pyqtSignal(dict)
    submit_cond_to_basics_gb = qtc.pyqtSignal(list, list)
    submit_available_conditions = qtc.pyqtSignal(dict)
    # submit_close_all_wins_clicked = qtc.pyqtSignal(bool)

    submit_loaded_nr_trials = qtc.pyqtSignal(str)
    submit_loading_settings_activated = qtc.pyqtSignal(bool)
    submit_loaded_available_conditions_and_markers_to_basics_gb = qtc.pyqtSignal(list, list)
    submit_loaded_available_conditions_to_properties = qtc.pyqtSignal(dict)
    submit_loaded_available_markers_to_properties = qtc.pyqtSignal(dict)
    submit_loaded_signal_imaging = qtc.pyqtSignal(str)
    submit_loaded_chosen_condition = qtc.pyqtSignal(str)
    submit_loaded_probe_set = qtc.pyqtSignal(str)
    submit_loaded_nr_trials = qtc.pyqtSignal(str)
    submit_loaded_task_name = qtc.pyqtSignal(str)
    submit_loaded_mayer_waves_source = qtc.pyqtSignal(str)
    submit_loaded_sig_analysis_method = qtc.pyqtSignal(str)
    submit_loaded_correction_mode = qtc.pyqtSignal(str)
    submit_loaded_baseline = qtc.pyqtSignal(bool)
    submit_loaded_notch = qtc.pyqtSignal(bool)
    submit_loaded_low_pass = qtc.pyqtSignal(bool)
    submit_loaded_cut_off_frequency = qtc.pyqtSignal(str)
    submit_loaded_mayer_lower = qtc.pyqtSignal(str)
    submit_loaded_mayer_upper = qtc.pyqtSignal(str)
    submit_loaded_mayer_corr_band = qtc.pyqtSignal(str)
    submit_loaded_resp_lower = qtc.pyqtSignal(str)
    submit_loaded_resp_upper = qtc.pyqtSignal(str)
    submit_loaded_resp_corr_band = qtc.pyqtSignal(str)
    submit_loaded_if_chans_excl_to_artebox = qtc.pyqtSignal(bool)
    submit_loaded_excl_channels = qtc.pyqtSignal(list)
    submit_loaded_if_chans_disp_to_artebox = qtc.pyqtSignal(bool)
    submit_loaded_disp_channels = qtc.pyqtSignal(list)
    submit_loaded_task_length = qtc.pyqtSignal(str)
    submit_loaded_pre_task_length = qtc.pyqtSignal(str)
    submit_loaded_post_task_length = qtc.pyqtSignal(str)
    submit_loaded_marker_offset = qtc.pyqtSignal(bool)
    submit_loaded_excl_trials_checked = qtc.pyqtSignal(bool)
    submit_loaded_excluded_trials_to_properties = qtc.pyqtSignal(list)
    submit_loaded_optode_failure_checked = qtc.pyqtSignal(bool)
    submit_loaded_optode_failure_val_to_properties = qtc.pyqtSignal(dict)
    submit_loaded_optode_failure_list_to_properties = qtc.pyqtSignal(dict)
    submit_loaded_gen_biosig_figures = qtc.pyqtSignal(bool)
    submit_loaded_gen_spectra_figures = qtc.pyqtSignal(bool)
    submit_loaded_gen_single_conc_ch_figures = qtc.pyqtSignal(bool)
    submit_loaded_gen_std_plot = qtc.pyqtSignal(bool)
    submit_loaded_freq_limit_spec_figures = qtc.pyqtSignal(str)
    submit_loaded_lower_spectra = qtc.pyqtSignal(str)
    submit_loaded_upper_spectra = qtc.pyqtSignal(str)

    ### Grand Average
    submit_ga_status = qtc.pyqtSignal(bool)
    submit_ga_status_to_properties = qtc.pyqtSignal(dict)
    submit_delete_ga_status_to_properties = qtc.pyqtSignal(str)
    submit_status_changed = qtc.pyqtSignal(bool)
    submit_rois_to_properties = qtc.pyqtSignal(dict)
    submit_delete_rois_to_properties = qtc.pyqtSignal(str)
    submit_set_initial_settings = qtc.pyqtSignal()

    ### T-Test
    submit_filename_to_ttest = qtc.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(MenuBar, self).__init__(*args, **kwargs)
        self.file_menu()
        self.meas_data_menu()
        self.user_settings_menu()
        self.grand_average_menu()
        self.statistics_menu()

    def file_menu(self):
        '''
        Defines File menu with features 'Select Analysis Path', 'Open Analysis Path', 'Close all Figures' and 'Close GUI'
        'Close all Figures' is still enabled, because plots are not shown during analysis
        '''
        self.file = qtw.QMenu('File')
        self.addMenu(self.file)
        self.select_analysis_path_action = qtw.QAction('Select Analysis Path')
        self.file.addAction(self.select_analysis_path_action)
        self.select_analysis_path_action.triggered.connect(self.get_analysis_path)
        self.open_analysis_path = qtw.QAction('Open Analysis Path')
        self.file.addAction(self.open_analysis_path)
        self.open_analysis_path.setEnabled(False)
        self.open_analysis_path.triggered.connect(self.open_path)
        self.close_all_figures = qtw.QAction('Close all Figures')
        self.close_all_figures.setEnabled(False)
        self.file.addAction(self.close_all_figures)
        # self.close_all_figures.triggered.connect(self.close_all_windows)
        self.close_gui = qtw.QAction('Close GUI')
        self.file.addAction(self.close_gui)

    def meas_data_menu(self):
        '''
        Defines Measurement Data menu with features 'Load' (HDR File, XDF File(s)), 'Clear' and 'Define Conditions'
        '''
        self.measurement_data = qtw.QMenu('Measurement Data')
        self.addMenu(self.measurement_data)
        self.load_measdata = qtw.QMenu('Load')
        self.measurement_data.addMenu(self.load_measdata)
        self.hdr_file_action = qtw.QAction('HDR File')
        self.xdf_file_action = qtw.QAction('XDF File(s)')
        self.load_measdata.addAction(self.hdr_file_action)
        self.hdr_file_action.triggered.connect(self.get_hdr_file)
        self.load_measdata.addAction(self.xdf_file_action)
        self.xdf_file_action.triggered.connect(self.get_xdf_file)
        self.clear = qtw.QAction('Clear')
        self.clear.setEnabled(False)
        self.measurement_data.addAction(self.clear)
        self.def_conditions_action = qtw.QAction('Define Conditions')
        self.def_conditions_action.triggered.connect(self.def_conditions)
        self.measurement_data.addAction(self.def_conditions_action)

    def user_settings_menu(self):
        '''
        Defines User Settings menu with features 'Save as' and 'Load'
        '''
        self.user_settings = qtw.QMenu('User Settings')
        self.addMenu(self.user_settings)
        self.save_as = qtw.QAction('Save as')
        self.load = qtw.QAction('Load')
        self.user_settings.addAction(self.save_as)
        self.user_settings.addAction(self.load)
        self.load.triggered.connect(self.load_settings)

    def grand_average_menu(self):
        '''
        Defines Grand Average menu with features 'Define ROIs', 'Start' and 'Stop'
        '''
        self.grand_average = qtw.QMenu('Grand Average')
        self.addMenu(self.grand_average)
        self.define_ROIs = qtw.QAction('Define ROIs')
        self.define_ROIs.setEnabled(False)
        self.start = qtw.QAction('Start')
        self.stop = qtw.QAction('Stop')
        self.stop.setEnabled(False)
        self.grand_average.addAction(self.define_ROIs)
        self.grand_average.addAction(self.start)
        self.start.triggered.connect(self.prepare_for_ga_start)  # disable all settings
        self.grand_average.addAction(self.stop)  # reactivate old properties, delete properties_ga
        self.stop.triggered.connect(self.prepare_for_ga_stop)
        self.define_ROIs.triggered.connect(self.def_ROIs_dialog)

    def statistics_menu(self):
        '''
        Defines Statistics menu with features 't-test'
        '''
        self.statistics = qtw.QMenu('Statistics')
        self.addMenu(self.statistics)
        self.ttest = qtw.QAction('t-test')
        # self.anova = qtw.QAction('ANOVA')
        self.statistics.addAction(self.ttest)
        self.ttest.triggered.connect(self.ttest_dialog)
        # self.staticitis.addAction(self.anova)

    @qtc.pyqtSlot()
    def open_path(self):
        '''
        Opens selected analysis path if one exists
        '''
        if hasattr(self.data, 'analysis_path'):
            path = self.data.analysis_path
            webbrowser.open('file:///' + path)
        elif hasattr(self.data, 'analysis_path_main'):
            path = self.data.analysis_path_main
            webbrowser.open('file:///' + path)
        else:
            return

    @qtc.pyqtSlot(bool)
    def update_enable_clear(self, enable):
        '''
        Allows if feature 'Clear' is enabled or not
        @param enable: Bool in order to obtain if files are selected and therefore 'Clear' can be enabled
        '''
        if enable:
            self.clear.setEnabled(True)
        else:
            self.clear.setEnabled(False)

    @qtc.pyqtSlot()
    def ttest_dialog(self):
        '''
        Opens the dialog for performing a modified t-test
        Tries first if a file is ready to load from a directly previously performed single analysis. If not,
        it asks for loading the file.
        '''
        try:
            filename = os.path.join(self.data.analysis_path, self.data.file_name + '_NIRx.pickle')
            ask = qtw.QMessageBox()
            ask.setIcon(qtw.QMessageBox.Question)
            ask.setText('Do you want do use the existing data file?')
            ask.setInformativeText('Press Ok if yes, Press Cancel if not')
            ask.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
            response = ask.exec_()
            if response == ask.Ok:
                self.submit_filename_to_ttest.emit(filename)
            elif response == ask.Cancel:
                self.get_filename_for_ttest()
        except:
            self.get_filename_for_ttest()

    def get_filename_for_ttest(self):
        '''
        Gets the filename of the desired file and submits the name to model_part.single_t_test(fname)
        '''
        filename, _ = qtw.QFileDialog.getOpenFileName(self, 'Select a pickle-File', '', 'pickle files (*.pickle)')
        if filename:
            self.submit_filename_to_ttest.emit(filename)

    @qtc.pyqtSlot(list)
    def show_ttest_output(self, ttest_output):
        '''
        Displays a short summary of the t-test results directly to the user inside the GUI
        @param ttest_output: list including the output results
        '''
        self.tt = qtw.QDialog()
        outer_layout = qtw.QVBoxLayout()
        outer_layout.setSpacing(5)
        self.tt.setLayout(outer_layout)
        tt_text = qtw.QTextEdit()
        tt_text.setReadOnly(True)
        for i in range(len(ttest_output)):
            tt_text.append(ttest_output[i])
        outer_layout.addWidget(tt_text)
        self.tt.exec_()

    '''def close_all_windows(self):
        plt.close(all)'''

    @qtc.pyqtSlot(object)
    def save_settings_as(self, properties):
        '''
        Saves the set settings to a json file.
        @param properties: dict object including all defined settings
        '''
        self.fname, _ = qtw.QFileDialog.getSaveFileName(self, 'Save File', '', 'JSON (.json)')
        if not self.fname.endswith('.json'):
            self.fname = self.fname + '.json'
        if self.fname is not '' or self.fname is not "":
            open_file = open(self.fname, "w")
            json.dump(properties, open_file, indent=4)
            open_file.close()

    @qtc.pyqtSlot()
    def load_settings(self):
        '''
        Loads saved settings from a json file and sets all parameters in the Settings Groupbox
        '''
        fname, _ = qtw.QFileDialog.getOpenFileName(self, 'Select a JSON-File', '', 'JSON Files (*.json)')
        if fname:
            with open(fname) as f:
                properties = json.load(f)

            self.submit_loaded_available_conditions_and_markers_to_basics_gb.emit(properties['available_conditions'],
                                                                                  properties['condition_markers'])
            # the next two signals need to be emitted separately to the properties object in NICA_GUI, because of the input dialog, otherwise this wouldn't work
            self.submit_loaded_available_conditions_to_properties.emit(
                {'available_conditions': properties['available_conditions']})  # emit to properties
            self.submit_loaded_available_markers_to_properties.emit(
                {'condition_markers': properties['condition_markers']})  # emit to properties

            self.submit_loaded_signal_imaging.emit(properties['signal_imaging'])
            self.submit_loaded_chosen_condition.emit(properties['chosen_condition'])
            self.submit_loaded_probe_set.emit(properties['probe_set'])
            self.submit_loaded_nr_trials.emit(str(properties['nr_trials']))
            self.submit_loaded_task_name.emit(properties['task_name'])
            self.submit_loaded_mayer_waves_source.emit(properties['mayer_waves_source'])
            self.submit_loaded_sig_analysis_method.emit(properties['signal_analysis_method'])
            self.submit_loaded_correction_mode.emit(properties['correction_mode'])
            self.submit_loaded_baseline.emit(properties['baseline'])
            self.submit_loaded_notch.emit(properties['notch'])
            self.submit_loaded_low_pass.emit(properties['low_pass'])
            self.submit_loaded_cut_off_frequency.emit(str(properties['cut_off_frequency']))
            self.submit_loaded_mayer_lower.emit(str(properties['mayer_lower']))
            self.submit_loaded_mayer_upper.emit(str(properties['mayer_upper']))
            self.submit_loaded_mayer_corr_band.emit(str(properties['mayer_corr_band']))
            self.submit_loaded_resp_lower.emit(str(properties['resp_lower']))
            self.submit_loaded_resp_upper.emit(str(properties['resp_upper']))
            self.submit_loaded_resp_corr_band.emit(str(properties['resp_corr_band']))
            # for excluded channels: list needs to be sorted, connect to properties and get_loaded_channels_excluded

            if len(properties['excluded_channels']) is not 0:
                self.submit_loaded_if_chans_excl_to_artebox.emit(True)
                self.submit_loaded_excl_channels.emit(properties['excluded_channels'])
            else:
                self.submit_loaded_if_chans_excl_to_artebox.emit(False)
                self.submit_loaded_excl_channels.emit([])

            # for displayed channels:list needs to be sorted, connect to properties and get_loaded_channels_displayed
            if len(properties['displayed_channels']) is not 0:
                self.submit_loaded_if_chans_disp_to_artebox.emit(True)
                self.submit_loaded_disp_channels.emit(properties['excluded_channels'])
            else:
                self.submit_loaded_if_chans_disp_to_artebox.emit(False)
                self.submit_loaded_disp_channels.emit([])

            self.submit_loaded_task_length.emit(str(properties['task_length']))
            self.submit_loaded_pre_task_length.emit(str(properties['pre_task_length']))
            self.submit_loaded_post_task_length.emit(str(properties['post_task_length']))
            self.submit_loaded_marker_offset.emit(properties['marker_offset'])
            if len(properties['excluded_trials']) is not 0:
                self.submit_loaded_excl_trials_checked.emit(True)  # add to checkbox
                self.submit_loaded_excluded_trials_to_properties.emit(
                    properties['excluded_trials'])  ## set check True if not empty
            else:
                self.submit_loaded_excl_trials_checked.emit(False)  # add to checkbox
                self.submit_loaded_excluded_trials_to_properties.emit([])  # connect to properties

            if properties['optode_failure_val'] is True:
                self.submit_loaded_optode_failure_checked.emit(True)  # emit to checkbox
                self.submit_loaded_optode_failure_val_to_properties.emit(
                    {'optode_failure_val': properties['optode_failure_val']})  # emit to properties
                self.submit_loaded_optode_failure_list_to_properties.emit(
                    {'optode_failure_list': properties['optode_failure_list']})  # emit to properties
            else:
                self.submit_loaded_optode_failure_checked.emit(False)  # emit to checkbox
                self.submit_loaded_optode_failure_val_to_properties.emit({'optode_failure_val': False})  # emit False
                self.submit_loaded_optode_failure_list_to_properties.emit(
                    {'optode_failure_list': [[], [[]]]})

            self.submit_loaded_gen_biosig_figures.emit(properties['generate_biosig_figures'])
            self.submit_loaded_gen_spectra_figures.emit(properties['generate_spectra_figures'])
            self.submit_loaded_gen_single_conc_ch_figures.emit(properties['generate_single_conc_change_figures'])
            self.submit_loaded_gen_std_plot.emit(properties['generate_std_plot'])
            self.submit_loaded_freq_limit_spec_figures.emit(str(properties['freq_limit_spectra_figures']))
            self.submit_loaded_lower_spectra.emit(str(properties['conc_range_lower']))
            self.submit_loaded_upper_spectra.emit(str(properties['conc_range_upper']))

    @qtc.pyqtSlot()
    def prepare_for_ga_start(self):
        '''
        Prepares everything inside the GUI to allow a Grand Average analysis in order to communicate that no single
        analysis is performed, but GA analysis
        '''
        self.load_measdata.setEnabled(False)
        if hasattr(self.status, 'analysis_path_main'):
            self.status.delete_item('analysis_path_main')
            self.data.delete_item('analysis_path_main')
        if hasattr(self.data, 'analysis_path'):
            self.data.delete_item('analysis_path')
        self.define_ROIs.setEnabled(True)
        self.stop.setEnabled(True)
        self.status.add(grand_average=True)
        self.submit_ga_status.emit(True)
        self.submit_ga_status_to_properties.emit({'grand_average': True})
        self.submit_status_changed.emit(True)

    @qtc.pyqtSlot()
    def prepare_for_ga_stop(self):
        '''
        Prepares everything to stop the Grand Average and allow again a single analysis.
        Deletes all attributes of the data object, created at Grand Average analysis.
        '''
        if hasattr(self.data, 'analysis_path_main'):
            self.data.delete_item('analysis_path_main')
        if hasattr(self.data, 'analysis_path_ga'):
            self.data.delete_item('analysis_path_ga')
        if hasattr(self.data, 'analysis_path_cond'):
            self.data.delete_item('analysis_path_cond')
        if hasattr(self.status, 'grand_average'):
            self.status.delete_item('grand_average')
        if hasattr(self.data, 'filenames_ga'):
            self.data.delete_item('filenames_ga')
        if hasattr(self.data, 'analysis_path'):
            self.data.delete_item('analysis_path')
        self.submit_ga_status.emit(
            False)  # Todo: connect to settings gb and probably to NICA_GuI to distinghuish between properties
        self.load_measdata.setEnabled(True)
        self.submit_delete_ga_status_to_properties.emit('grand_average')
        self.submit_delete_rois_to_properties.emit('grand_average_rois')
        self.submit_status_changed.emit(True)
        self.stop.setEnabled(False)

    @qtc.pyqtSlot()
    def get_analysis_path(self):
        '''
        Gets the analysis path and adds it to data object
        If no previous analysis path is chosen it opens the file dialog in the NICApy directory path
        Submits the analysis path to loadfiles.set_analysis_path in nica_ui.py
        '''
        start_path = os.path.dirname(os.path.realpath(__file__))
        folder_name = qtw.QFileDialog.getExistingDirectory(self, 'Select a Directory for your Analysis Files:',
                                                           start_path, qtw.QFileDialog.ShowDirsOnly)
        self.data.add(nica_directory_path=start_path)
        self.status.add(analysis_path=True)
        self.open_analysis_path.setEnabled(True)
        self.submit_analysis_path.emit(folder_name)

    @qtc.pyqtSlot()
    def get_hdr_file(self):
        '''
        Gets hdr file name and submits it to load_files in nica_ui.py
        '''
        # check if attributes exist, if attribute exists and is empty, then problem
        if hasattr(self.data, 'temp_path_hdr'):
            temporary_path = self.data.temp_path_hdr
        elif hasattr(self.data, 'temp_path_xdf'):
            temporary_path = self.data.temp_path_xdf
        elif hasattr(self.data, 'analysis_path_main'):
            temporary_path = self.data.analysis_path_main
        else:
            temporary_path = self.data.nica_directory_path
        hdr_file, _ = qtw.QFileDialog.getOpenFileName(self, 'Select a HDR File', temporary_path, 'HDR Files (*.hdr)')
        # to check if ok or cancel pressed
        if hdr_file:
            self.submit_hdr_file.emit(hdr_file)

    @qtc.pyqtSlot()
    def get_xdf_file(self):
        '''
        Gets xdf file name and submits it to load_files in nica_ui.py
        '''
        if hasattr(self.data, 'temp_path_xdf'):
            temporary_path = self.data.temp_path_xdf
        elif hasattr(self.data, 'temp_path_hdr'):
            temporary_path = self.data.temp_path_hdr
        elif hasattr(self.data, 'analysis_path_main'):
            temporary_path = self.data.analysis_path_main
        else:
            temporary_path = self.data.nica_directory_path

        xdf_files, _ = qtw.QFileDialog.getOpenFileNames(self, 'Please select your XDF File(s)', temporary_path,
                                                        'XDF Files (*.xdf)')
        # to check if ok or cancel pressed
        if xdf_files:
            self.submit_xdf_files.emit(xdf_files)

    @qtc.pyqtSlot()
    def def_conditions(self):
        '''
        Opens dialogs to define the number of conditions used during an experiment
        '''
        get_num_conds = qtw.QInputDialog()
        number, ok_pressed = get_num_conds.getInt(self, 'Define Conditions', 'Number of Conditions')

        if ok_pressed and number != 0:
            self.input_cond_and_marker(number)

        elif ok_pressed and number == 0:
            cond_warning = qtw.QMessageBox(qtw.QMessageBox.Warning, 'Input Warning', 'Please enter an integer number!')
            cond_warning.exec_()
            print('No condition specified.')

    def input_cond_and_marker(self, number):
        '''
        Creates the dialog for input the condition and condition marker definition according the defined number in
        def_conditions()
        @param number: number of used conditions during the measurement defined in def_conditions()
        @return:
        '''
        self.conditions = qtw.QDialog()
        outer_layout = qtw.QVBoxLayout()
        outer_layout.setSpacing(5)
        self.ok_button = qtw.QPushButton('Ok')
        self.cancel_button = qtw.QPushButton('Cancel')
        self.conditions.setLayout(outer_layout)
        layout_idx = 0
        self.condition_list = []
        self.marker_list = []
        for num in range(number):
            self.condition_list.append(qtw.QLineEdit())
            self.marker_list.append(qtw.QLineEdit())

        for indx in range(number):
            condition_name = qtw.QLabel('Name Condition %s' % str(indx + 1))
            enter_name = self.condition_list[indx]
            enter_name.setStyleSheet('min-height: 15px; max-height: 15px')
            marker_condition = qtw.QLabel('Marker Nr. Condtion %s' % str(indx + 1))
            enter_marker = self.marker_list[indx]
            enter_marker.setStyleSheet('min-height: 15px; max-height: 15px')
            outer_layout.addWidget(condition_name, layout_idx)
            outer_layout.addWidget(enter_name, layout_idx + 1)
            outer_layout.addWidget(marker_condition, layout_idx + 2)
            outer_layout.addWidget(enter_marker, layout_idx + 3)
            layout_idx += 4

        self.ok_button.clicked.connect(self.conditions.accept)
        self.cancel_button.clicked.connect(self.conditions.reject)

        bottom_layout = qtw.QHBoxLayout()
        bottom_layout.addWidget(self.ok_button, 0)
        bottom_layout.addWidget(self.cancel_button, 1)
        outer_layout.addLayout(bottom_layout)
        result = self.conditions.exec_()
        if result is 1:
            self.create_new_cond_and_marker(self.condition_list, self.marker_list, number)
        if result is 0:
            self.cancel_cond_dialog()

    def create_new_cond_and_marker(self, cond, marker, num):
        '''
        Checks the input of conditions and markers and submits to properties object if ok
        @param cond: list of the condition names defined in input_cond_and_marker(self, number)
        @param marker: list of the condition markers defined in input_cond_and_marker(self, number)
        @param num: number of conditions
        '''
        self.new_condition_list = [str(cond[i].text()) for i in range(len(cond))]
        cond_entry_ok = 0
        marker_entry_ok = 0
        for c in self.new_condition_list:
            if c is not '' or c is not "":
                cond_entry_ok += 1

        self.new_marker_list = [str(marker[i].text()) for i in range(len(marker))]

        for m in self.new_marker_list:
            if m is not '' or m is not "":
                marker_entry_ok += 1

        if int(cond_entry_ok) != num or int(marker_entry_ok) != num:
            self.show_cond_marker_warning(num)  # clears also new_condition_list
        else:
            self.communicate_condition_and_marker(self.new_condition_list, self.new_marker_list)
            self.submit_cond_to_basics_gb.emit(self.new_condition_list, self.new_marker_list)
            self.submit_markers.emit({'condition_markers': self.new_marker_list})
            self.submit_available_conditions.emit({'available_conditions': self.new_condition_list})
            self.conditions.close()

    def cancel_cond_dialog(self):
        '''
        Returns if Cancel is clicked during conditions dialog
        '''
        self.conditions.reject()

    def communicate_condition_and_marker(self, condition, marker):
        '''
        Submits conditions and markers to the gui part to show inside the GUI
        @param condition: list of conditions
        @param marker: list of markers
        '''
        self.submit_condition_and_marker_to_gui.emit(condition, marker)

    def show_cond_marker_warning(self, number):
        '''
        Gives a warning if the entries in the condition dialog were not correct
        @param number: number of conditions
        '''
        msg_cond_or_marker_missing = qtw.QMessageBox()
        msg_cond_or_marker_missing.setText('No empty line(s) allowed!')
        msg_cond_or_marker_missing.setIcon(qtw.QMessageBox.Warning)
        self.new_condition_list.clear()
        # print(self.new_condition_list)
        msg_cond_or_marker_missing.exec_()
        self.input_cond_and_marker(number)

    @qtc.pyqtSlot()
    def def_ROIs_dialog(self):
        '''
        Opens dialog to define the number of desired ROIs. If entered number is ok, the input dialog for defining the
        conditions gets opend, if not ok, a warning is given
        '''
        get_num_rois = qtw.QInputDialog()
        number, ok_pressed = get_num_rois.getInt(self, 'Define ROIs', 'Number of ROIs (Region of Interests)')

        if ok_pressed and number != 0:
            self.input_rois(number)

        elif ok_pressed and number is 0:
            cond_warning = qtw.QMessageBox(qtw.QMessageBox.Warning, 'Input Warning', 'Please enter an integer number!')
            cond_warning.exec_()
            print('No condition specified.')

    def input_rois(self, number):
        '''
        Opens input dialog to define the desired ROIs according the number of ROIs defined in def_ROIs_dialog(self)
        @param number: number of desired ROIs defined in def_ROIs_dialog(self)
        '''
        self.rois_dialog = qtw.QDialog()
        outer_layout = qtw.QVBoxLayout()
        outer_layout.setSpacing(5)
        self.info_roi = qtw.QLabel('Please enter the channels per ROI in the following format: 1,2,3 etc.')
        outer_layout.addWidget(self.info_roi)
        self.ok_button_roi = qtw.QPushButton('Ok')
        self.cancel_button_roi = qtw.QPushButton('Cancel')
        self.rois_dialog.setLayout(outer_layout)
        layout_idx = 0
        self.roi_list = []
        for num in range(number):
            self.roi_list.append(qtw.QLineEdit())

        for indx in range(number):
            roi_number = qtw.QLabel('ROI %s' % str(indx + 1))
            enter_roi = self.roi_list[indx]
            enter_roi.setStyleSheet('min-height: 15px; max-height: 15px')
            outer_layout.addWidget(roi_number, layout_idx)
            outer_layout.addWidget(enter_roi, layout_idx + 1)
            layout_idx += 2

        self.ok_button_roi.clicked.connect(self.rois_dialog.accept)
        self.cancel_button_roi.clicked.connect(self.rois_dialog.reject)

        bottom_layout = qtw.QHBoxLayout()
        bottom_layout.addWidget(self.ok_button_roi, 0)
        bottom_layout.addWidget(self.cancel_button_roi, 1)
        outer_layout.addLayout(bottom_layout)
        result = self.rois_dialog.exec_()
        if result is 1:
            self.create_new_rois(self.roi_list, number)
        if result is 0:
            self.cancel_roi_dialog()

    def create_new_rois(self, roi, num):
        '''
        Converts the ROI input string to lists for each ROI including its corresponding defined channels.
        If entries were ok, the lists are submitted to properties
        @param roi: list of the ROIs including its defined corresponding channel numbers
        @param num: number of desired ROIs
        @return:
        '''
        self.new_roi_list = [roi[i].text() for i in range(len(roi))]
        roi_entry_ok = 0
        char_set = '0123456789,'
        for r in range(len(self.new_roi_list)):
            if self.new_roi_list[r] != '' or self.new_roi_list[r] != "":
                if all((c in char_set) for c in self.new_roi_list[r]):
                    self.new_roi_list[r] = self.new_roi_list[r].split(',')
                    self.new_roi_list[r] = [int(i) for i in self.new_roi_list[r]]
                    roi_entry_ok += 1

        if int(roi_entry_ok) != num:
            self.show_roi_warning(num)  # clears also new_condition_list
        else:
            self.submit_rois_to_properties.emit({'grand_average_rois': self.new_roi_list})
            self.rois_dialog.close()

    def cancel_roi_dialog(self):
        '''
        Returns if Cancel is clicked during the ROI dialog
        '''
        self.rois_dialog.reject()

    def show_roi_warning(self, number):
        '''
        Gives a warning if the entries in the ROI dialog were not correct
        @param number: number of ROIs
        '''
        roi_wrong_input = qtw.QMessageBox()
        roi_wrong_input.setText('Check if input is empty or wrong input format!')
        roi_wrong_input.setIcon(qtw.QMessageBox.Warning)
        self.new_roi_list.clear()
        # print(self.new_roi_list)
        rej = roi_wrong_input.exec_()
        self.input_rois(number)
