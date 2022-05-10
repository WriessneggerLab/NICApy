import numpy as np
from scipy import signal
from scipy import linalg
import matplotlib.pyplot as plt
import os

def corr_NIRx(oxy_signal, deoxy_signal, nirx_corr, props, txt, data):
    '''
    Removes physiological induced artefacts by using Transfer Function (TF) models
    @param oxy_signal: oxy signal
    @param deoxy_signal: deoxy signal
    @param nirx_corr: NIRx object of class data_dict including the loaded hdr and xdf data of the selected
    @param props: dict object including all defined settings
    @param txt: list including prints displayed to self.output_gb in build_gui()
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @return: oxy_signal: oxy signal after applied TF method
             deoxy_signal: deoxy signal after applied TF method
             nirx_corr: NIRx object of class data_dict including the loaded hdr and xdf data of the selected
             txt: list including prints displayed to self.output_gb in build_gui()
    '''

    refused_channels = []

    if props['optode_failure_val']:
        optode_failure = props['optode_failure_list']
        failed_channs = []

        for i in range(len(optode_failure[0])):
            failed_channs.append(optode_failure[0][i])

        for i in range(len(failed_channs)):
            refused_channels.append(optode_failure[i][0])

    excluded_channels = props['excluded_channels']

    if len(excluded_channels) !=0:
        for i in range(len(excluded_channels)):
            refused_channels.append(excluded_channels[i])

    if len(refused_channels) != 0:
        refused_channels = np.unique(np.asarray(refused_channels))

    # temporary variables
    fs = round(nirx_corr.hdr['Sampling Rate'][0])
    if nirx_corr.hdr['Bool']['gUSBamp']:
        gUSBamp_fs = nirx_corr.hdr['gUSBamp_sampling_rate']

    ### Trigger Line
    no_upsample = 0
    old = fs
    if fs is 3:
        no_upsample = 1
        old = 3
        fs = 6
    ######################
    # Correction Modes
    # 1 = Uncorrected
    # 2 = Respiration
    # 3 = Mayer Waves
    # 4 = Mayer Waves + Respiration

    if props['correction_mode'] == 'Default':
        correction_mode = 1
    elif props['correction_mode'] == 'Respiration':
        correction_mode = 2
    elif props['correction_mode'] == 'Mayer Waves':
        correction_mode = 3
    elif props['correction_mode'] == 'Mayer and Respiration':
        correction_mode = 4

    mayer_source = 1  # only heart rate possible (no BP)


    #######################
    if correction_mode == 1:
        pass

    if correction_mode != 1:
        nirx_corr.nirx_data['Downsampled'] = dict()

    if correction_mode == 2 or correction_mode == 4:
        ### Respiratory signal
        if nirx_corr.hdr['Bool']['gUSBamp']:
            if not bool(nirx_corr.nirx_data.get('Respiration').any()):
                print('No Respiration Data found! Artefact Correction is not possible!')
                txt.append('No Respiration Data found! Artefact Correction is not possible!')
                raise Exception('No Respiration Data found! Artefact Correction is not possible!')
                return  # return should not be needed

            # downsampling
            resp_down = signal.resample_poly(nirx_corr.nirx_data['Respiration'], fs, gUSBamp_fs, window=('kaiser', 5))

            ## Spectra
            r_resp = calc_physio_spectra(resp_down, fs)
            p_1 = r_resp['pxx']
            f_1 = r_resp['f']
            resp_settings = [props['resp_lower'], props['resp_upper'], props['resp_corr_band']]
            idx_1 = [idx for idx, val in enumerate(f_1) if val <= resp_settings[1]]
            idx_2 = [idx for idx, val in enumerate(f_1) if val >= resp_settings[0]]
            idx_intsec = np.intersect1d(idx_1, idx_2)
            one_pw_lf = np.diff(p_1[idx_intsec])
            two_pw_lf = np.diff(one_pw_lf)
            peak_idx_resp = find_peak(p_1[idx_intsec], one_pw_lf, two_pw_lf)

            f_peak_resp = f_1[idx_2[0] + peak_idx_resp]  # do not do -1 here, because then the index is moved by 2
            print('Peak Resp (EF): %s' % str(f_peak_resp))
            txt.append('Peak Resp (EF): %s' % str(f_peak_resp))
            nirx_corr.nirx_data['Spectra'].update({'F_Peak_Resp': f_peak_resp})

            fig = plt.figure(figsize=(7, 5))
            ax = fig.add_subplot()
            ax.plot(f_1[idx_intsec], 10 * np.log10(p_1[idx_intsec]), color='black', linewidth=1.5)
            ax.plot(f_1[idx_2[0] + peak_idx_resp], 10 * np.log10(p_1[idx_2[0] + peak_idx_resp]), color='red',
                    marker='o', linewidth=1.5)
            ax.autoscale(enable=True, axis='x', tight=True)
            ax.set_xlabel('f (Hz)')
            ax.set_ylabel('Power spectrum (dB)')
            ax.set_title('Downsampled Frequency Spectra')
            fig.savefig(
                os.path.join(data.analysis_path, data.file_name) + '_' + props[
                    'signal_analysis_method'] + '_' + props['correction_mode'] + '_RespirationSpectra.eps')

            temp_peak = round(f_peak_resp * 100) / 100
            wn_low = temp_peak - resp_settings[2]
            wn_high = temp_peak + resp_settings[2]
            if wn_high > resp_settings[1]:
                wn_high = resp_settings[1]
            if wn_low < resp_settings[0]:
                wn_low = resp_settings[0]

            ### Spectra
            wn_resp = np.array([wn_low, wn_high])
            nirx_corr.nirx_data['Spectra'].update({'F_Window_Resp': wn_resp})
            N = 200
            b = signal.firwin(201, wn_resp / (fs / 2), pass_zero=False)
            resp_down = signal.filtfilt(b, 1, resp_down)

            if no_upsample:
                resp_down = signal.resample_poly(resp_down, 3, fs)

            if resp_down.shape[0] < oxy_signal.shape[0]:
                resp_down = np.concatenate((resp_down, np.zeros(oxy_signal.shape[0] - resp_down.shape[0])))

            resp_down = resp_down - np.mean(resp_down)
            nirx_corr.nirx_data['Downsampled'].update({'respiratory': resp_down[0:oxy_signal.shape[0]]})

    if correction_mode == 3 or correction_mode == 4:  # heart rate
        if nirx_corr.hdr['Bool']['gUSBamp']:
            if not bool(nirx_corr.nirx_data.get('Heart Rate').any()):  # 'Respiration' in NIRx.nirx_data.items():
                print('No Heart Rate Data found! Artefact Correction is not possible!')
                txt.append('No Heart Rate Data found! Artefact Correction is not possible!')
                raise Exception('No Heart Rate Data found! Artefact Correction is not possible!')
                return

            # downsampling
            hr_down = signal.resample_poly(nirx_corr.nirx_data['Heart Rate'], fs, gUSBamp_fs, window=('kaiser', 5))

            ## Spectra
            r_hr = calc_physio_spectra(hr_down, fs)
            p_1 = r_hr['pxx']
            f_1 = r_hr['f']
            mayer_settings = [props['mayer_lower'], props['mayer_upper'], props['mayer_corr_band']]
            idx_1 = [idx for idx, val in enumerate(f_1) if val <= mayer_settings[1]]
            idx_2 = [idx for idx, val in enumerate(f_1) if val >= mayer_settings[0]]
            idx_intsec = np.intersect1d(idx_1, idx_2)
            one_pw_lf = np.diff(p_1[idx_intsec])
            two_pw_lf = np.diff(one_pw_lf)
            peak_idx_hr = find_peak(p_1[idx_intsec], one_pw_lf, two_pw_lf)

            f_peak_hr = f_1[idx_2[0] + peak_idx_hr]  # do not do -1 here, because then the index is moved by 2
            print('Peak Heart Rate (EF): %s' % str(f_peak_hr))
            txt.append('Peak Heart Rate (EF): %s' % str(f_peak_hr))
            nirx_corr.nirx_data['Spectra'].update({'F_Peak_Heart_Rate': f_peak_hr})

            fig = plt.figure(figsize=(7, 5))
            ax = fig.add_subplot()
            ax.plot(f_1[idx_intsec], 10 * np.log10(p_1[idx_intsec]), color='black', linewidth=1.5)
            ax.plot(f_1[idx_2[0] + peak_idx_hr], 10 * np.log10(p_1[idx_2[0] + peak_idx_hr]), color='red',
                    marker='o', linewidth=1.5)
            ax.autoscale(enable=True, axis='x', tight=True)
            ax.set_xlabel('f (Hz)')
            ax.set_ylabel('Power spectrum (dB)')
            ax.set_title('Downsampled Heart Rate Spectra')
            fig.savefig(
                os.path.join(data.analysis_path, data.file_name) + '_' + props[
                    'signal_analysis_method'] + '_' + props['correction_mode'] + '_HeartRateSpectra.eps')

            temp_peak = round(f_peak_hr * 100) / 100
            wn_low = temp_peak - mayer_settings[2]
            wn_high = temp_peak + mayer_settings[2]
            if wn_high > mayer_settings[1]:
                wn_high = mayer_settings[1]
            if wn_low < mayer_settings[0]:
                wn_low = mayer_settings[0]

            ### Spectra
            wn_hr = np.array([wn_low, wn_high])
            nirx_corr.nirx_data['Spectra'].update({'F_Window_Heart_Rate': wn_hr})
            N = 200
            b = signal.firwin(201, wn_hr / (fs / 2), pass_zero=False)  # check with order or order +1, should be allright
            hr_down = signal.filtfilt(b, 1, hr_down)
            ####### it works until here

            if no_upsample:
                hr_down = signal.resample_poly(hr_down, 3, fs)

            if hr_down.shape[0] < oxy_signal.shape[0]:
                hr_down = np.concatenate((hr_down, np.zeros(oxy_signal.shape[0] - hr_down.shape[0])))

            hr_down = hr_down - np.mean(hr_down)
            nirx_corr.nirx_data['Downsampled'].update({'Heart Rate': hr_down[0:oxy_signal.shape[0]]})
            nirx_corr.nirx_data['Downsampled'].update({'Mayer': nirx_corr.nirx_data['Downsampled']['Heart Rate']})
            nirx_corr.nirx_data['Spectra'].update({'F_Window_Mayer': wn_hr})

    if correction_mode == 2:  # Respiration
        if nirx_corr.hdr['Bool']['gUSBamp']:
            nirx_corr.nirx_data['Clean'] = {}
            nirx_corr.nirx_data['Clean']['oxy_signals_resp_corr'] = []
            nirx_corr.nirx_data['Clean']['deoxy_signals_resp_corr'] = []
            for g in range(oxy_signal.shape[1]):
                res_oxy = remove_noise_tf(oxy_signal[:, g], nirx_corr.nirx_data['Downsampled']['respiratory'], fs)
                res_deoxy = remove_noise_tf(deoxy_signal[:, g], nirx_corr.nirx_data['Downsampled']['respiratory'], fs)
                nirx_corr.nirx_data['Clean']['oxy_signals_resp_corr'].append(res_oxy)
                nirx_corr.nirx_data['Clean']['deoxy_signals_resp_corr'].append(res_deoxy)
            oxy_signal = np.asarray(nirx_corr.nirx_data['Clean']['oxy_signals_resp_corr']).T
            deoxy_signal = np.asarray(nirx_corr.nirx_data['Clean']['deoxy_signals_resp_corr']).T
            print('Respiration Correction done')
            txt.append('Respiration Correction done')

    if correction_mode == 3:  # Mayer
        nirx_corr.nirx_data['Clean'] = {}
        nirx_corr.nirx_data['Clean']['oxy_signals_mayer_corr'] = []
        nirx_corr.nirx_data['Clean']['deoxy_signals_mayer_corr'] = []
        for g in range(oxy_signal.shape[1]):
            res_oxy = remove_noise_tf(oxy_signal[:, g], nirx_corr.nirx_data['Downsampled']['Mayer'], fs)
            res_deoxy = remove_noise_tf(deoxy_signal[:, g], nirx_corr.nirx_data['Downsampled']['Mayer'], fs)
            nirx_corr.nirx_data['Clean']['oxy_signals_mayer_corr'].append(res_oxy)
            nirx_corr.nirx_data['Clean']['deoxy_signals_mayer_corr'].append(res_deoxy)

        oxy_signal = np.asarray(nirx_corr.nirx_data['Clean']['oxy_signals_mayer_corr']).T
        deoxy_signal = np.asarray(nirx_corr.nirx_data['Clean']['deoxy_signals_mayer_corr']).T
        print('Mayer Waves Correction done')
        txt.append('Mayer Waves Correction done')

    if correction_mode == 4:  # Mayer and Respiration
        if nirx_corr.hdr['Bool']['gUSBamp']:
            nirx_corr.nirx_data['Clean'] = {}
            nirx_corr.nirx_data['Clean']['oxy_signals_resp_corr'] = []
            nirx_corr.nirx_data['Clean']['deoxy_signals_resp_corr'] = []
            for g in range(oxy_signal.shape[1]):
                res_oxy = remove_noise_tf(oxy_signal[:, g], nirx_corr.nirx_data['Downsampled']['respiratory'], fs)
                res_deoxy = remove_noise_tf(deoxy_signal[:, g], nirx_corr.nirx_data['Downsampled']['respiratory'], fs)
                nirx_corr.nirx_data['Clean']['oxy_signals_resp_corr'].append(res_oxy)
                nirx_corr.nirx_data['Clean']['deoxy_signals_resp_corr'].append(res_deoxy)

        if nirx_corr.hdr['Bool']['gUSBamp']:
            nirx_corr.nirx_data['Clean']['oxy_signals_mayer_resp_corr'] = []
            nirx_corr.nirx_data['Clean']['deoxy_signals_mayer_resp_corr'] = []
            for g in range(oxy_signal.shape[1]):
                res_oxy = remove_noise_tf(nirx_corr.nirx_data['Clean']['oxy_signals_resp_corr'][g],
                                          nirx_corr.nirx_data['Downsampled']['Mayer'], fs)
                res_deoxy = remove_noise_tf(nirx_corr.nirx_data['Clean']['deoxy_signals_resp_corr'][g],
                                            nirx_corr.nirx_data['Downsampled']['Mayer'], fs)
                nirx_corr.nirx_data['Clean']['oxy_signals_mayer_resp_corr'].append(res_oxy)
                nirx_corr.nirx_data['Clean']['deoxy_signals_mayer_resp_corr'].append(res_deoxy)

            oxy_signal = np.asarray(nirx_corr.nirx_data['Clean']['oxy_signals_mayer_resp_corr']).T
            deoxy_signal = np.asarray(nirx_corr.nirx_data['Clean']['deoxy_signals_mayer_resp_corr']).T
        print('Respiration and Mayer Waves Correction done')
        txt.append('Respiration and Mayer Waves Correction done')

    
    return oxy_signal, deoxy_signal, nirx_corr, txt

