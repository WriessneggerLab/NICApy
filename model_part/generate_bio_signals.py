import os
import numpy as np
from scipy import signal
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

### functions import
from model_part.calculate_concentration_change import calculate_conc_change


def generate_biosignals(nirx_bio, props, data):
    '''
    Filters ecg and respiration signals if notch filter is selected.
    Generates biosignals plots.
    Averages physiological signals ecg and respiration.
    @param nirx_bio: NIRx object of class data_dict including the loaded hdr and xdf data of the selected measurement
    @param props: dict object including all defined settings
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @return: nirx_bio: NIRx object of class data_dict including the loaded hdr and xdf data of the selected measurement
             text: list including prints displayed to self.output_gb in build_gui()
    '''
    text = []
    try:
        print('Generate Biosignals start')
        text.append('Generate Biosignals start')
        image_class_string = props['chosen_condition']
        image_class_value = [int(props['condition_markers'][marker]) for marker in
                             range(len(props['available_conditions'])) if
                             props['available_conditions'][marker] == image_class_string]
        image_class_value = image_class_value[0]
        class_labels = nirx_bio.hdr['markers']['class']
        trigger = nirx_bio.hdr['markers']['time']
        gUSBamp_ecg = nirx_bio.nirx_data['ECG']
        gUSBamp_resp = nirx_bio.nirx_data['Respiration']
        if nirx_bio.hdr['Bool']['gUSBamp']:
            gUSBamp_fs = nirx_bio.hdr['gUSBamp_sampling_rate']
        else:
            gUSBamp_fs = 0

        if image_class_string != 'Default':
            trig = trigger[class_labels == image_class_value]
        else:
            trig = trigger

        condition_trigger = np.unique(class_labels)

        # In case no triggers are found for the chosen condition
        if trig.size == 0:
            print('No marker for condition %s found. Execution stopped!' % image_class_string)
            print('Possible marker: %s' % condition_trigger)
            text.append('No marker for condition %s found. Execution stopped!' % image_class_string)
            text.append('Possible marker: %s' % condition_trigger)
            error_message = 'No marker for condition %s found. Execution stopped!' % image_class_string + '\n Possible marker: %s' % condition_trigger
            raise Exception(error_message)

        nr_trials = props['nr_trials']
        if trig.shape[0] != nr_trials:
            print('Number of Trials does not match number of condition marker. Execution stopped!')
            print('Possible marker: %s' % condition_trigger)
            text.append('Number of Trials does not match number of condition marker. Execution stopped!')
            text.append('Possible marker: %s' % condition_trigger)
            error_message = 'Number of Trials does not match number of condition marker. Execution stopped! \n Possible marker: %s' % condition_trigger
            raise Exception(error_message)


        if nirx_bio.hdr['Bool']['gUSBamp']:
            target_activation = np.zeros(nirx_bio.nirx_data['Respiration'].shape[0], dtype=int) * 0

            # notch-Filter data at 50Hz
            if props['notch']:
                try:
                    sos_butter = signal.butter(1, Wn=[48, 52], btype='bandstop', fs=gUSBamp_fs,
                                               output='sos')
                    b, a = signal.butter(1, Wn=[48, 52], btype='bandstop', fs=gUSBamp_fs)
                    ecg_filtered_butter_sos = signal.sosfiltfilt(sos_butter, gUSBamp_ecg,
                                                                 padtype='odd', padlen=3 * (
                                max(len(b), len(a)) - 1))  # TODO: check the axis and padlength again, evtl. *(-1)
                    respiration_filtered_butter_sos = signal.sosfiltfilt(sos_butter, gUSBamp_resp, padtype='odd',
                                                                         padlen=3 * (max(len(b), len(a)) - 1))
                    nirx_bio.nirx_data['ECG'] = ecg_filtered_butter_sos
                    nirx_bio.nirx_data['Respiration'] = respiration_filtered_butter_sos
                except:
                    w0 = 50 / (round(gUSBamp_fs) / 2)  # 128
                    b, a = signal.iirnotch(w0, 35)  # 50, 12.5
                    ecg_filtered_notch = signal.lfilter(b, a,
                                                        gUSBamp_ecg)  # if input array is 2D, axis = 0 might be needed
                    respiration_filtered_notch = signal.lfilter(b, a, gUSBamp_resp)
                    nirx_bio.nirx_data['ECG'] = ecg_filtered_notch
                    nirx_bio.nirx_data['Respiration'] = respiration_filtered_notch
        else:
            target_activation = 0

        # according to debugging, the next whole block is not even needed???
        '''### target_activation everywhere 1 where signal is active
        for i in range(0, trig.shape[0]):
            if NIRx.hdr['Bool']['gUSBamp']:
                tmp = np.amin(np.abs(NIRx.time['gUSBamp'] - trig[i]))
                idx = np.where(tmp == np.abs(NIRx.time['gUSBamp'] - trig[i]))
                abc = idx[0]
                target_activation[idx[0] + round(0*gUSBamp_fs):round(12 * gUSBamp_fs)] = 1  # check settings.timing.signal
                # target_activation[idx + round(0*gUSBamp_fs) : round(settings.timing.signal * gUSBamp_fs)] = 1  # check settings.timing.signal

            #tmp = np.amax(np.abs(np.mean(np.reshape(t, sz[1:3], order='F'), axis=1)))
            # for ix: it takes the first index if it appears more than one time (when calculating the delay), but it does the same in Matlab
            #ix = np.where(tmp == np.abs(np.mean(np.reshape(t, sz[1:3], order='F'), axis=1)))  # t * (-1)

        del i, idx'''

        props['correct_physio_signals'] = True

        # if settings['correct physio signals'] is True:
        if props['correct_physio_signals']:  # correct_physio_signals:
            ecg_temporary = (
                    nirx_bio.nirx_data['ECG'] - np.mean(
                nirx_bio.nirx_data['ECG']))
            nirx_bio.nirx_data['ECG'] = ecg_temporary
            respiration_temporary = nirx_bio.nirx_data['Respiration'] * (-1)
            nirx_bio.nirx_data['Respiration'] = respiration_temporary

        curve_phyisio(nirx_bio, data, gUSBamp_fs=gUSBamp_fs)
        text = averaging_physio(nirx_bio, props, data, image_class_string, trig=trig, gUSBamp_fs=gUSBamp_fs, txt=text)

        deoxy_signal, oxy_signal = calculate_conc_change(nirx_bio)

        if np.isnan(deoxy_signal).any() or np.isnan(oxy_signal).any():
            print('Error with Concentration Calculation!')
            text.append('Error with Concentration Calculation!')
            raise Exception('Error with Concentration Calculation!')
            return

        nirx_bio.nirx_data['Concentration'] = dict()
        nirx_bio.nirx_data['Concentration'].update({'raw': {'deoxy': deoxy_signal, 'oxy': oxy_signal}})

        print('Generate Biosignals finished')
        text.append('Generate Biosignals finished')

        nirx_bio.add(trigger=trig)
        return nirx_bio, text

    except Exception:
        if not nirx_bio.hdr['Bool']['gUSBamp']:
            print('Error "Analysis": No gUSBamp data available.')
            text.append('Error "Analysis": No gUSBamp data available.')
            raise
            #raise Exception('Error "Analysis": No gUSBamp data available.')
        else:
            print('Error message: %s' % str(traceback.format_exc()))
            text.append('Error message: %s' % str(traceback.format_exc()))
            raise
        return


