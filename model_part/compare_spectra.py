import numpy as np
import matplotlib.pyplot as plt
import os

def compare_spectra(nirx_compare, props, data):
    '''
    Generates plots to compare the spectra before and after removal of physiological induced artefacts
    Calculates the averaged and continuous data for further analysis
    @param nirx_compare: NIRx object of class data_dict including the loaded hdr and xdf data of the selected measurement
    @param props: dict object including all defined settings
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @return: nirx_compare,
             text: list including prints displayed to self.output_gb in build_gui()
    '''
    text = []
    print('Spectra compare start')
    text.append('Spectra compare start')
    fs = nirx_compare.hdr['Sampling Rate'][0]
    task = props['task_name']
    image_class = props['chosen_condition']
    trig = nirx_compare.trigger
    oxy_signal = nirx_compare.nirx_data['Concentration']['clean']['oxy']
    deoxy_signal = nirx_compare.nirx_data['Concentration']['clean']['deoxy']
    frequency_range = float(props['freq_limit_spectra_figures'])
    excluded_channels = props['excluded_channels']

    if props['generate_spectra_figures']:

        ### oxy - raw
        p1 = nirx_compare.nirx_data['Spectra']['raw_oxy']
        f1 = nirx_compare.nirx_data['Spectra']['Base']
        indx = [idx for idx, val in enumerate(f1) if val <= frequency_range]
        ### deoxy - raw
        p2 = nirx_compare.nirx_data['Spectra']['raw_deoxy']
        ### oxy - clean
        p3 = nirx_compare.nirx_data['Spectra']['cleaned_oxy']
        ### deoxy - clean
        p4 = nirx_compare.nirx_data['Spectra']['cleaned_deoxy']

        fig, ax = plt.subplots()
        ax.plot(f1[indx], 10*np.log10(p1[indx]), color=(1, 0.6, 0.6), label='[oxy-Hb]_raw')
        ax.plot(f1[indx], 10*np.log10(p2[indx]), color=(0.8, 0.8, 1), label='[deoxy-Hb]_raw')
        ax.plot(f1[indx], 10 * np.log10(p3[indx]), color='r', label='[oxy-Hb]_clean')
        ax.plot(f1[indx], 10*np.log10(p4[indx]), color='b', label='[deoxy-Hb]_clean')
        ax.grid()
        ax.set_xlabel('f (Hz)', fontsize=12, fontweight='bold')
        ax.set_xlim(0, frequency_range)
        ax.set_xticks(np.arange(0, frequency_range + 0.1, 0.1))
        ax.set_ylabel('Power spectrum (dB)', fontsize=11, fontweight='bold')
        ax.set_title('Avg. Spectrum [(de)oxy-Hb] before and after \n physiological influence removal', fontsize=11, fontweight='bold')
        ax.legend(loc='best')
        fig.savefig(os.path.join(data.analysis_path, data.file_name) + '_Spectra_Compared_' + props[
        'signal_analysis_method'] + '_' + props['correction_mode'] + '.eps')
        


        # if properties['correction_mode'] == 'Uncorrected':
        #    plt.savefig(os.path.join(data.analysis_path_main, data.selected_file) + '_Spectra_Compared' + properties['TF (Transfer Function Models)'] + properties['correction_mode']+'.png')
        # else:
        # plt.savefig(os.path.join(data.analysis_path_main, data.selected_file) + '_Spectra_Compared' + properties['TF (Transfer Function Models)'] + properties['correction_mode']+'.png')

        # Kanalschleife
    head_oxy = []
    head_deoxy = []
    head_oxy_std = []
    head_deoxy_std = []
    nirx_compare.nirx_data['all_trials_oxy'] = []
    nirx_compare.nirx_data['all_trials_deoxy'] = []

    t = np.arange(1/fs, deoxy_signal.shape[0]/fs+(1/fs), 1/fs)
    soll_activation = np.zeros(deoxy_signal.shape[0])*0
    nirx_compare.nirx_data['all_trials_oxy_continuous'] = [0]*oxy_signal.shape[1]
    nirx_compare.nirx_data['all_trials_deoxy_continuous'] = [0]*oxy_signal.shape[1]

    for i in range(0, trig.shape[0]):
       task_length = float(props['task_length'])
       tmp = np.amin(np.abs(nirx_compare.time['NIRS'] - trig[i]))
       idx = np.where(tmp == np.abs(nirx_compare.time['NIRS'] - trig[i]))
       end_interval = round(0*fs) + round(12*fs)
       if idx[0] + round(task_length*fs) <= len(t):
           soll_activation[int(idx[0]) : int(idx[0])+end_interval+1] = 1  # + 1 to include last value
    del i
    for i in range(0, oxy_signal.shape[1]):
        curve_NIRx(oxy_signal[:,i], deoxy_signal[:,i], props, t, soll_activation, i, data)
        dat_avg, dat_std, t_trial, data_all_trials, text = average_NIRx(np.vstack((oxy_signal[:,i], deoxy_signal[:,i])), nirx_compare, props, trig, fs, text)
        head_oxy.append(dat_avg[:,0])
        head_deoxy.append(dat_avg[:,1])
        head_oxy_std.append(dat_std[:,0])
        head_deoxy_std.append(dat_std[:,1])

        nirx_compare.nirx_data['all_trials_oxy'].append(data_all_trials[0].T)
        nirx_compare.nirx_data['all_trials_deoxy'].append(data_all_trials[1].T)
        all_trials_oxy_continuous_temp = []
        all_trials_deoxy_continuous_temp = []
        for j in range(data_all_trials.shape[1]):
            data_oxy = data_all_trials[0][j,:]
            data_deoxy = data_all_trials[1][j,:]
            step_size = int(np.floor(data_all_trials.shape[2]/10))
            data_oxy_av = []
            data_deoxy_av = []
            for k in range(0, 10):  # change 10 to stepsize?
                data_oxy_av.append(np.mean(data_oxy[k*step_size : k*step_size + step_size]))
                data_deoxy_av.append(np.mean(data_deoxy[k*step_size : k*step_size + step_size]))
            all_trials_oxy_continuous_temp.append(data_oxy_av)
            all_trials_deoxy_continuous_temp.append(data_deoxy_av)
        all_trials_oxy_continuous_temp = np.asarray(all_trials_oxy_continuous_temp)
        all_trials_oxy_continuous_temp = np.reshape(all_trials_oxy_continuous_temp, (all_trials_oxy_continuous_temp.shape[0]*all_trials_oxy_continuous_temp.shape[1]))
        all_trials_deoxy_continuous_temp = np.asarray(all_trials_deoxy_continuous_temp)
        all_trials_deoxy_continuous_temp = np.reshape(all_trials_deoxy_continuous_temp, (all_trials_deoxy_continuous_temp.shape[0]*all_trials_deoxy_continuous_temp.shape[1]))

        nirx_compare.nirx_data['all_trials_oxy_continuous'][i] = (smooth(all_trials_oxy_continuous_temp, 5))
        nirx_compare.nirx_data['all_trials_deoxy_continuous'][i] = (smooth(all_trials_deoxy_continuous_temp, 5))
    del i
    head_oxy = np.asarray(head_oxy).T
    head_deoxy = np.asarray(head_deoxy).T
    head_oxy_std = np.asarray(head_oxy_std).T
    head_deoxy_std = np.asarray(head_deoxy_std).T
    nirx_compare.nirx_data['all_trials_oxy_continuous'] = np.asarray(nirx_compare.nirx_data['all_trials_oxy_continuous'])
    nirx_compare.nirx_data['all_trials_oxy_continuous'] = nirx_compare.nirx_data['all_trials_oxy_continuous'].T
    nirx_compare.nirx_data['all_trials_deoxy_continuous'] = np.asarray(nirx_compare.nirx_data['all_trials_deoxy_continuous'])
    nirx_compare.nirx_data['all_trials_deoxy_continuous'] = nirx_compare.nirx_data['all_trials_deoxy_continuous'].T

    head_oxy, head_deoxy, head_oxy_std, head_deoxy_std, text = optode_failure_NIRx(head_oxy, head_deoxy, head_oxy_std, head_deoxy_std, props, text)

    if len(props['excluded_channels']) != 0:
        for excl in range(len(excluded_channels)):
            head_oxy[:, excluded_channels[excl]-1] = 0
            head_deoxy[:, excluded_channels[excl]-1] = 0
            head_oxy_std[:, excluded_channels[excl]-1] = 0
            head_deoxy_std[:, excluded_channels[excl]-1] = 0

    nirx_compare.nirx_data['avg_oxy'] = head_oxy
    nirx_compare.nirx_data['avg_deoxy'] = head_deoxy
    nirx_compare.nirx_data['avg_oxy_std'] = head_oxy_std
    nirx_compare.nirx_data['avg_deoxy_std'] = head_deoxy_std
    nirx_compare.add(properties=dict(props))
    nirx_compare.properties['t_trial'] = t_trial
    nirx_compare.properties['fs'] = fs
    nirx_compare.nirx_data['oxy_Hb'] = oxy_signal
    nirx_compare.nirx_data['deoxy_Hb'] = deoxy_signal
    print('Spectra compare finished')
    text.append('Spectra compare finished')
    return nirx_compare, text

