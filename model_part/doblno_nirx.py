import numpy as np
from scipy import signal

def doblno_nirx(nirx_doblno, props):
    '''
    Applies low pass filter and baseline removal if selected
    @param nirx_doblno: NIRx object of class data_dict including the loaded hdr and xdf data of the selected
    @param props: dict object including all defined settings
    @return: nirx_doblno: NIRx object of class data_dict including the loaded hdr and xdf data of the selected
             text: list including prints displayed to self.output_gb in build_gui()
    '''
    text = []
    oxy_signal = nirx_doblno.nirx_data['Concentration']['raw']['oxy']
    deoxy_signal = nirx_doblno.nirx_data['Concentration']['raw']['deoxy']
    fs = nirx_doblno.hdr['Sampling Rate'][0]

    # Resampling oxy- and deoxy-Hb signal --> 4 Hz
    ds_up = np.round(4 * 10000)
    ds_down = np.round(fs * 10000)
    oxy_signal = signal.resample_poly(oxy_signal, ds_up, ds_down, window=('kaiser', 5))
    deoxy_signal = signal.resample_poly(deoxy_signal, ds_up, ds_down, window=('kaiser', 5))
    fs = round(fs * ds_up / ds_down)  # should be 4
    nirx_doblno.hdr['Sampling Rate'][0] = fs
    if props['low_pass']:
        cut_off = props['cut_off_frequency']
        N_low, Wn_low = signal.buttord(cut_off / (fs / 2), (cut_off + 0.2) / (fs / 2), 3, 30)  # slightly differs from Matlab
        b, a = signal.butter(N_low, Wn_low, btype='low')
        sos_lp = signal.butter(N_low, Wn_low, btype='low', output='sos')  # todo: check that
        oxy_signal2 = oxy_signal
        oxy_signal = signal.sosfiltfilt(sos_lp, oxy_signal, axis=0, padtype='odd', padlen=3 * (max(len(b), len(a)) - 1))
        deoxy_signal = signal.sosfiltfilt(sos_lp, deoxy_signal, axis=0, padtype='odd',
                                          padlen=3 * (max(len(b), len(a)) - 1))

    if props['baseline']:
        N_base, Wn_base = signal.buttord(0.01 / (fs / 2), 0.005 / (fs / 2), 3, 30)
        d, c = signal.butter(N_base, Wn_base, btype='high')  # try with N_base - 1
        sos_baseline = signal.butter(N_base, Wn_base, btype='high', output='sos')
        oxy_signal = signal.sosfiltfilt(sos_baseline, oxy_signal, axis=0, padtype='odd',
                                        padlen=3 * (max(len(d), len(c)) - 1))
        deoxy_signal = signal.sosfiltfilt(sos_baseline, deoxy_signal, axis=0, padtype='odd',
                                          padlen=3 * (max(len(d), len(c)) - 1))

    nirx_doblno.nirx_data['Concentration'].update({'clean': {'deoxy': deoxy_signal, 'oxy': oxy_signal}})
    print('Baseline removal and TP filtering done')
    text.append('Baseline removal and TP filtering done')
    return nirx_doblno, text