def calc_physio_spectra(physio_signal, fs):
    '''
    Calculates spectra of downsampled physiological input signal
    @param physio_signal: downsampled physiological signal
    @param fs: sampling frequency
    @return: r: dictionary including the power spectral density pxx and array of sample frequencies f
    '''
    window_length = 100
    window_overlap = 50
    fft_length = 200
    window = signal.windows.hann(window_length * fs)  # fs =  in this test case
    r = dict()
    f, pxx = signal.welch(physio_signal - np.mean(physio_signal), window=window,
                                  noverlap=window_overlap * round(fs),
                                  nfft=fft_length * round(fs), fs=round(fs), detrend=False)
    r['pxx'] = pxx
    r['f'] = f
    r['fs'] = fs
    return r

def x_cov(arr_1, arr_2, max_lag_len):
    '''
    Calculates auto- or cross-covariance. If length of auto- or cross-covariance is smaller than max_lag_len,
    zero padding is used
    @param arr_1: input array 1
    @param arr_2: input array 2
    @param max_lag_len: defines how many entries from the middle point of the auto- or crosscovariance are considered
    @return: result: returns auto- or cross covariance of length -max_lang_length until +max_lag_length
    '''
    result = signal.correlate(arr_1 - arr_1.mean(), arr_2 - arr_2.mean(), mode='full')
    result = result / arr_1.shape[0]
    len_interval = (max_lag_len * 2) + 1
    if result.shape[0] < (len_interval):
        num_to_pad = int((len_interval - result.shape[0]) / 2)
        result = np.pad(result, (num_to_pad, num_to_pad), 'constant', constant_values=(0, 0))
    else:
        indx = int((result.shape[0] / 2))
        result = result[indx - max_lag_len: indx + max_lag_len + 1]
    return result

