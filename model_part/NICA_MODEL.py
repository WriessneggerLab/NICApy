### import pyqt module
from PyQt5 import QtCore as qtc
import numpy as np
import traceback

### import functions from files
from model_part.checkprobeset import check_probeset
from model_part.load_files import load_files
from model_part.generate_bio_signals import generate_biosignals
from model_part.doblno_nirx import doblno_nirx
from model_part.remove_physio_signals import remove_physio
from model_part.compare_spectra import compare_spectra
from model_part.generate_raw_spectra import generate_raw_spectra
from model_part.generate_cleaned_spectra import generate_cleaned_spectra
from model_part.generate_head_plot import generate_headplot
from model_part.create_eval_path import create_eval_path
from model_part.write_output_file import write_output_file
from model_part.grand_average import get_grand_average_data
from model_part.grand_average import grand_average_output_file
from model_part.t_test import single_t_test

class NICAModel(qtc.QObject):
    '''
    Class including all signals and run method needed for communicating with nica_ui and performing standard single
    or Grand Average analysis.
    Inherited from QObject.

    --------
    Methods:
    --------

    run(self, data, properties)

    '''
    submit_error = qtc.pyqtSignal(str)
    submit_load_text_to_ana_status = qtc.pyqtSignal(str)
    submit_eval_path_to_ana_status = qtc.pyqtSignal(str)
    submit_probeset_text_to_ana_status = qtc.pyqtSignal(str)
    submit_bio_text_to_ana_status = qtc.pyqtSignal(str)
    submit_base_text_to_ana_status = qtc.pyqtSignal(str)
    submit_raw_text_to_ana_status = qtc.pyqtSignal(str)
    submit_physio_text_to_ana_status = qtc.pyqtSignal(str)
    submit_cleaned_text_to_ana_status = qtc.pyqtSignal(str)
    submit_compare_text_to_ana_status = qtc.pyqtSignal(str)
    submit_head_text_to_ana_status = qtc.pyqtSignal(str)
    submit_output_text_to_ana_status = qtc.pyqtSignal(str)
    submit_text_to_outputbox = qtc.pyqtSignal(list)
    submit_error_to_messagebox = qtc.pyqtSignal(str)
    finished = qtc.pyqtSignal()

    def run(self, data, properties):
        '''
        Performs a single analysis or Grand Average analysis including all necessary functions of each
        processing pipeline. At the beggining there will be checked if Grand Analysis or standard single analysis is
        desired.
        @param data: Singleton object including parameters like analysis_path, file_name etc.
        @param properties: dict object including all defined settings
        @return: if any method fails, the exception as string is returned to self.output_gb in build_gui()
        through signal and slot connection
        '''

        if 'grand_average' not in properties:
            #self.returnflag = False
            try:
                ana_status = 'Create Evaluation Path ...'
                self.submit_eval_path_to_ana_status.emit(ana_status)
                data = create_eval_path(self, data, properties)
            except Exception:
            #if self.returnflag == True:
                ana_status = 'Could not create Analysis Path'
                self.submit_eval_path_to_ana_status.emit(ana_status)
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                self.finished.emit()
                return

            try:
                ana_status = 'Loading XDF-Data ...'
                self.submit_load_text_to_ana_status.emit(ana_status)
                NIRx, text = load_files(data, properties)
                self.submit_text_to_outputbox.emit(text)
            except Exception:
                ana_status = 'Error while loading XDF-Data'
                self.submit_load_text_to_ana_status.emit(ana_status)
                self.submit_text_to_outputbox.emit([str(traceback.format_exc())])
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                self.finished.emit()
                return

            try:
                ana_status = 'Checking Probeset ...'
                self.submit_probeset_text_to_ana_status.emit(ana_status)
                NIRx, properties = check_probeset(NIRx, properties)
            except Exception:
                ana_status = 'Probeset not ok.'
                self.submit_probeset_text_to_ana_status.emit(ana_status)
                self.submit_text_to_outputbox.emit([str(traceback.format_exc())])
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                self.finished.emit()
                return

            try:
                ana_status = 'Generating Biosignals and Concentration Change Signals...'
                self.submit_bio_text_to_ana_status.emit(ana_status)
                NIRx, text = generate_biosignals(NIRx, properties, data)
                self.submit_text_to_outputbox.emit(text)
            except Exception:
                ana_status = 'Error while generating Biosignals and Conc. Change Signals'
                self.submit_bio_text_to_ana_status.emit(ana_status)
                self.submit_text_to_outputbox.emit([str(traceback.format_exc())])
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                self.finished.emit()
                return

            try:
                ana_status = 'Removing Baseline and Filtering ...'
                self.submit_base_text_to_ana_status.emit(ana_status)
                NIRx, text = doblno_nirx(NIRx, properties)
                self.submit_text_to_outputbox.emit(text)
            except Exception:
                ana_status = 'Error while removing Baseline and Filtering'
                self.submit_base_text_to_ana_status.emit(ana_status)
                self.submit_text_to_outputbox.emit([str(traceback.format_exc())])
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                self.finished.emit()
                return

            try:
                ana_status = 'Generating RAW Spectra ...'
                self.submit_raw_text_to_ana_status.emit(ana_status)
                NIRx, text = generate_raw_spectra(NIRx, properties, data)
                self.submit_text_to_outputbox.emit(text)
            except Exception:
                ana_status = 'Error while generating RAW Spectra'
                self.submit_raw_text_to_ana_status.emit(ana_status)
                self.submit_text_to_outputbox.emit([str(traceback.format_exc())])
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                self.finished.emit()
                return

            try:
                ana_status = 'Removing Physiological Artefacts ...'
                self.submit_physio_text_to_ana_status.emit(ana_status)
                NIRx, text = remove_physio(NIRx, properties, data)
                self.submit_text_to_outputbox.emit(text)
            except Exception:
                ana_status = 'Error while removing Physiological Artefacts'
                self.submit_physio_text_to_ana_status.emit(ana_status)
                self.submit_text_to_outputbox.emit([str(traceback.format_exc())])
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                self.finished.emit()
                return

            try:
                ana_status = 'Generating Cleaned Spectra ...'
                self.submit_cleaned_text_to_ana_status.emit(ana_status)
                NIRx, text = generate_cleaned_spectra(NIRx, properties, data)
                self.submit_text_to_outputbox.emit(text)
            except Exception:
                ana_status = 'Error while generating Cleaned Spectra'
                self.submit_cleaned_text_to_ana_status.emit(ana_status)
                self.submit_text_to_outputbox.emit([str(traceback.format_exc())])
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                self.finished.emit()
                return

            try:
                ana_status = 'Comparing Spectra ...'
                self.submit_compare_text_to_ana_status.emit(ana_status)
                NIRx, text = compare_spectra(NIRx, properties, data)
                self.submit_text_to_outputbox.emit(text)
            except Exception:
                ana_status = 'Error while generating Compared Spectra'
                self.submit_compare_text_to_ana_status.emit(ana_status)
                self.submit_text_to_outputbox.emit([str(traceback.format_exc())])
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                self.finished.emit()
                return

            try:
                ana_status = 'Generating Concentration Head Plot ...'
                self.submit_head_text_to_ana_status.emit(ana_status)
                NIRx = generate_headplot(NIRx, properties, data)
            except Exception:
                ana_status = 'Error while generating Concentration Head Plot'
                self.submit_head_text_to_ana_status.emit(ana_status)
                self.submit_text_to_outputbox.emit([str(traceback.format_exc())])
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                self.finished.emit()
                return

            try:
                ana_status = 'Write Output Files ...'
                self.submit_head_text_to_ana_status.emit(ana_status)
                text = write_output_file(NIRx, properties, data)
                ana_status = 'Analysis Finished'
                self.submit_output_text_to_ana_status.emit(ana_status)
                self.submit_text_to_outputbox.emit(text)
                self.finished.emit()
            except Exception:
                ana_status = 'Could not write xlsx-file!'
                self.submit_output_text_to_ana_status.emit(ana_status)
                self.submit_text_to_outputbox.emit([str(traceback.format_exc())])
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                self.finished.emit()
                return

        else:
            try:
                ana_status = 'Prepare Grand Average Data ...'
                self.submit_head_text_to_ana_status.emit(ana_status)
                NIRx, all_data, properties = get_grand_average_data(data, properties)
            except Exception:
                ana_status = 'Error while preparing Grand Average Data'
                self.submit_head_text_to_ana_status.emit(ana_status)
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                print(str(traceback.format_exc()))
                return

            try:
                ana_status = 'Generate Grand Average Concentration Head Plots ...'
                self.submit_head_text_to_ana_status.emit(ana_status)
                fs = NIRx.properties['fs']
                timing = np.asarray([-int(properties['pre_task_length']),
                                     int(properties['task_length']) + int(properties['post_task_length'])])
                NIRx.properties['t_trial'] = np.arange(round(timing[0] * fs), round(timing[1] * fs))
                NIRx = generate_headplot(NIRx, properties, data)
            except Exception:
                ana_status = 'Error while generating Grand Average Concentration Head Plots'
                self.submit_head_text_to_ana_status.emit(ana_status)
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                print(str(traceback.format_exc()))
                return

            try:
                ana_status = 'Write Grand Average Output Files ...'
                self.submit_head_text_to_ana_status.emit(ana_status)
                grand_average_output_file(all_data, NIRx, properties, data)
                ana_status = 'Grand Average Analysis Finished'
                self.submit_output_text_to_ana_status.emit(ana_status)
                self.finished.emit()
            except Exception:
                ana_status = 'Could not write Grand Average Output Files!'
                self.submit_output_text_to_ana_status.emit(ana_status)
                self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
                print(str(traceback.format_exc()))
                return


class TTest(qtc.QObject):
    '''
    Class including all signals and methods for performing the modified t-test
    Inherited from QObject.

    --------
    Methods:
    --------

    do_ttest(self, fname)

    '''

    submit_ttest_show = qtc.pyqtSignal(list)
    submit_error_to_messagebox = qtc.pyqtSignal(str)

    def do_ttest(self, fname):
        '''
        Executes the modified one-sample t-test and submits the output to the window shown afterwards to the user
        inside the GUI
        @param fname: filename of the data on which the t-test should be performed
        '''
        try:
            tt_output = single_t_test(fname)
            self.submit_ttest_show.emit(tt_output)
        except Exception:
            # tt_status = 'Could not execute t-test.'
            # self.submit_output_text_to_ana_status.emit(tt_status)
            self.submit_error_to_messagebox.emit(str(traceback.format_exc()))
            print(str(traceback.format_exc()))
            return