def optode_failure_NIRx(hd_oxy, hd_deoxy, hd_oxy_std, hd_deoxy_std, props, txt):
    '''
    Calculate value for channels specified in optode failure by replacing them with the mean of the replacement channels
    @param hd_oxy: averaged oxy signal
    @param hd_deoxy: averaged deoxy signal
    @param hd_oxy_std: averaged oxy-std signal
    @param hd_deoxy_std: averaged deoxy-std signal
    @param props: dict object including all defined settings
    @param txt: list including prints displayed to self.output_gb in build_gui()
    @return: hd_oxy, hd_deoxy, hd_oxy_std, hd_deoxy_std, txt
    '''
    optode_failure = props['optode_failure_list']

    if props['optode_failure_val']:
        failed_channs = []
        replacement_channs = []
        for i in range(len(optode_failure[0])):
            failed_channs.append(optode_failure[0][i])
            replacement_channs.append(optode_failure[1][i])

        for j in range(len(failed_channs)):
            print('Optode Failure activated: ch ' + str(failed_channs[i]))
            txt.append('Optode Failure activated: ch ' + str(failed_channs[i]))
            tmp1 = []
            tmp2 = []
            tmp3 = []
            tmp4 = []
            for l in range(len(replacement_channs[j])):
                tmp1.append(hd_oxy[:, replacement_channs[j][l]-1])
                tmp2.append(hd_deoxy[:, replacement_channs[j][l]-1])
                tmp3.append(hd_oxy_std[:, replacement_channs[j][l]-1])
                tmp4.append(hd_deoxy_std[:, replacement_channs[j][l]-1])
            tmp1 = np.asarray(tmp1)
            tmp2 = np.asarray(tmp2)
            tmp3 = np.asarray(tmp3)
            tmp4 = np.asarray(tmp4)
            hd_oxy[:, failed_channs[j]-1] = np.mean(tmp1,axis=0)
            hd_deoxy[:, failed_channs[j]-1] = np.mean(tmp2,axis=0)
            hd_oxy_std[:, failed_channs[j]-1] = np.mean(tmp3,axis=0)
            hd_deoxy_std[:, failed_channs[j]-1] = np.mean(tmp4,axis=0)

    return hd_oxy, hd_deoxy, hd_oxy_std, hd_deoxy_std, txt