def remove_noise_tf(signal_in, noise, fs):
    '''
    This function is a modified version from remNoiseTF.m implemented by Günther Bauernfeind and Rupert Ortner and is
    part of the BioSig project in MATLAB.
    Removes respiration an Mayer waves related noise from [(de)oxy-Hb] signals by using a transfer function
    model [1,2]. For a detailed description of the model see [3].
    @param signal_in: signal with noise (either oxy or deoxy)
    @param noise: noise signal from a different source (respiration, HR)
    @param fs: sampling frequency
    @return: corr_signal: corrected signal without influence of noise

    [1] Priestley, M.B., 1981. Spectral Analysis and Time Series. Vol. 1 and 2. Academic Press, London, pp. 671.
    [2] Wei, W.W.S., 1990. Time Series Analysis; Univariate and Multivariate Methods. Addison Wesley, New York, pp. 289.
    [3] Florian G, Stancak A, Pfurtscheller G. Cardiac response induced by voluntary selfpaced finger movement.
    International Journal of Psychophysiology, 28: 273-283, 1998.

    modified by Kris Unterhauser, 22.08.2021
    '''
    window_length = 240
    mmax = 15
    seq = fs * window_length
    part_n = int(np.ceil(signal_in.shape[0] / seq))
    corr = np.zeros(signal_in.shape[0])
    end_act = 0
    for i in range(part_n):
        onset = (i) * seq
        ending = (i + 1) * seq

        if ending > signal_in.shape[0]:
            ending = signal_in.shape[0]
        if onset is 0:
            noise_e = np.concatenate((np.ones(mmax) * noise[0], noise[onset:ending]))
        else:
            noise_e = noise[onset - mmax: ending]

        corr_p = part_tf(noise_e, signal_in[onset:ending], mmax)
        corr[end_act:end_act + corr_p.shape[0]] = corr_p  # should work correctly
        end_act = end_act + corr_p.shape[0]

    end_signal = signal_in.shape[0]
    # corr = np.pad(corr, (0, end_signal), mode='constant', constant_values=(0, corr[-1]))  # TODO: check that
    corr_signal = signal_in - corr
    return corr_signal

