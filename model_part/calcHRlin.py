import numpy as np
import heartpy as hp
import matplotlib.pyplot as plt
import os


def EHK_calcHRlin(sig, fs, props, data, txt):  # data
    '''
    calculates the linear interpolated heart rate signal
    @param sig: input signal of ecg data
    @param fs: effective sample rate of measurement
    @param props: properties object including all user defined settings
    @param data: data object including parameters like analysis_path, file_name etc.
    @param txt: list including prints displayed to self.output_gb in build_gui()
    @return: estimated heart rate signal

    modified 22.08.2021 by Kris Unterhauser
    This function is modified from calcHRlin.m used in NICA MATLAB version
    '''

    mode = 1
    # pass positive sig, because otherwise the heartpy algorithm detects wrong peaks
    # therefore, multiply by (-1) afterwards to get the same flow as in Matlab
    h_qrs, txt = qrs_detect(sig, fs, 2, txt)
    sig = sig * (-1)
    time = np.round(h_qrs['EVENT']['POS'])
    time = time - 3
    time_in_seconds = time / fs

    # possible correction
    correction = False
    rate = np.diff(time)
    mean_rate = np.mean(rate)
    delete = []
    for i in range(rate.shape[0]):
        if rate[i] < mean_rate / 2:
            if i < rate.shape[0]:
                if rate[i - 1] > rate[i + 1]:
                    delete.append(i + 1)
                else:
                    delete.append(i)
            else:
                delete.append(i)
            correction = True

    delete = np.asarray(delete)
    q = np.diff(time_in_seconds)
    bpm = 60 / q

    if correction and props['generate_biosig_figures']:
        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(7, 5))
        ax1.plot(time_in_seconds, np.append(bpm, bpm[-1]))
        ax1.set(title='Heart Rate')
        ax1.margins(x=0)
        ax2.plot(np.arange(0, (len(sig)/fs), 1/fs), sig)
        ax2.plot(time_in_seconds, sig[time], 'ro')
        ax2.margins(x=0)
        ax2.set(title='detected QRS-peaks')
        print('warning: maybe false positive detected heart beats')
        txt.append('warning: maybe false positive detected heart beats')
        fig.savefig(os.path.join(data.analysis_path, data.file_name) + '_Heart_Rate.eps')

        correct = 'y'
        if correct == 'y':
            time_in_seconds = np.delete(time_in_seconds, delete)
            time = np.delete(time, delete)
            q = np.diff(time_in_seconds)
            bpm = 60 / q

            fig2, (ax3, ax4) = plt.subplots(nrows=2, figsize=(7, 5))
            ax3.plot(time_in_seconds, np.append(bpm, bpm[-1]))
            ax3.set(title='Corrected Heart Rate')
            ax3.margins(x=0)
            ax4.plot(np.arange(0, (len(sig)/fs), 1/fs), sig)
            ax4.plot(time_in_seconds, sig[time], 'ro')
            ax4.margins(x=0)
            ax4.set(title='detected QRS-peaks')
            fig2.savefig(os.path.join(data.analysis_path, data.file_name) + '_Heart_Rate_Corr.eps')

        else:
            print('Wrong input, no correction will be done.')
            txt.append('Wrong input, no correction will be done.')

    # Plausibility check
    for i in range(1, bpm.shape[0]):
        if bpm[i] > 2 * bpm[i - 1]:
            bpm[i] = bpm[i - 1]
        elif bpm[i] < (bpm[i - 1] / 2):
            bpm[i] = bpm[i - 1]

    if mode == 1:
        bpm = np.append(bpm, bpm[-1])
        X = time_in_seconds
        XI = np.arange(time_in_seconds[0], time_in_seconds[-1] + 1 / fs, 1 / fs)
        HR = np.interp(XI, X, bpm)
        HR = np.concatenate((HR[0] * np.ones(time[0]), HR, HR[-1] * np.ones(
            sig.shape[0] - (time[-1]+1))))  # np.ones(time[0] -1)

    
    return HR


