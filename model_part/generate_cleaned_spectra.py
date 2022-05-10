import numpy as np
import os
import copy

### functions import
from model_part.generate_raw_spectra import calc_NIRS_spectra


def generate_cleaned_spectra(nirx_clean, props, data):
    '''
    Generates spectra of cleaned signals afte selected physiological artefact removal method
    @param nirx_clean: NIRx object of class data_dict including the loaded hdr and xdf data of the selected measurement
    @param props: dict object including all defined settings
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @return: nirx_clean: NIRx object of class data_dict including the loaded hdr and xdf data of the selected measurement
             text: list including prints displayed to self.output_gb in build_gui()
    '''
    text = []
    print('Cleaned spectra start')
    text.append('Cleaned spectra start')

    fs = nirx_clean.hdr['Sampling Rate'][0]

    oxy_signal_clean = nirx_clean.nirx_data['Concentration']['clean'][
        'oxy']
    oxy_signal1 = copy.deepcopy(oxy_signal_clean)  # these two are only needed for excluding the channels while calculating the spectra
    deoxy_signal_clean = nirx_clean.nirx_data['Concentration']['clean'][
        'deoxy']
    deoxy_signal1 = copy.deepcopy(deoxy_signal_clean)  # hence, the original oxy-deoxy signals remain untouched, these can be seen as a copy

    excluded_channels = props['excluded_channels']

    if len(excluded_channels) != 0:
        for i in range(len(excluded_channels)):
            oxy_signal1[:, excluded_channels[i] - 1] = np.NaN  # -1 for index correction
            deoxy_signal1[:, excluded_channels[i] - 1] = np.NaN

    if props['optode_failure_val']:
        optode_failure = props['optode_failure_list']
        failed_channs = []
        for i in range(len(optode_failure[0])):
            failed_channs.append(optode_failure[0][i])

        for i in range(len(failed_channs)):
            oxy_signal1[:, failed_channs[i] - 1] = np.NaN
            deoxy_signal1[:, failed_channs[i] - 1] = np.NaN

    nirx_clean, spectra, fig, text = calc_NIRS_spectra(oxy_signal1, deoxy_signal1, nirx_clean, fs, props, text)
    nirx_clean.nirx_data['Spectra']['all_channels_cleaned'] = spectra
    nirx_clean.nirx_data['Spectra']['cleaned_oxy'] = np.mean(spectra['oxy'], axis=1)
    nirx_clean.nirx_data['Spectra']['cleaned_deoxy'] = np.mean(spectra['deoxy'], axis=1)
    fig.savefig(os.path.join(data.analysis_path, data.file_name) + '_Spectra_Clean' + props[
        'signal_analysis_method'] + props['correction_mode'] + '.eps')

    print('Cleaned spectra finished')
    text.append('Cleaned spectra finished')
    return nirx_clean, text