def curve_phyisio(nirx_curve_physio, data, gUSBamp_fs):
    '''
    Generates biosignals plots.
    @param nirx_curve_physio: NIRx object of class data_dict including the loaded hdr and xdf data of the selected
    measurement
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @param gUSBamp_fs: Sampling rate of gUSB-amplifier
    @return: None
    '''

    if nirx_curve_physio.hdr['Bool']['gUSBamp']:
        t_gusbamp = np.arange(1 / gUSBamp_fs, (nirx_curve_physio.nirx_data['Respiration'].shape[0] + 1) / gUSBamp_fs,
                              1 / gUSBamp_fs)
        # TODO: check if +1 is needed at shape
        font_size = 16
        line_width = 2

        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(8, 6))
        ax1.plot(t_gusbamp, nirx_curve_physio.nirx_data['Respiration'], 'k-', linewidth=1)
        ax1.set_xlabel('time (s)')
        ax1.set_ylabel('(a.u)')
        ax1.set(title='Respiration')
        ax1.set_xlim(0, nirx_curve_physio.nirx_data['Respiration'].shape[0] / gUSBamp_fs)
        ax1.grid()

        ax2.plot(t_gusbamp, nirx_curve_physio.nirx_data['Heart Rate'], 'k-', linewidth=1)
        ax2.set_xlabel('time (s)')
        ax2.set_ylabel('(bpm)')
        ax2.set(title='Heart Rate')
        ax2.set_xlim(0, nirx_curve_physio.nirx_data['Heart Rate'].shape[0] / gUSBamp_fs)
        ax2.grid()

        ax3.plot(t_gusbamp, nirx_curve_physio.nirx_data['ECG'], 'k-', linewidth=1)
        ax3.set_xlabel('time (s)')
        ax3.set_ylabel('(a.u.)')
        ax3.set(title='ECG')
        ax3.set_xlim(0, nirx_curve_physio.nirx_data['ECG'].shape[0] / gUSBamp_fs)
        ax3.grid()
        plt.tight_layout()

        fig.savefig(os.path.join(data.analysis_path, data.file_name) + '_Physio_Signals.eps')


