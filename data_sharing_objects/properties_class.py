class Properties(dict):
    '''
    Class for creating a Properties object which stores all the defined settings in the Settings Groupbox
    Inherited from dict.

    --------
    Methods:
    --------

    initial_properties(self)
    delete_ga_property(self, string_ga)
    add_properties(self, inputs)

    '''
    def __init__(self):
        dict.__init__(self)
        # super(Properties, self).__init__()
        self.initial_properties()

    def initial_properties(self):
        '''
        Defines the initial Settings shown to the user when the application started
        '''
        self.update({'condition_markers': [],
                     'available_conditions': [],
                     'signal_imaging': 'Averaging over Trials',
                     'chosen_condition': 'Default',
                     'probe_set': '12',
                     'nr_trials': '',
                     'task_name': '',
                     'mayer_waves_source': '',
                     'signal_analysis_method': 'TF (Transfer Function Models)',
                     'correction_mode': 'Uncorrected',
                     'baseline': False,
                     'notch': False,
                     'low_pass': False,
                     'cut_off_frequency': '',
                     'mayer_lower': '',
                     'mayer_upper': '',
                     'mayer_corr_band': '',
                     'resp_lower': '',
                     'resp_upper': '',
                     'resp_corr_band': '',
                     'excluded_channels': [],
                     'displayed_channels': [],
                     'task_length': '',
                     'pre_task_length': '',
                     'post_task_length': '',
                     'marker_offset': False,
                     'excluded_trials': '',
                     'optode_failure_val': False,
                     'optode_failure_list': [[], [[]]],
                     'generate_biosig_figures': False,
                     'generate_spectra_figures': False,
                     'generate_single_conc_change_figures': False,
                     'generate_std_plot': False,
                     'freq_limit_spectra_figures': '',
                     'conc_range_lower': '',
                     'conc_range_upper': ''
                     })

    def delete_ga_property(self, string_ga):
        '''
        Deletes keys in the properties object when Grand Average analysis is not desired anymore (Stop clicked)
        @param string_ga: string, properties key to delete
        '''
        if string_ga in self:
            del self[string_ga]

    def add_properties(self, inputs):
        '''
        Add or update key to properties object
        Usually called when the user enters or changes some settings
        @param inputs:
        '''
        self.update(inputs)
        print(self)  # this is useful for debugging