def part_tf(noise_e, signal_p, mmax):
    '''
    Implementation of the transfer function equations from [3].
    @param noise_e: noise
    @param signal_p: signal
    @param mmax: pre-defined as 15 in remove_noise_tf()
    @return: corr_p: correction term
    '''
    noise_p = noise_e[mmax:]
    mmin = 5
    g_yy = x_cov(noise_p, noise_p, mmax)
    g_xy = x_cov(signal_p, noise_p, mmax)
    g_xx0 = x_cov(signal_p, signal_p, 0)
    index = mmax  # no need for + 1
    lamb = np.zeros(mmax - mmin + 1)
    gu = []
    for m in range(mmin, mmax + 1):
        g_xy_pj = g_xy[index:index + m + 1]
        g_yy_uj = g_yy[index:index + m + 1]
        G = linalg.toeplitz(g_yy_uj)
        g_xy_pj = np.reshape(g_xy_pj, (g_xy_pj.shape[0], 1))
        gu.append(np.linalg.inv(G).dot(g_xy_pj))
        Snn = g_xx0 - np.dot(gu[m - 5].T, g_xy_pj)
        lamb[m - mmin] = noise_p.shape[0] * np.log(Snn) + 2 * (m + 1)

    min_indx = np.argmin(lamb)
    # minm = np.amin(lamb) , not needed
    # mind = mmin + min_indx , not needed
    b = gu[min_indx]
    b = np.reshape(b, (b.shape[0]))
    S = signal.lfilter(b, 1, noise_e)
    corr_p = S[mmax:]
    return corr_p

def find_peak(pw_lf, one_pw_lf, two_pw_lf):
    '''

    @param pw_lf: power spectral density in user defined correction interval
    @param one_pw_lf: differences of pw_lf
    @param two_pw_lf: differences of one_pw_lf
    @return: ef_peak: peak index
    '''
    aa = []
    for i in range(1, len(one_pw_lf) - 1):
        if one_pw_lf[i - 1] <= 0:
            if one_pw_lf[i + 1] >= 0:
                aa.append(i)
        if one_pw_lf[i - 1] >= 0:
            if one_pw_lf[i + 1] <= 0:
                aa.append(i)

    aaa = []
    for ii in range(0, len(aa)):
        if two_pw_lf[aa[ii]] <= 0:
            aaa.append(aa[ii])

    if aaa.__len__() is 0:
        aaa = 1

    amount = pw_lf[aaa[0]]
    ef_peak = aaa[0]
    for iii in range(1, len(aaa)):
        if pw_lf[aaa[iii]] >= amount:
            ef_peak = aaa[iii]
            amount = pw_lf[ef_peak]
    return ef_peak