def smooth(arr, win_size):
    '''
    Smoothes input array with the same behaviour as smooth in MATLAB
    @param arr: NumPy 1-D array containing the data to be smoothed
    @param win_size: smoothing window size needs, which must be odd number, as in the original MATLAB implementation
    @return: smoothed array
    '''
    out_0 = np.convolve(arr,np.ones(win_size,dtype=int),'valid')/win_size
    r = np.arange(1,win_size-1,2)
    start = np.cumsum(arr[:win_size-1])[::2]/r
    stop = (np.cumsum(arr[:-win_size:-1])[::2]/r)[::-1]
    return np.concatenate((start, out_0, stop))


def curve_NIRx(oxy_signal, deoxy_signal, props, t, soll_activation, c, data):
    '''
    Generates plots of the curved oxy and deoxy signals
    @param oxy_signal: oxy signal
    @param deoxy_signal: deoxy signal
    @param props: dict object including all defined settings
    @param t: time
    @param soll_activation: shows where the activation should be, between trigger marks
    @param c: channel to display
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @return:
    '''
    display_steps = True
    channel = props['displayed_channels']
    if display_steps and props['generate_spectra_figures']:
        # only plotted if the channel is equal to the current iteration in outer for-loop
        if c+1 in channel:
            fig, ax = plt.subplots()
            ax.plot(t, oxy_signal, color='r', linewidth=1)
            ax.plot(t, deoxy_signal, color='b', linewidth=1)
            ax_bounds_y = ax.dataLim.intervaly
            ax_bounds_x = ax.dataLim.intervalx

            ax.set_title('Concentration Change Channel ' + str(c+1))
            ax.set_xlabel('t(s)', fontsize=12)
            ax.set_ylabel('(mM mm)', fontsize=12)
            ax.set_xlim(left=0, right=ax_bounds_x[1])
            abs_max = max(round(np.abs(ax_bounds_y[0]),1), round(np.abs(ax_bounds_y[1]),1))
            ax.set_ylim(bottom=-abs_max, top=abs_max)

            ax.plot(t, soll_activation*(abs_max), color='g', linewidth=1, label='trigger')
            fig.legend(['[oxy-Hb]', '[deoxy-Hb]', 'trigger'], loc='upper right')
            fig.savefig(os.path.join(data.analysis_path, data.file_name) + '_Conc_Chg_Raw_Ch'  + str(c+1) + '_' + props[
                'signal_analysis_method'] + '_' + props['correction_mode'] + '.eps')
            

