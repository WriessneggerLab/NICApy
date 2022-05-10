import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import os
import copy


def generate_raw_spectra(nirx_raw, props, data):
    '''
    Generates spectra of the raw oxy and deoxy signals
    @param nirx_raw: NIRx object of class data_dict including the loaded hdr and xdf data of the selected
    @param props: dict object including all defined settings
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @return: nirx_raw: NIRx object of class data_dict including the loaded hdr and xdf data of the selected
             text: list including prints displayed to self.output_gb in build_gui()
    '''
    text = []
    print('RAW Spectra start')
    text.append('RAW Spectra start')

    oxy_signal = nirx_raw.nirx_data['Concentration']['raw'][
        'oxy']
    oxy_signal1 = copy.deepcopy(
        oxy_signal)  # these two are only needed for excluding the channels while calculating the spectra
    deoxy_signal = nirx_raw.nirx_data['Concentration']['raw'][
        'deoxy']
    deoxy_signal1 = copy.deepcopy(
        deoxy_signal)  # hence, the original oxy-deoxy signals remain untouched, these can be seen as a copy

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


    fs = nirx_raw.hdr['Sampling Rate'][0]
    nirx_raw.nirx_data['Spectra'] = {}
    nirx_raw, spectra, fig, text = calc_NIRS_spectra(oxy_signal1, deoxy_signal1, nirx_raw, fs, props, text)
    nirx_raw.nirx_data['Spectra']['all_channels_raw'] = spectra
    nirx_raw.nirx_data['Spectra']['raw_oxy'] = np.mean(spectra['oxy'], axis=1)
    nirx_raw.nirx_data['Spectra']['raw_deoxy'] = np.mean(spectra['deoxy'], axis=1)
    if props['probe_set_val'] != 1 or props['probe_set_val'] != 2:
        fig.savefig(os.path.join(data.analysis_path, data.file_name) + '_Spectra_Raw_' + props[
        'signal_analysis_method'] + '_' + props['correction_mode'] + '.eps')
    else:
        del fig

    print('RAW spectra finished')
    text.append('RAW spectra finished')

    return nirx_raw, text


def calc_NIRS_spectra(signal_oxy, signal_deoxy, nirx_input, fs, props, txt):
    '''
    Calculates the spectra of oxy and deoxy signals using the welch method
    @param signal_oxy: raw oxy signal
    @param signal_deoxy: raw deoxy signal
    @param nirx_input: NIRx object of class data_dict including the loaded hdr and xdf data of the selected
    @param fs: sampling rate
    @param props: props: dict object including all defined settings
    @param txt: list including prints displayed to self.output_gb in build_gui()
    @return:
    '''
    window_length = 100
    window_overlap = 50
    fft_length = 200
    window = signal.windows.hann(window_length * fs)  # fs = 4 in this test case
    spectra_oxy = []
    spectra_deoxy = []
    spectra = {'oxy': spectra_oxy, 'deoxy': spectra_deoxy}
    included_channels = []
    r = dict()
    for i in range(signal_oxy.shape[1]):
        signal_sum = np.sum(signal_oxy[:, i])  # if channel excluded, it is for both, oxy and deoxy
        if not np.isnan(signal_sum):
            f_oxy, pxx_oxy = signal.welch(signal_oxy[:, i] - np.mean(signal_oxy[:, i]), window=window,
                                          noverlap=window_overlap * round(fs),
                                          nfft=fft_length * round(fs), fs=round(fs), detrend=False)
            f_deoxy, pxx_deoxy = signal.welch(signal_deoxy[:, i] - np.mean(signal_deoxy[:, i]), window=window,
                                              noverlap=window_overlap * round(fs),
                                              nfft=fft_length * round(fs), fs=round(fs), detrend=False)
            included_channels.append(i + 1)
            r['pxx_oxy'] = pxx_oxy
            r['f_oxy'] = f_oxy
            r['pxx_deoxy'] = pxx_deoxy
            r['f_deoxy'] = f_deoxy
            r['fs'] = fs
            nirx_input.nirx_data['Spectra']['Base'] = f_oxy

            spectra['oxy'].append(list(pxx_oxy))
            spectra['deoxy'].append(list(pxx_deoxy))
        else:
            pass
            # rsignals[:, i]  # TODO: check that again in Matlab, probably not even needed here
    spectra['oxy'] = np.asarray(spectra['oxy']).T
    spectra['deoxy'] = np.asarray(spectra['deoxy']).T

    fig, text = illustration_multichannel(props['probe_set_val'], spectra['oxy'], spectra['deoxy'], included_channels, f_oxy, props['freq_limit_spectra_figures'], txt=txt)

    return nirx_input, spectra, fig, text


