from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from gui_part.settings.basics_groupbox import Basics
from gui_part.settings.signalprocessing_groupbox import SignalProcessing
from gui_part.settings.pyhsioartefacts_groupbox import PhysiologicalArtefacts
from gui_part.settings.channels_groupbox import Channels
from gui_part.settings.timing_groupbox import Timing
from gui_part.settings.artefacts_groupbox import Artefacts
from gui_part.settings.figureoptions_groupbox import FigureOptions
from gui_part.settings.startanalysis_groupbox import StartAnalysis

class Settings(qtw.QWidget):
    '''
    Class creating the Settings Main Groupbox including all the subgroupboxes
    Inherited from QWidget.

    --------
    Methods:
    --------

    build_settings_gb(self)
    allow_ga_settings(self, ga_status)

    '''
    submit_optode_failure_val_to_props_ga = qtc.pyqtSignal(dict)
    submit_optode_failure_list_to_props_ga = qtc.pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)
        self.build_settings_gb()

    def build_settings_gb(self):
        '''
        Creates the Settings Groupbox layout including all the subgroupboxes and the signal and slot connections
        happening inside the Settings Groupbox
        '''
        settings_gb = qtw.QGroupBox('Settings')
        settings_gb.setProperty("cssClass", "outer")

        # Subwidgets of Settings
        self.basics_box = Basics()
        self.sig_proc_box = SignalProcessing()
        self.physio_arte_box = PhysiologicalArtefacts()
        self.channels_box = Channels()
        self.timing_box = Timing()
        self.artefacts_box = Artefacts()
        self.fig_opt_box = FigureOptions()
        self.start_ana_button = StartAnalysis()

        self.sig_proc_box.submit_possible_artefact_correction.connect(self.physio_arte_box.allow_physio_artefacts)
        self.artefacts_box.submit_method_excluded_channels.connect(self.channels_box.allow_excluding_channels)
        self.artefacts_box.submit_method_excluded_channels.connect(self.channels_box.allow_display_channels)
        self.artefacts_box.submit_nr_trials_checked.connect(self.basics_box.get_if_nr_trials_checked)
        self.basics_box.submit_nr_trials_to_artebox.connect(self.artefacts_box.get_nr_trials)

        # Settings Main Layout
        outer_layout = qtw.QVBoxLayout()
        outer_layout.setSpacing(0)
        outer_layout.addWidget(settings_gb)
        outer_layout.setContentsMargins(0, 0, 5, 0)
        inner_layout = qtw.QVBoxLayout()
        inner_layout.setSpacing(0)
        h_layout_top = qtw.QHBoxLayout()
        h_layout_top.setSpacing(5)
        h_layout_top.addWidget(self.basics_box)
        h_layout_top.addWidget(self.sig_proc_box)
        h_layout_top.setStretch(0, 4)
        h_layout_top.setStretch(1, 5)
        h_layout_bottom = qtw.QHBoxLayout()
        v_layout_left = qtw.QVBoxLayout()
        v_layout_left.setContentsMargins(0, 0, 5, 0)
        v_layout_left.addWidget(self.physio_arte_box)
        v_layout_left.addWidget(self.channels_box)
        v_layout_left.setStretch(0, 2)
        v_layout_left.setStretch(1, 5)
        v_layout_right = qtw.QVBoxLayout()
        v_layout_right.setSpacing(0)
        v_layout_right.addWidget(self.timing_box)
        v_layout_right.addWidget(self.artefacts_box)
        v_layout_right.addWidget(self.fig_opt_box)
        v_layout_right.addWidget(self.start_ana_button)
        h_layout_bottom.addLayout(v_layout_left)
        h_layout_bottom.addLayout(v_layout_right)
        h_layout_bottom.setStretch(0, 3)
        h_layout_bottom.setStretch(1, 2)
        inner_layout.addLayout(h_layout_top)
        inner_layout.addLayout(h_layout_bottom)
        inner_layout.setStretch(0, 3)
        inner_layout.setStretch(1, 8)
        inner_layout.setContentsMargins(5, 0, 5, 5)
        settings_gb.setLayout(inner_layout)
        self.setLayout(outer_layout)

    @qtc.pyqtSlot(bool)
    def allow_ga_settings(self, ga_status):
        '''
        Checks if Grand Average or single analysis is performed and allows the corresponding settings
        @param ga_status: bool, True if Grand Average analysis and False if not
        '''
        if ga_status:
            # Basics
            self.basics_box.nr_trials.setEnabled(False)
            self.basics_box.task_name.setEnabled(False)
            # Signal Processing
            self.sig_proc_box.setEnabled(False)
            # Physiological Artefacts
            self.physio_arte_box.setEnabled(False)
            # Timing
            self.timing_box.consider_marker_offset.setEnabled(False)
            # Artefacts
            self.artefacts_box.cons_opt_failure.setEnabled(False)
            # Figure Options
            self.fig_opt_box.generate_biosig_figs.setEnabled(False)
            self.fig_opt_box.generate_spectra_figs.setEnabled(False)
            self.fig_opt_box.frequency_limit.setEnabled(False)
            self.fig_opt_box.frequency_limit_l.setEnabled(False)
        elif not ga_status:
            self.basics_box.nr_trials.setEnabled(True)
            self.basics_box.task_name.setEnabled(True)
            # Signal Processing
            self.sig_proc_box.setEnabled(True)
            # Physiological Artefacts
            self.physio_arte_box.setEnabled(True)
            # Artefacts
            self.artefacts_box.cons_opt_failure.setEnabled(True)
            # Timing
            self.timing_box.consider_marker_offset.setEnabled(True)
            # Figure Options
            self.fig_opt_box.generate_biosig_figs.setEnabled(True)
            self.fig_opt_box.generate_spectra_figs.setEnabled(True)
            self.fig_opt_box.frequency_limit.setEnabled(True)
            self.fig_opt_box.frequency_limit_l.setEnabled(True)