def average_NIRx(sig, nirx_av, props, trig, fs, txt):
    '''
    Calculates averaged signals and subtracts mean of other time points
    @param sig: input containing both, oxy and deoxy signal as vstacked
    @param nirx_av: NIRx object of class data_dict including the loaded hdr and xdf data of the selected measurement
    @param props: props: dict object including all defined settings
    @param trig: array including time points of triggers
    @param fs: sampling frequency
    @param txt: list including prints displayed to self.output_gb in build_gui()
    @return: dat_avg: squeezed data including oxy and deoxy signals
             dat_std: squeezed std data including oxy and deoxy signals
             t_trial: time points of trial including pre timing
             data_ch_all: data including oxy and deoxy signals
             txt
    '''
    timing = np.asarray([-int(props['pre_task_length']),
                         int(props['task_length']) + int(props['post_task_length'])])

    t_trial = np.arange(round(timing[0]*fs), round(timing[1]*fs))
    data_av = []
    data_ch_all = [[], []]
    sig = sig.T
    for k in range(0, len(trig)):
        # Marker offset
        if props['marker_offset']:
            diff = nirx_av.time['NIRS'][0] - nirx_av.hdr['markers']['time'][0]
            diff_idx = round(diff*fs)
        else:
            diff_idx = 0

        tmp = np.amin(np.abs(nirx_av.time['NIRS'] - trig[k]))
        idx = np.where(tmp == np.abs(nirx_av.time['NIRS'] - trig[k]))

        try:
            data_av.append(sig[idx[0] + diff_idx + t_trial])
            data_ch_all[0].append(sig[idx[0] + t_trial, 0] - np.mean(sig[idx[0] + t_trial[0:(round(timing[0]*fs)*(-1) +1)], 0]))
            data_ch_all[1].append(sig[idx[0] + t_trial, 1] - np.mean(sig[idx[0] + t_trial[0:(round(timing[0]*fs)*(-1) +1)], 1]))
        except:
            print('Could not process Trigger Nr. ' + str(k))
            txt.append('Could not process Trigger Nr. ' + str(k))
    del k
    data_av = np.asarray(data_av)
    data_ch_all = np.asarray(data_ch_all)
    # averaging and smoothing

    dat_avg = np.squeeze(np.mean(data_av, 0))
    dat_std = np.squeeze(np.std(data_av/np.sqrt(trig.shape[0]), 0, ddof=1))
    dat_avg = dat_avg - np.mean(dat_avg[0:(timing[0]*fs)*(-1) + 1], axis=0)

    return dat_avg, dat_std, t_trial, data_ch_all, txt