def illustration_multichannel(probeset_val, pxx_oxy, pxx_deoxy, included_channels, f_oxy, freq_range, txt):
    '''
    Generates spectra plots for each channel in one figure.
    @param probeset_val: selected probe set
    @param pxx_oxy: power spectral density of oxy signal
    @param pxx_deoxy: power spectral density of deoxy signal
    @param included_channels: all channels without excluded and optode failure channels
    @param f_oxy: array of sample frequencies.
    @param freq_range: user defined frequency range for displaying the spectra
    @param txt: list including prints displayed to self.output_gb in build_gui()
    @return: fig: figure of spectras
             txt: list including prints displayed to self.output_gb in build_gui()
    '''
    ### dictionaries containing the plotting settings of each different probeset
    probe_set_val5 = {'1': [0.05300, 0.76667, 0.07576, 0.125], '2': [0.14394, 0.76667, 0.07576, 0.125],
                      '3': [0.23485, 0.76667, 0.07576, 0.125], '4': [0.32576, 0.76667, 0.07576, 0.125],
                      '5': [0.41667, 0.76667, 0.07576, 0.125], '6': [0.50758, 0.76667, 0.07576, 0.125],
                      '7': [0.59848, 0.76667, 0.07576, 0.125], '8': [0.68939, 0.76667, 0.07576, 0.125],
                      '9': [0.78030, 0.76667, 0.07576, 0.125], '10': [0.87121, 0.76667, 0.07576, 0.125],
                      '11': [0.00758, 0.60000, 0.07576, 0.125], '12': [0.09848, 0.60000, 0.07576, 0.125],
                      '13': [0.18939, 0.60000, 0.07576, 0.125], '14': [0.28030, 0.60000, 0.07576, 0.125],
                      '15': [0.37121, 0.60000, 0.07576, 0.125], '16': [0.46212, 0.60000, 0.07576, 0.125],
                      '17': [0.55303, 0.60000, 0.07576, 0.125], '18': [0.64394, 0.60000, 0.07576, 0.125],
                      '19': [0.73485, 0.60000, 0.07576, 0.125], '20': [0.82575, 0.60000, 0.07576, 0.125],
                      '21': [0.91667, 0.60000, 0.07576, 0.125], '22': [0.05300, 0.43334, 0.07576, 0.125],
                      '23': [0.14394, 0.43334, 0.07576, 0.125], '24': [0.23485, 0.43334, 0.07576, 0.125],
                      '25': [0.32576, 0.43334, 0.07576, 0.125], '26': [0.41667, 0.43334, 0.07576, 0.125],
                      '27': [0.50758, 0.43334, 0.07576, 0.125], '28': [0.59848, 0.43334, 0.07576, 0.125],
                      '29': [0.68939, 0.43334, 0.07576, 0.125], '30': [0.78030, 0.43334, 0.07576, 0.125],
                      '31': [0.87121, 0.43334, 0.07576, 0.125], '32': [0.00758, 0.26667, 0.07576, 0.125],
                      '33': [0.09848, 0.26667, 0.07576, 0.125], '34': [0.18939, 0.26667, 0.07576, 0.125],
                      '35': [0.28030, 0.26667, 0.07576, 0.125], '36': [0.37121, 0.26667, 0.07576, 0.125],
                      '37': [0.46212, 0.26667, 0.07576, 0.125], '38': [0.55303, 0.26667, 0.07576, 0.125],
                      '39': [0.64394, 0.26667, 0.07576, 0.125], '40': [0.73485, 0.26667, 0.07576, 0.125],
                      '41': [0.82575, 0.26667, 0.07576, 0.125], '42': [0.91667, 0.26667, 0.07576, 0.125],
                      '43': [0.05300, 0.10000, 0.07576, 0.125], '44': [0.14394, 0.10000, 0.07576, 0.125],
                      '45': [0.23485, 0.10000, 0.07576, 0.125], '46': [0.32576, 0.10000, 0.07576, 0.125],
                      '47': [0.41667, 0.10000, 0.07576, 0.125], '48': [0.50758, 0.10000, 0.07576, 0.125],
                      '49': [0.59848, 0.10000, 0.07576, 0.125], '50': [0.68939, 0.10000, 0.07576, 0.125],
                      '51': [0.78030, 0.10000, 0.07576, 0.125], '52': [0.87121, 0.10000, 0.07576, 0.125],
                      }

    probe_set_val3 = {
        '2': [0.41667, 0.76667, 0.07576, 0.125], '5': [0.50758, 0.76667, 0.07576, 0.125],
        '4': [0.37121, 0.60000, 0.07576, 0.125], '16': [0.46212, 0.60000, 0.07576, 0.125],
        '8': [0.55303, 0.60000, 0.07576, 0.125], '9': [0.14394, 0.43334, 0.07576, 0.125],
        '10': [0.23485, 0.43334, 0.07576, 0.125], '13': [0.32576, 0.43334, 0.07576, 0.125],
        '18': [0.41667, 0.43334, 0.07576, 0.125], '21': [0.50758, 0.43334, 0.07576, 0.125],
        '24': [0.59848, 0.43334, 0.07576, 0.125], '25': [0.18939, 0.26667, 0.07576, 0.125],
        '15': [0.28030, 0.26667, 0.07576, 0.125], '29': [0.37121, 0.26667, 0.07576, 0.125],
        '23': [0.46212, 0.26667, 0.07576, 0.125], '36': [0.55303, 0.26667, 0.07576, 0.125],
        '28': [0.23485, 0.10000, 0.07576, 0.125], '31': [0.32576, 0.10000, 0.07576, 0.125],
        '34': [0.41667, 0.10000, 0.07576, 0.125], '38': [0.50758, 0.10000, 0.07576, 0.125]
    }

    probe_set_val4 = {
        '46': [0.23485, 0.76667, 0.07576, 0.125], '44': [0.32576, 0.76667, 0.07576, 0.125],
        '43': [0.41667, 0.76667, 0.07576, 0.125], '41': [0.50758, 0.76667, 0.07576, 0.125],
        '40': [0.59848, 0.76667, 0.07576, 0.125], '38': [0.68939, 0.76667, 0.07576, 0.125],
        '37': [0.78030, 0.76667, 0.07576, 0.125], '47': [0.00758, 0.60000, 0.07576, 0.125],
        '45': [0.18939, 0.60000, 0.07576, 0.125], '32': [0.28030, 0.60000, 0.07576, 0.125],
        '42': [0.37121, 0.60000, 0.07576, 0.125], '28': [0.46212, 0.60000, 0.07576, 0.125],
        '39': [0.55303, 0.60000, 0.07576, 0.125], '24': [0.64394, 0.60000, 0.07576, 0.125],
        '36': [0.73485, 0.60000, 0.07576, 0.125], '20': [0.82575, 0.60000, 0.07576, 0.125],
        '35': [0.05300, 0.43334, 0.07576, 0.125], '34': [0.14394, 0.43334, 0.07576, 0.125],
        '31': [0.23485, 0.43334, 0.07576, 0.125], '30': [0.32576, 0.43334, 0.07576, 0.125],
        '27': [0.41667, 0.43334, 0.07576, 0.125], '26': [0.50758, 0.43334, 0.07576, 0.125],
        '23': [0.59848, 0.43334, 0.07576, 0.125], '22': [0.68939, 0.43334, 0.07576, 0.125],
        '19': [0.78030, 0.43334, 0.07576, 0.125], '18': [0.87121, 0.43334, 0.07576, 0.125],
        '16': [0.00758, 0.26667, 0.07576, 0.125], '33': [0.09848, 0.26667, 0.07576, 0.125],
        '14': [0.18939, 0.26667, 0.07576, 0.125], '29': [0.28030, 0.26667, 0.07576, 0.125],
        '11': [0.37121, 0.26667, 0.07576, 0.125], '25': [0.46212, 0.26667, 0.07576, 0.125],
        '8': [0.55303, 0.26667, 0.07576, 0.125], '21': [0.64394, 0.26667, 0.07576, 0.125],
        '5': [0.73485, 0.26667, 0.07576, 0.125], '17': [0.82575, 0.26667, 0.07576, 0.125],
        '2': [0.91667, 0.26667, 0.07576, 0.125], '15': [0.05300, 0.10000, 0.07576, 0.125],
        '13': [0.14394, 0.10000, 0.07576, 0.125], '12': [0.23485, 0.10000, 0.07576, 0.125],
        '10': [0.32576, 0.10000, 0.07576, 0.125], '9': [0.41667, 0.10000, 0.07576, 0.125],
        '7': [0.50758, 0.10000, 0.07576, 0.125], '6': [0.59848, 0.10000, 0.07576, 0.125],
        '4': [0.68939, 0.10000, 0.07576, 0.125], '3': [0.78030, 0.10000, 0.07576, 0.125],
        '1': [0.87121, 0.10000, 0.07576, 0.125],
    }
    '''probe_set_val4 = {
        '46': [0.68939, 0.10000, 0.07576, 0.125], '44': [0.59848, 0.10000, 0.07576, 0.125],
        '43': [0.50758, 0.10000, 0.07576, 0.125], '41': [0.41667, 0.10000, 0.07576, 0.125],
        '40': [0.32576, 0.10000, 0.07576, 0.125], '38': [0.23485, 0.10000, 0.07576, 0.125],
        '37': [0.14394, 0.10000, 0.07576, 0.125], '47': [0.91667, 0.26667, 0.07576, 0.125],
        '45': [0.73485, 0.26667, 0.07576, 0.125], '32': [0.64394, 0.26667, 0.07576, 0.125],
        '42': [0.55303, 0.26667, 0.07576, 0.125], '28': [0.46212, 0.26667, 0.07576, 0.125],
        '39': [0.37121, 0.26667, 0.07576, 0.125], '24': [0.28030, 0.26667, 0.07576, 0.125],
        '36': [0.18939, 0.26667, 0.07576, 0.125], '20': [0.09848, 0.26667, 0.07576, 0.125],
        '35': [0.87121, 0.43334, 0.07576, 0.125], '34': [0.78030, 0.43334, 0.07576, 0.125],
        '31': [0.68939, 0.43334, 0.07576, 0.125], '30': [0.59848, 0.43334, 0.07576, 0.125],
        '27': [0.50758, 0.43334, 0.07576, 0.125], '26': [0.41667, 0.43334, 0.07576, 0.125],
        '23': [0.32576, 0.43334, 0.07576, 0.125], '22': [0.23485, 0.43334, 0.07576, 0.125],
        '19': [0.14394, 0.43334, 0.07576, 0.125], '18': [0.05300, 0.43334, 0.07576, 0.125],
        '16': [0.91667, 0.60000, 0.07576, 0.125], '33': [0.82575, 0.60000, 0.07576, 0.125],
        '14': [0.73485, 0.60000, 0.07576, 0.125], '29': [0.64394, 0.60000, 0.07576, 0.125],
        '11': [0.55303, 0.60000, 0.07576, 0.125], '25': [0.46212, 0.60000, 0.07576, 0.125],
        '8': [0.37121, 0.60000, 0.07576, 0.125], '21': [0.28030, 0.60000, 0.07576, 0.125],
        '5': [0.18939, 0.60000, 0.07576, 0.125], '17': [0.09848, 0.60000, 0.07576, 0.125],
        '2': [0.00758, 0.60000, 0.07576, 0.125], '15': [0.87121, 0.76667, 0.07576, 0.125],
        '13': [0.78030, 0.76667, 0.07576, 0.125], '12': [0.68939, 0.76667, 0.07576, 0.125],
        '10': [0.59848, 0.76667, 0.07576, 0.125], '9': [0.50758, 0.76667, 0.07576, 0.125],
        '7': [0.41667, 0.76667, 0.07576, 0.125], '6': [0.32576, 0.76667, 0.07576, 0.125],
        '4': [0.23485, 0.76667, 0.07576, 0.125], '3': [0.14394, 0.76667, 0.07576, 0.125],
        '1': [0.05300, 0.76667, 0.07576, 0.125],
    }'''

    probe_set_val6 = {
        '1': [5, 11, 53], '2': [5, 11, 51],
        '3': [5, 11, 41], '4': [5, 11, 49],
        '5': [5, 11, 47], '6': [5, 11, 37],
        '7': [5, 11, 43], '8': [5, 11, 31],
        '9': [5, 11, 21], '10': [5, 11, 39],
        '11': [5, 11, 29], '12': [5, 11, 27],
        '13': [5, 11, 17], '14': [5, 11, 35],
        '15': [5, 11, 25], '16': [5, 11, 13],
        '17': [5, 11, 11], '18': [5, 11, 19],
        '19': [5, 11, 9], '20': [5, 11, 7],
        '21': [5, 11, 15], '22': [5, 11, 5],
        '23': [5, 11, 3], '24': [5, 11, 1],
    }

    probe_set_val7 = {
        '1': [5, 17, 84], '2': [5, 17, 68],
        '3': [5, 17, 82], '4': [5, 17, 80],
        '5': [5, 17, 64], '6': [5, 17, 78],
        '7': [5, 17, 76], '8': [5, 17, 60],
        '9': [5, 17, 74], '10': [5, 17, 72],
        '11': [5, 17, 56], '12': [5, 17, 70],
        '13': [5, 17, 52], '14': [5, 17, 66],
        '15': [5, 17, 50], '16': [5, 17, 48],
        '17': [5, 17, 32], '18': [5, 17, 62],
        '19': [5, 17, 46], '20': [5, 17, 44],
        '21': [5, 17, 28], '22': [5, 17, 58],
        '23': [5, 17, 42], '24': [5, 17, 40],
        '25': [5, 17, 24], '26': [5, 17, 54],
        '27': [5, 17, 38], '28': [5, 17, 36],
        '29': [5, 17, 20], '30': [5, 17, 34],
        '31': [5, 17, 16], '32': [5, 17, 30],
        '33': [5, 17, 14], '34': [5, 17, 12],
        '35': [5, 17, 26], '36': [5, 17, 10],
        '37': [5, 17, 8], '38': [5, 17, 22],
        '39': [5, 17, 6], '40': [5, 17, 4],
        '41': [5, 17, 18], '42': [5, 17, 2],
    }

    probe_set_val8 = {
        '1': [14, 13, 7], '2': [14, 13, 19],
        '3': [14, 13, 21], '4': [14, 13, 33],
        '5': [14, 13, 31], '6': [14, 13, 43],
        '7': [14, 13, 45], '8': [14, 13, 57],
        '9': [14, 13, 35], '10': [14, 13, 47],
        '11': [14, 13, 49], '12': [14, 13, 61],
        '13': [14, 13, 55], '14': [14, 13, 67],
        '15': [14, 13, 69], '16': [14, 13, 81],
        '17': [14, 13, 59], '18': [14, 13, 71],
        '19': [14, 13, 73], '20': [14, 13, 85],
        '21': [14, 13, 63], '22': [14, 13, 75],
        '23': [14, 13, 77], '24': [14, 13, 89],
        '25': [14, 13, 79], '26': [14, 13, 93],
        '27': [14, 13, 105], '28': [14, 13, 83],
        '29': [14, 13, 95], '30': [14, 13, 97],
        '31': [14, 13, 109], '32': [14, 13, 87],
        '33': [14, 13, 99], '34': [14, 13, 101],
        '35': [14, 13, 113], '36': [14, 13, 91],
        '37': [14, 13, 103], '38': [14, 13, 117],
        '39': [14, 13, 107], '40': [14, 13, 119],
        '41': [14, 13, 121], '42': [14, 13, 133],
        '43': [14, 13, 111], '44': [14, 13, 123],
        '45': [14, 13, 125], '46': [14, 13, 137],
        '47': [14, 13, 115], '48': [14, 13, 127],
        '49': [14, 13, 129], '50': [14, 13, 141],
        '51': [14, 13, 135], '52': [14, 13, 147],
        '53': [14, 13, 149], '54': [14, 13, 161],
        '55': [14, 13, 139], '56': [14, 13, 151],
        '57': [14, 13, 153], '58': [14, 13, 165],
        '59': [14, 13, 163], '60': [14, 13, 175],
        '61': [14, 13, 177]
    }

    fig = plt.figure(figsize=(10, 5))
    indx = [idx for idx, val in enumerate(f_oxy) if val <= freq_range]
    if probeset_val == 8:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for ix, channel_number in enumerate(
                included_channels):  # size of included_channels must be identical to size of pxx_oxy/pxx_deoxy
            make_plot = fig.add_subplot(14, 13, probe_set_val8[str(channel_number)][2])
            make_plot.tick_params(axis='both', labelsize=5, pad=1)
            make_plot.set_xlabel('f [Hz]', size=5, labelpad=1)
            make_plot.set_title('Ch' + str(channel_number), fontsize=5, pad=1)
            make_plot.plot(f_oxy[indx], 10 * np.log10(pxx_oxy[indx, ix]), color='r', linewidth=1)
            make_plot.plot(f_oxy[indx], 10 * np.log10(pxx_deoxy[indx, ix]), color='b', linewidth=1)


    elif probeset_val == 7:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for ix, channel_number in enumerate(included_channels):
            make_plot = fig.add_subplot(5, 17, probe_set_val7[str(channel_number)][2])
            make_plot.tick_params(axis='both', labelsize=5, pad=1)
            make_plot.set_xlabel('f [Hz]', size=5, labelpad=1)
            make_plot.set_title('Ch' + str(channel_number), fontsize=5, pad=1)
            make_plot.plot(f_oxy[indx], 10 * np.log10(pxx_oxy[indx, ix]), color='r', linewidth=1)
            make_plot.plot(f_oxy[indx], 10 * np.log10(pxx_deoxy[indx, ix]), color='b', linewidth=1)
        

    elif probeset_val == 6:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for ix, channel_number in enumerate(included_channels):
            make_plot = fig.add_subplot(5, 11, probe_set_val6[str(channel_number)][2])
            make_plot.tick_params(axis='both', labelsize=5, pad=1)
            make_plot.set_xlabel('f [Hz]', size=5, labelpad=1)
            make_plot.set_title('Ch' + str(channel_number), fontsize=5, pad=1)
            make_plot.plot(f_oxy[indx], 10 * np.log10(pxx_oxy[indx, ix]), color='r', linewidth=1)
            make_plot.plot(f_oxy[indx], 10 * np.log10(pxx_deoxy[indx, ix]), color='b', linewidth=1)
        

    elif probeset_val == 5:
        fig.subplots_adjust(hspace=0.4, wspace=0.2)
        for ix, channel_number in enumerate(included_channels):
            ax = fig.add_axes(probe_set_val5[str(channel_number)])
            ax.tick_params(axis='both', labelsize=5, pad=1)
            ax.set_xlabel('f [Hz]', size=5, labelpad=1)
            ax.set_title('Ch' + str(channel_number), fontsize=5, pad=1)
            ax.plot(f_oxy[indx], 10 * np.log10(pxx_oxy[indx, ix]), color='r', linewidth=1)
            ax.plot(f_oxy[indx], 10 * np.log10(pxx_deoxy[indx, ix]), color='b', linewidth=1)
        

    elif probeset_val == 4:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for ix, channel_number in enumerate(included_channels):
            ax = fig.add_axes(probe_set_val4[str(channel_number)])
            ax.tick_params(axis='both', labelsize=5, pad=1)
            ax.set_xlabel('f [Hz]', size=5, labelpad=1)
            ax.set_title('Ch' + str(channel_number), fontsize=5, pad=1)
            ax.plot(f_oxy[indx], 10 * np.log10(pxx_oxy[indx, ix]), color='r', linewidth=1)
            ax.plot(f_oxy[indx], 10 * np.log10(pxx_deoxy[indx, ix]), color='b', linewidth=1)
        

    elif probeset_val == 3:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for ix, channel_number in enumerate(included_channels):
            if channel_number != 1:  # channel 1 is not included in plot dict, see above probeset_val3
                ax = fig.add_axes(probe_set_val3[str(channel_number)])
                ax.tick_params(axis='both', labelsize=5, pad=1)
                ax.set_xlabel('f [Hz]', size=5, labelpad=1)
                ax.set_title('Ch' + str(channel_number), fontsize=5, pad=1)
                ax.plot(f_oxy[indx], 10 * np.log10(pxx_oxy[indx, ix]), color='r', linewidth=1)
                ax.plot(f_oxy[indx], 10 * np.log10(pxx_deoxy[indx, ix]), color='b', linewidth=1)

    else:
        print('Grid of Probe Set' + str(probeset_val) + 'not supported')
        txt.append('Grid of Probe Set' + str(probeset_val) + 'not supported')

    return fig, txt