def qrs_detect(ecg_sig, fs, mode, txt):  # ecg_sig = gUSBamp_ecg , round(gusbamp['info']['effective_srate'])
    '''
    detects qrs complexes
    @param ecg_sig: ecg signal data
    @param fs: effective sample rate of measurement
    @param mode: Should always remain 2 in the present use case. Originally different modes for detecting qrs-peaks are
    available. For further information refer to the link listed below.
    @return: fiducial points of qrs complexes

    modified 22.08.2021 by Kris Unterhauser
    This function is modified from qrsdetect.m originally used in the Biosig project:
    http://biosig.sourceforge.net/index.html
    '''
    hdr = dict()
    H2 = dict()
    s = ecg_sig
    hdr.update({'SampleRate': fs})
    chan = np.arange(0, s.shape.__len__())

    for k in range(s.shape.__len__()):
        if mode is 2:
            working_data, measures = hp.process(s, fs)
            positions = working_data['peaklist'][0:-2]  # [0:-2] is to get as well 583 values as in Matlab
            # TODO: check the line above again for other files as well, to see if it is always -2
            s = s*(-1)
        else:
            print('Error QRSDETECT: Mode %i not supported' % mode)
            txt.append('Error QRSDETECT: Mode %i not supported' % mode)
        t, sz = trigg(s, positions, int(np.floor(-hdr['SampleRate'])), int(np.ceil(hdr['SampleRate'])))
        tmp = np.nanmax(np.abs(np.mean(np.reshape(t, sz[1:3], order='F'), axis=1)))  # should be mean for each row  # t * (-1)
        # for ix: it takes the first index if it appears more than one time (when calculating the delay),
        # but the same behavior is in Matlab
        ix = np.where(tmp == np.abs(np.mean(np.reshape(t, sz[1:3], order='F'), axis=1)))  # t * (-1)
        delay = hdr['SampleRate'] - ix[0]  # in Matlab it is with + 1, but here we need it like this to be the same
        positions = np.asarray(positions)
        c = positions - delay
        d = np.reshape(positions - delay, (positions.shape[0], 1))
        e = np.tile([int('0501', 16), chan[k]+1, 0], (positions.shape[0], 1))
        abc = (np.reshape(positions - delay, (positions.shape[0], 1)), np.tile([int('0501', 16), chan[k] + 1, 0], (positions.shape[0], 1)))
        ET = np.concatenate((np.reshape(positions - delay, (positions.shape[0], 1)),
                             np.tile([int('0501', 16), chan[k]+1, 0], (positions.shape[0], 1))),
                            axis=1)

    tmp = np.sort(ET[:, 0])  # this value will be unused
    ix = np.argsort(ET[:, 0])
    H2['EVENT'] = dict()
    H2['EVENT']['POS'] = ET[ix, 0]
    H2['EVENT']['TYP'] = ET[ix, 1]
    H2['EVENT']['CHN'] = ET[ix, 2]
    H2['EVENT']['DUR'] = ET[ix, 3]
    H2['EVENT']['SampleRate'] = hdr['SampleRate']
    H2['TYPE'] = 'EVENT'
    return H2, txt


def trigg(sig, trig, pre, post):  # gap
    '''
    Cuts continuous sequence into segments. Missing values (in case sig is to short) are substituted by nan's.
    @param sig: the continuous data sequence (1 channel per column)
    @param trig: defines the trigger points, counted in samples
    @param pre: offset of the start of each segment (relative to trigger), counted in samples
    @param post: offset of the end of each segment (relative to trigger), counted in samples
    @return: x returns array of dimension sz[0], sz[1]*sz[2]
             sz = ndarray([nc, post-pre+1+gap, length(TRIG)])
             sz[0] is the number of channels NS
             sz[1] is the number of samples per trial
             sz[2] is the number of trials, hence, trig.shape[0]

    modified 22.08.2021 by Kris Unterhauser
    This function is modified from trigg.m originally used in the Biosig project:
    http://biosig.sourceforge.net/index.html
    '''
    trig = np.round(trig)
    gap = 0  # not really needed, but included for completeness
    post = int(np.round(post))

    # for the calculation of off and off2:
    # there needs to be added +1 to each value in trig = position, since this value will be used for creating a matrix and not for indexing
    # so otherwise we would miss two values (one for off and one for off2) in matrix construction with concatenate in the if:
    a = np.append(trig + 1, float('inf'))
    b = np.amin(np.append(trig + 1, float('inf')))  # sollte 258 (257) sein
    off = int(np.min((np.amin(np.append(trig + 1, float('inf'))) + pre - 1,
                      0)))  # TODO: check that again: here theoretically without -1; in Matlab = min(513,0), here min(512,0), but in both cases obviously 0
    off2 = int(np.max((np.amax(np.append(trig + 1, float('-inf'))) + post - sig.shape[0], 0)))
    if off != 0 or off2 != 0:
        sig = np.concatenate((np.tile(np.nan, -off, ), sig, np.tile(np.nan, off2, )), axis=0)
        trig = trig - off
    N = post - pre + 1 + gap
    nc = 1  # originally nr of columns of sig, but sig should always be ndarray with only one dimension. If not refer to
    # the original Matlab version
    sz = np.array([nc, N, trig.shape[0]])
    x = np.tile(np.nan, (1, sz[1] * sz[2]))
    for m in range(trig.shape[0]):
        x[:, (m + 1) * N + np.arange(1 - N, -gap + 1) - 1] = sig[trig[m] + np.arange(pre, post+1)]

    return x, sz