def averaging_physio(nirx_av_physio, props, data, image_class, trig, gUSBamp_fs, txt):
    '''
    Generates plots of averaged physiological signals
    @param nirx_av_physio: NIRx object of class data_dict including the loaded hdr and xdf data of the selected
    @param props: dict object including all defined settings
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @param image_class: chosen condition (string)
    @param trig: time points of trigger
    @param gUSBamp_fs: Sampling rate of gUSB-amplifier
    @param txt: list including prints displayed to self.output_gb in build_gui()
    @return: txt: list including prints displayed to self.output_gb in build_gui()
    '''
    timing = np.asarray([-int(props['pre_task_length']),
                         int(props['task_length']) + int(props['post_task_length'])])
    if nirx_av_physio.hdr['Bool']['gUSBamp']:
        t_trial_gUSBamp = np.arange(round(timing[0] * gUSBamp_fs),
                                    round(timing[1] * gUSBamp_fs))
        t_trial_gUSBamp_size = t_trial_gUSBamp.size
    data_channel_gUSBamp = np.zeros((trig.shape[0], 1, t_trial_gUSBamp.shape[0]))
    for k in range(1, trig.shape[0]):
        try:
            if nirx_av_physio.hdr['Bool']['gUSBamp']:
                tmp = np.amin(np.abs(nirx_av_physio.time['gUSBamp'] - trig[k]))
                idy = np.where(tmp == np.abs(nirx_av_physio.time['gUSBamp'] - trig[k]))[0]
                b = (timing[0] * gUSBamp_fs) * (-1) + 1  # 1281
                a = t_trial_gUSBamp[0:b]  # x 1281
                c = nirx_av_physio.nirx_data['Heart Rate'][idy + a]
                d = np.mean(c)
                data_channel_gUSBamp[k, 0, :] = nirx_av_physio.nirx_data['Heart Rate'][idy + t_trial_gUSBamp] - d
        except:
            print('Could not process Trigger Nr. %s' % str(k))
            txt.append('Could not process Trigger Nr. %s' % str(k))

    del k, idy

    # averaging and smoothing
    if nirx_av_physio.hdr['Bool']['gUSBamp']:
        data_avg_gUSBamp = np.squeeze(np.mean(data_channel_gUSBamp[:, 0, :], 0))
        data_std_gUSBamp = np.squeeze(np.std(data_channel_gUSBamp[:, 0, :] / np.sqrt(trig.shape[0]), axis=0, ddof=1))

        # auf referenz-intervall referenzieren
        data_avg_gUSBamp = data_avg_gUSBamp - np.mean(data_avg_gUSBamp[0:(timing[0] * gUSBamp_fs) * (-1) + 1])

    if nirx_av_physio.hdr['Bool']['gUSBamp']:
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(t_trial_gUSBamp / 256, data_avg_gUSBamp, 'k-', label='HRV')
        ax.plot(t_trial_gUSBamp / 256, data_avg_gUSBamp - data_std_gUSBamp, 'b-', label='HRV - STD')
        ax.plot(t_trial_gUSBamp / 256, data_avg_gUSBamp + data_std_gUSBamp, 'g-', label='HRV + STD')
        ax.set_xlabel('time (s)')
        ax.set_ylabel(r'($\Delta$ bpm)')
        ax.set(title='Mean HRV %s' % image_class)
        ax.grid()
        ax.set_xlim(timing[0], timing[1])
        ax.set_ylim(np.floor(np.amin(data_avg_gUSBamp - data_std_gUSBamp)),
                    np.ceil(np.amax(data_avg_gUSBamp + data_std_gUSBamp)))
        plt.tight_layout()
        fig.savefig(os.path.join(data.analysis_path, data.file_name) + '_Physio_Signals_Mean.eps')

    return txt
