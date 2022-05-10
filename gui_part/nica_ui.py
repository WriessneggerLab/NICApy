from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

### imports from modules (files) belonging to NICApy
from model_part.NICA_MODEL import NICAModel
from model_part.NICA_MODEL import TTest
from data_sharing_objects.status_singleton import Status
from data_sharing_objects.data_singleton import Data
from gui_part.menubar_class import MenuBar
from gui_part.settings_groupbox import Settings
from gui_part.outputtext_groupbox import OutputText
from data_sharing_objects.properties_class import Properties
from gui_part.measdata_class import MeasurementData
from gui_part.measdata_callback import MenuMeasurementDataLoadHDR_Callback
from gui_part.analysisstatus_groupbox import AnalysisStatus


class NICA_UI(qtw.QMainWindow):
    '''
    Class where everything of the application NICApy comes together. All the objects of the Groupboxes are created here
    and all main signal and slot communication happens inside this class.
    Inherited from QMainWindow.

    --------
    Methods:
    --------

    build_gui(self)
    show_error(self, err)
    data_and_properties_to_func(self)
    properties_to_save(self)
    check_properties(self, data, props)
    flatten_nested_list(self, nested_list)

    '''

    submit_properties_to_save = qtc.pyqtSignal(object)
    submit_data_and_props_to_check_props = qtc.pyqtSignal(object, object)
    submit_properties_to_model_ok = qtc.pyqtSignal(object, object)

    data = Data()
    status = Status()

    def __init__(self, *args, **kwargs):
        super(NICA_UI, self).__init__(*args, **kwargs)

        self.setWindowTitle("NICApy")
        self.setGeometry(0, 0, 1100, 720)
        self.build_gui()

    def build_gui(self):
        '''
        Builds the main layout of the whole GUI application NICApy including all the Groupboxes and Menus
        Creates all necessary objects and the main signal and slot connections
        Almost everything needed for running NICApy is included in this method
        '''

        ### set Style Properties with css Styles in gui_part.stylesheet
        # with min-height in QGroupBox you can specify the minimum size of the groupbox

        ### Layout
        layout = qtw.QGridLayout()
        self.meas_data_gb = MeasurementData()
        self.analysis_status_gb = AnalysisStatus()
        self.settings_gb = Settings()
        self.output_gb = OutputText()
        layout.addWidget(self.meas_data_gb, 0, 0)
        layout.addWidget(self.analysis_status_gb, 1, 0)
        layout.addWidget(self.settings_gb, 0, 1, 2, 1)
        layout.addWidget(self.output_gb, 2, 0, 1, 2)
        layout.setColumnStretch(0, 4)
        layout.setColumnStretch(1, 6)
        layout.setRowStretch(0, 11)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 3)
        layout.setSpacing(0)
        layout.setContentsMargins(5, 0, 5, 5)

        ### Menu Bar
        self.menubar = MenuBar()
        self.setMenuBar(self.menubar)
        self.menuBar().setNativeMenuBar(False)
        self.load_files = MenuMeasurementDataLoadHDR_Callback()


        ### Signal-Slot connections

        self.menubar.submit_hdr_file.connect(self.load_files.show_hdr_file)
        self.load_files.submit_hdr_name_and_path.connect(self.meas_data_gb.update_hdr_labels_text)
        self.menubar.submit_analysis_path.connect(self.load_files.set_analysis_path)
        self.menubar.submit_xdf_files.connect(self.load_files.show_xdf_file)
        self.load_files.submit_xdf_name_and_path.connect(self.meas_data_gb.update_xdf_labels)
        self.load_files.submit_ana_status_and_mode.connect(self.analysis_status_gb.update_analysis_status)
        self.load_files.submit_ana_status_and_mode.connect(self.settings_gb.start_ana_button.update_start_analysis)
        self.menubar.submit_cond_to_basics_gb.connect(self.settings_gb.basics_box.get_conditions_and_markers)
        self.menubar.save_as.triggered.connect(self.properties_to_save)
        self.menubar.clear.triggered.connect(self.meas_data_gb.clear_hdr_and_xdf)
        self.meas_data_gb.submit_enable_clear.connect(self.menubar.update_enable_clear)
        self.menubar.close_gui.triggered.connect(self.close)
        self.submit_properties_to_save.connect(self.menubar.save_settings_as)

        ### the next one is only printing for debugging, this is only for printing
        # self.settings_gb.start_ana_button.start_analysis_button.clicked.connect(self.submit_settings)

        ### Create properties, nica_model and t_test_obj objects
        self.properties = Properties()
        self.nica_model = NICAModel()
        self.t_test_obj = TTest()

        ### Basics
        self.settings_gb.basics_box.submit_signal_imaging.connect(self.properties.add_properties)
        self.settings_gb.basics_box.submit_condition.connect(self.properties.add_properties)
        self.menubar.submit_markers.connect(self.properties.add_properties)
        self.menubar.submit_available_conditions.connect(self.properties.add_properties)
        self.settings_gb.basics_box.submit_probe_set.connect(self.properties.add_properties)
        self.settings_gb.basics_box.submit_nr_trials.connect(self.properties.add_properties)
        self.settings_gb.basics_box.submit_task_name.connect(self.properties.add_properties)
        ### Signal Processing
        self.settings_gb.sig_proc_box.submit_sig_ana_method.connect(self.properties.add_properties)
        self.settings_gb.sig_proc_box.submit_corr_mode.connect(self.properties.add_properties)
        self.settings_gb.sig_proc_box.submit_mayer_source.connect(self.properties.add_properties)
        self.settings_gb.sig_proc_box.submit_baseline.connect(self.properties.add_properties)
        self.settings_gb.sig_proc_box.submit_notch.connect(self.properties.add_properties)
        self.settings_gb.sig_proc_box.submit_low_pass.connect(self.properties.add_properties)
        self.settings_gb.sig_proc_box.submit_cut_off.connect(self.properties.add_properties)
        ### Physiological Artefacts
        self.settings_gb.physio_arte_box.submit_resp_lower.connect(self.properties.add_properties)
        self.settings_gb.physio_arte_box.submit_resp_upper.connect(self.properties.add_properties)
        self.settings_gb.physio_arte_box.submit_resp_corr_band.connect(self.properties.add_properties)
        self.settings_gb.physio_arte_box.submit_mayer_lower.connect(self.properties.add_properties)
        self.settings_gb.physio_arte_box.submit_mayer_upper.connect(self.properties.add_properties)
        self.settings_gb.physio_arte_box.submit_mayer_corr_band.connect(self.properties.add_properties)

        ### Timing
        self.settings_gb.timing_box.submit_task_length.connect(self.properties.add_properties)
        self.settings_gb.timing_box.submit_pretask_length.connect(self.properties.add_properties)
        self.settings_gb.timing_box.submit_posttask_length.connect(self.properties.add_properties)
        self.settings_gb.timing_box.submit_marker_offset.connect(self.properties.add_properties)

        ### Excluded Channels
        self.settings_gb.channels_box.submit_excluded_channs.connect(self.properties.add_properties)
        self.settings_gb.channels_box.submit_displayed_channs.connect(self.properties.add_properties)
        ### Excluded Trials
        self.settings_gb.artefacts_box.submit_excluded_trials.connect(self.properties.add_properties)
        ### Optode Failure
        self.settings_gb.artefacts_box.submit_optode_failure_val.connect(self.properties.add_properties)
        self.settings_gb.artefacts_box.submit_optode_failure_list.connect(self.properties.add_properties)

        ### Figure settings
        self.settings_gb.fig_opt_box.submit_biosig_figs.connect(self.properties.add_properties)
        self.settings_gb.fig_opt_box.submit_spectra_figs.connect(self.properties.add_properties)
        self.settings_gb.fig_opt_box.submit_single_conc_ch_figs.connect(self.properties.add_properties)
        self.settings_gb.fig_opt_box.submit_std_signal.connect(self.properties.add_properties)
        self.settings_gb.fig_opt_box.submit_freq_limit.connect(self.properties.add_properties)
        self.settings_gb.fig_opt_box.submit_conc_limit_lower.connect(self.properties.add_properties)
        self.settings_gb.fig_opt_box.submit_conc_limit_upper.connect(self.properties.add_properties)

        ### Load Settings Connections
        # Basics GB
        self.menubar.submit_loaded_nr_trials.connect(self.settings_gb.basics_box.nr_trials.setText)
        self.menubar.submit_loaded_available_conditions_and_markers_to_basics_gb.connect(
            self.settings_gb.basics_box.get_conditions_and_markers)
        self.menubar.submit_loaded_available_conditions_to_properties.connect(self.properties.add_properties)
        self.menubar.submit_loaded_available_markers_to_properties.connect(self.properties.add_properties)
        self.menubar.submit_loaded_signal_imaging.connect(self.settings_gb.basics_box.signal_imaging.setCurrentText)
        self.menubar.submit_loaded_chosen_condition.connect(self.settings_gb.basics_box.conditions_cb.setCurrentText)
        self.menubar.submit_loaded_probe_set.connect(self.settings_gb.basics_box.probe_set.setCurrentText)
        self.menubar.submit_loaded_nr_trials.connect(self.settings_gb.basics_box.nr_trials.setText)
        self.menubar.submit_loaded_task_name.connect(self.settings_gb.basics_box.task_name.setText)
        # Signal Processing GB
        self.menubar.submit_loaded_mayer_waves_source.connect(
            self.settings_gb.sig_proc_box.mayer_waves_cb.setCurrentText)
        self.menubar.submit_loaded_sig_analysis_method.connect(self.settings_gb.sig_proc_box.sig_ana_cb.setCurrentText)
        self.menubar.submit_loaded_correction_mode.connect(self.settings_gb.sig_proc_box.corr_mode_cb.setCurrentText)
        self.menubar.submit_loaded_baseline.connect(self.settings_gb.sig_proc_box.baseline_removal_chb.setChecked)
        self.menubar.submit_loaded_notch.connect(self.settings_gb.sig_proc_box.notch_filter_chb.setChecked)
        self.menubar.submit_loaded_low_pass.connect(self.settings_gb.sig_proc_box.low_pass_chb.setChecked)
        self.menubar.submit_loaded_cut_off_frequency.connect(self.settings_gb.sig_proc_box.cut_off_le.setText)
        # Physiological Artefacts GB
        self.menubar.submit_loaded_mayer_lower.connect(self.settings_gb.physio_arte_box.mayer_lower.setText)
        self.menubar.submit_loaded_mayer_upper.connect(self.settings_gb.physio_arte_box.mayer_upper.setText)
        self.menubar.submit_loaded_mayer_corr_band.connect(self.settings_gb.physio_arte_box.mayer_corr_band.setText)
        self.menubar.submit_loaded_resp_lower.connect(self.settings_gb.physio_arte_box.resppeak_lower.setText)
        self.menubar.submit_loaded_resp_upper.connect(self.settings_gb.physio_arte_box.resppeak_upper.setText)
        self.menubar.submit_loaded_resp_corr_band.connect(self.settings_gb.physio_arte_box.resppeak_corr_band.setText)
        # Channel GB
        self.menubar.submit_loaded_if_chans_excl_to_artebox.connect(self.settings_gb.artefacts_box.channels.setChecked)
        self.menubar.submit_loaded_excl_channels.connect(
            self.settings_gb.channels_box.get_loaded_checked_channels_exclude)
        self.menubar.submit_loaded_disp_channels.connect(
            self.settings_gb.channels_box.get_loaded_checked_channels_displayed)
        # Timing GB
        self.menubar.submit_loaded_task_length.connect(self.settings_gb.timing_box.task_length.setText)
        self.menubar.submit_loaded_pre_task_length.connect(self.settings_gb.timing_box.pretask_length.setText)
        self.menubar.submit_loaded_post_task_length.connect(self.settings_gb.timing_box.posttask_length.setText)
        self.menubar.submit_loaded_marker_offset.connect(self.settings_gb.timing_box.consider_marker_offset.setChecked)
        # Artefacts GB
        self.menubar.submit_loaded_excl_trials_checked.connect(self.settings_gb.artefacts_box.trials.setChecked)
        self.menubar.submit_loaded_excluded_trials_to_properties.connect(self.properties.add_properties)
        self.menubar.submit_loaded_optode_failure_checked.connect(
            self.settings_gb.artefacts_box.cons_opt_failure.setChecked)
        self.menubar.submit_loaded_optode_failure_val_to_properties.connect(self.properties.add_properties)
        self.menubar.submit_loaded_optode_failure_list_to_properties.connect(self.properties.add_properties)
        # Figure Options GB
        self.menubar.submit_loaded_gen_biosig_figures.connect(
            self.settings_gb.fig_opt_box.generate_biosig_figs.setChecked)
        self.menubar.submit_loaded_gen_spectra_figures.connect(
            self.settings_gb.fig_opt_box.generate_spectra_figs.setChecked)
        self.menubar.submit_loaded_gen_single_conc_ch_figures.connect(
            self.settings_gb.fig_opt_box.generate_single_conc_ch_figs.setChecked)
        self.menubar.submit_loaded_gen_std_plot.connect(self.settings_gb.fig_opt_box.plot_std_signal.setChecked)
        self.menubar.submit_loaded_freq_limit_spec_figures.connect(self.settings_gb.fig_opt_box.frequency_limit.setText)
        self.menubar.submit_loaded_lower_spectra.connect(self.settings_gb.fig_opt_box.conc_range_lower.setText)
        self.menubar.submit_loaded_upper_spectra.connect(self.settings_gb.fig_opt_box.conc_range_upper.setText)

        ### Qthread used for allowing multiple processes run parallel, otherwise the analysis status would not be
        # updated, because the GUI would freeze

        self.thread = qtc.QThread()
        self.nica_model.moveToThread(self.thread)

        ### Start Analysis Button
        self.settings_gb.start_ana_button.start_analysis_button.clicked.connect(
            self.data_and_properties_to_func)
        self.settings_gb.start_ana_button.start_analysis_button.clicked.connect(
            self.output_gb.text_field.clear)  # todo: check that
        self.submit_data_and_props_to_check_props.connect(self.check_properties)
        self.submit_properties_to_model_ok.connect(self.nica_model.run)
        self.submit_properties_to_model_ok.connect(self.thread.start)
        self.thread.started.connect(lambda: self.settings_gb.start_ana_button.setEnabled(False))

        ### Connections for displaying analysis status during processing steps
        self.nica_model.submit_error_to_messagebox.connect(self.show_error)
        self.nica_model.submit_load_text_to_ana_status.connect(self.analysis_status_gb.analysis_status_label.setText)
        self.nica_model.submit_eval_path_to_ana_status.connect(self.analysis_status_gb.analysis_status_label.setText)
        self.nica_model.submit_probeset_text_to_ana_status.connect(
            self.analysis_status_gb.analysis_status_label.setText)
        self.nica_model.submit_bio_text_to_ana_status.connect(self.analysis_status_gb.analysis_status_label.setText)
        self.nica_model.submit_base_text_to_ana_status.connect(self.analysis_status_gb.analysis_status_label.setText)
        self.nica_model.submit_raw_text_to_ana_status.connect(self.analysis_status_gb.analysis_status_label.setText)
        self.nica_model.submit_physio_text_to_ana_status.connect(self.analysis_status_gb.analysis_status_label.setText)
        self.nica_model.submit_cleaned_text_to_ana_status.connect(self.analysis_status_gb.analysis_status_label.setText)
        self.nica_model.submit_compare_text_to_ana_status.connect(self.analysis_status_gb.analysis_status_label.setText)
        self.nica_model.submit_head_text_to_ana_status.connect(self.analysis_status_gb.analysis_status_label.setText)
        self.nica_model.submit_output_text_to_ana_status.connect(self.analysis_status_gb.analysis_status_label.setText)
        self.nica_model.submit_text_to_outputbox.connect(self.output_gb.add_text)

        ### Grand Average
        self.menubar.submit_ga_status.connect(self.settings_gb.allow_ga_settings)
        self.menubar.submit_status_changed.connect(self.analysis_status_gb.update_analysis_status)
        self.menubar.submit_ga_status_to_properties.connect(self.properties.add_properties)
        self.menubar.submit_delete_ga_status_to_properties.connect(self.properties.delete_ga_property)
        self.menubar.submit_rois_to_properties.connect(self.properties.add_properties)
        self.menubar.submit_delete_rois_to_properties.connect(self.properties.delete_ga_property)
        self.menubar.start.triggered.connect(self.meas_data_gb.clear_hdr_and_xdf)
        self.settings_gb.submit_optode_failure_val_to_props_ga.connect(self.properties.add_properties)
        self.settings_gb.submit_optode_failure_list_to_props_ga.connect(self.properties.add_properties)
        self.nica_model.finished.connect(self.output_gb.write_output_to_file)
        self.nica_model.finished.connect(self.thread.quit)
        self.thread.finished.connect(lambda: self.settings_gb.start_ana_button.setEnabled(True))

        ### T-Test
        self.menubar.submit_filename_to_ttest.connect(self.t_test_obj.do_ttest)
        self.t_test_obj.submit_ttest_show.connect(self.menubar.show_ttest_output)
        self.t_test_obj.submit_error_to_messagebox.connect(self.show_error)

        widget = qtw.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    @qtc.pyqtSlot(str)
    def show_error(self, err):
        '''
        Shows a message box if any error occurs during the analysis
        @param err: str, error message
        '''
        err_message = qtw.QMessageBox()
        err_message.setIcon(qtw.QMessageBox.Critical)
        err_message.setWindowTitle('Error Message')
        err_message.setText('Error Message: \n' + err)
        err_message.exec_()
        return

    # the next one is useful for debugging
    '''def submit_settings(self):
        print(self.properties)
        print('kris')'''

    def data_and_properties_to_func(self):
        self.submit_data_and_props_to_check_props.emit(self.data, self.properties)
        print('connection to function might work')

    @qtc.pyqtSlot()
    def properties_to_save(self):  # Could be included into properties class with emit.(self)
        self.submit_properties_to_save.emit(self.properties)

    @qtc.pyqtSlot(object, object)
    def check_properties(self, data, props):
        status = True
        xdf_empty = False
        grand_average_wrong = False
        if 'grand_average' in props and 'grand_average_rois' not in props:
            status = False
            grand_average_wrong = True
        if 'grand_average' not in props:
            if 'selected_xdf_files' not in data.xdf:
                status = False
                xdf_empty = True
            if props['nr_trials'] == '':
                status = False
            if props['task_name'] == '':
                status = False
            mayer_props = [props['mayer_lower'], props['mayer_upper'], props['mayer_corr_band']]
            resp_props = [props['resp_lower'], props['resp_upper'], props['resp_corr_band']]
            if props['correction_mode'] == 'Mayer Waves':
                result1 = False if any(mayer == '' for mayer in mayer_props) else True
                if not result1 or props['mayer_upper'] <= props['mayer_lower']:
                    status = False
            elif props['correction_mode'] == 'Mayer and Respiration':
                result2 = False if any(
                    mayer == '' for mayer in mayer_props) or any(resp == '' for resp in resp_props) else True
                if not result2 or props['mayer_upper'] <= props['mayer_lower'] or props['resp_upper'] <= \
                        props['resp_lower']:
                    status = False
            elif props['correction_mode'] == 'Respiration':
                result3 = False if any(resp == '' for resp in resp_props) else True
                if not result3 or props['resp_upper'] <= props['resp_lower']:
                    status = False
            # elif props['correction_mode'] == 'Default':
        if props['optode_failure_val']:
            flattened_optodes = self.flatten_nested_list(props['optode_failure_list'])
            if props['probe_set'] == '12':
                nr_max_chan = 12
                result4 = False if any(chan > nr_max_chan for chan in flattened_optodes) else True
                if not result4:
                    status = False
            if props['probe_set'] == '24':
                nr_max_chan = 24
                result5 = False if any(chan > nr_max_chan for chan in flattened_optodes) else True
                if not result5:
                    status = False
            if props['probe_set'] == '38':
                nr_max_chan = 38
                result6 = False if any(chan > nr_max_chan for chan in flattened_optodes) else True
                if not result6:
                    status = False
            if props['probe_set'] == '47':
                nr_max_chan = 47
                result7 = False if any(chan > nr_max_chan for chan in flattened_optodes) else True
                if not result7:
                    status = False
            if props['probe_set'] == '50':
                nr_max_chan = 50
                result8 = False if any(chan > nr_max_chan for chan in flattened_optodes) else True
                if not result8:
                    status = False
            if props['probe_set'] == 'Laboratory new':
                nr_max_chan = 24
                result9 = False if any(chan > nr_max_chan for chan in flattened_optodes) else True
                if not result9:
                    status = False
            if props['probe_set'] == 'NIRx Sports old':
                nr_max_chan = 42
                result10 = False if any(chan > nr_max_chan for chan in flattened_optodes) else True
                if not result10:
                    status = False
            if props['probe_set'] == 'NIRx Sports new':
                nr_max_chan = 61
                result11 = False if any(chan > nr_max_chan for chan in flattened_optodes) else True
                if not result11:
                    status = False

        if props['task_length'] == '' or props['pre_task_length'] == '' or props['pre_task_length'] == '':
            status = False

        if props['chosen_condition'] == 'Default':
            status = False
        # TODO: activate this again, but make it better
        '''if props['generate_single_conc_change_figures'] and (not props['conc_range_lower'].lstrip('-').isdigit() or not props['conc_range_upper'].lstrip('-').isdigit()):
            status = False
        elif props['generate_single_conc_change_figures'] and (props['conc_range_lower'] >= props['conc_range_upper']):
            # if props['conc_range_lower'] >= props['conc_range_upper']:
            status = False'''

        if status:
            if 'grand_average' in props:
                filename_list = []
                filename = 'start_str'
                while filename != '':
                    filename, _ = qtw.QFileDialog.getOpenFileName(self, 'Select an Analysis File',
                                                                  self.data.analysis_path_main,
                                                                  'Numpy Files (*.npz)')
                    if filename != '':
                        filename_list.append(filename)
                print(filename_list)
                if len(filename_list) > 1:
                    data.add(filenames_ga=filename_list)
                    self.submit_properties_to_model_ok.emit(self.data, props)
                else:
                    msg_load_ga_not_ok = qtw.QMessageBox(qtw.QMessageBox.Warning, 'File Loading Error',
                                                         'Please select at least two files!')
                    msg_load_ga_not_ok.exec_()
            else:
                self.submit_properties_to_model_ok.emit(self.data, props)
        else:
            if xdf_empty:
                warn_str = 'Please select a xdf-file. Other possible errors: e.g. upper < lower; e.g. empty strings'
            elif grand_average_wrong:
                warn_str = 'Please define the ROIs.'
            else:
                warn_str = 'Possible errors: e.g. upper < lower; e.g. empty strings, invalid chars'
            msg_props_not_ok = qtw.QMessageBox(qtw.QMessageBox.Warning, 'Input Error',
                                               'Please check again your input settings.')
            msg_props_not_ok.setInformativeText(warn_str)
            res = msg_props_not_ok.exec_()

    def flatten_nested_list(self, nested_list):
        ''' Converts a nested list to a flat list '''
        flat_list = []
        # Iterate over all the elements in given list
        for elem in nested_list:
            # Check if type of element is list
            if isinstance(elem, list):
                # Extend the flat list by adding contents of this element (list)
                flat_list.extend(self.flatten_nested_list(elem))
            else:
                # Append the element to the list
                flat_list.append(elem)
        return flat_list
