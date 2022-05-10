import numpy as np
import matplotlib.pyplot as plt
import os


def generate_headplot(nirx_head, props, data):
    '''
    Genereates head plot according the optode placement of the selected probe set
    @param nirx_head: NIRx object of class data_dict including the loaded hdr and xdf data of the selected measurement
    @param props: dict object including all defined settings
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @return: nirx_head
    '''
    if props['signal_imaging'] == 'Averaging over Trials':
        head_oxy = nirx_head.nirx_data['avg_oxy']
        head_deoxy = nirx_head.nirx_data['avg_deoxy']
        t_trial = nirx_head.properties['t_trial']
    elif props['signal_imaging'] == 'Continuous':
        head_oxy = nirx_head.nirx_data['all_trials_oxy_continuous']
        head_deoxy = nirx_head.nirx_data['all_trials_deoxy_continuous']
        t_trial = np.arange(1, head_oxy.shape[0]+1)
        t_trial = t_trial * 2*len(props['available_conditions']) / 60  # * nr. of conditions / convert to minutes

    head_oxy_std = nirx_head.nirx_data['avg_oxy_std']
    head_deoxy_std = nirx_head.nirx_data['avg_deoxy_std']
    fs = nirx_head.properties['fs']

    # visualization average new  --> see Matlab Version
    if props['generate_single_conc_change_figures']:
        visualization_nirx_sigma(head_oxy, head_deoxy, head_oxy_std, head_deoxy_std, props, t_trial=t_trial, fs=fs,
                                 data=data)

    return nirx_head


def visualization_nirx_sigma(oxy_sig, deoxy_sig, std_oxy_sig, std_deoxy_sig, props, t_trial, fs, data):
    '''
    This function should use a for loop for plotting, but has been changed lately during the development process
    Visualizes head plot and individual channels contained in properties in 'displayed_channels'
    @param oxy_sig: input oxy signal
    @param deoxy_sig: input deoxy signal
    @param std_oxy_sig: input std-oxy signal
    @param std_deoxy_sig: input std-deoxy signal
    @param props: dict object including all defined settings
    @param t_trial: time points of trial inclduing pre timing
    @param fs: sampling rate
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @return:
    '''
    if props['signal_imaging'] == 'Averaging over Trials':
        timing = np.asarray([-int(props['pre_task_length']),
                             int(props['task_length']) + int(props['post_task_length'])])
    elif props['signal_imaging'] == 'Continuous':
        timing = np.array([1, oxy_sig.shape[0]])

    exclude_channs = props['excluded_channels']
    start = 0
    end = props['task_length']
    channs_to_disp = props['displayed_channels']
    probeset_val = props['probe_set_val']
    c_min = float(str(props['conc_range_lower']))
    c_max = float(str(props['conc_range_upper']))

    all_channs = list(range(1, oxy_sig.shape[1] + 1))
    remaining_channs = [ch for ch in all_channs if ch not in exclude_channs]

    probe_set_val5 = {'1': [12, 21, 10], '2': [12, 21, 30],
                      '3': [12, 21, 12], '4': [12, 21, 34],
                      '5': [12, 21, 32], '6': [12, 21, 54],
                      '7': [12, 21, 52], '8': [12, 21, 74],
                      '9': [12, 21, 72], '10': [12, 21, 94],
                      '11': [12, 21, 76], '12': [12, 21, 96],
                      '13': [12, 21, 144], '14': [12, 21, 142],
                      '15': [12, 21, 164], '16': [12, 21, 140],
                      '17': [12, 21, 138], '18': [12, 21, 160],
                      '19': [12, 21, 136], '20': [12, 21, 134],
                      '21': [12, 21, 156], '22': [12, 21, 132],
                      '23': [12, 21, 130], '24': [12, 21, 152],
                      '25': [12, 21, 162], '26': [12, 21, 184],
                      '27': [12, 21, 182], '28': [12, 21, 204],
                      '29': [12, 21, 158], '30': [12, 21, 180],
                      '31': [12, 21, 178], '32': [12, 21, 200],
                      '33': [12, 21, 154], '34': [12, 21, 176],
                      '35': [12, 21, 174], '36': [12, 21, 196],
                      '37': [12, 21, 206], '38': [12, 21, 228],
                      '39': [12, 21, 226], '40': [12, 21, 202],
                      '41': [12, 21, 224], '42': [12, 21, 222],
                      '43': [12, 21, 244], '44': [12, 21, 198],
                      '45': [12, 21, 220], '46': [12, 21, 218],
                      '47': [12, 21, 240], '48': [12, 21, 194],
                      '49': [12, 21, 216], '50': [12, 21, 214],
                      }

    probe_set_val1 = {'1': [5, 5, 24], '2': [5, 5, 20],
                      '3': [5, 5, 22], '4': [5, 5, 16],
                      '5': [5, 5, 18], '6': [5, 5, 12],
                      '7': [5, 5, 14], '8': [5, 5, 8],
                      '9': [5, 5, 10], '10': [5, 5, 4],
                      '11': [5, 5, 6], '12': [5, 5, 2],
                      }

    '''probe_set_val3 = {
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
    }'''

    probe_set_val3 = {
        '1': [7, 17, 10], '2': [7, 17, 11],
        '3': [7, 17, 26], '4': [7, 17, 43],
        '5': [7, 17, 13], '6': [7, 17, 14],
        '7': [7, 17, 32], '8': [7, 17, 49],
        '9': [7, 17, 53], '10': [7, 17, 55],
        '11': [7, 17, 56], '12': [7, 17, 58],
        '13': [7, 17, 59], '14': [7, 17, 74],
        '15': [7, 17, 91], '16': [7, 17, 29],
        '17': [7, 17, 46], '18': [7, 17, 61],
        '19': [7, 17, 62], '20': [7, 17, 64],
        '21': [7, 17, 65], '22': [7, 17, 80],
        '23': [7, 17, 97], '24': [7, 17, 67],
        '25': [7, 17, 71], '26': [7, 17, 88],
        '27': [7, 17, 106], '28': [7, 17, 107],
        '29': [7, 17, 77], '30': [7, 17, 94],
        '31': [7, 17, 109], '32': [7, 17, 110],
        '33': [7, 17, 112], '34': [7, 17, 113],
        '35': [7, 17, 83], '36': [7, 17, 100],
        '37': [7, 17, 115], '38': [7, 17, 116],
    }

    probe_set_val2 = {
        '1': [4, 10, 4], '2': [4, 10, 5],
        '3': [4, 10, 13], '4': [4, 10, 23],
        '5': [4, 10, 7], '6': [4, 10, 8],
        '7': [4, 10, 19], '8': [4, 10, 29],
        '12': [4, 10, 31], '13': [4, 10, 32],
        '16': [4, 10, 16], '17': [4, 10, 26],
        '18': [4, 10, 34], '19': [4, 10, 35],
        '20': [4, 10, 37], '21': [4, 10, 38],
        '24': [4, 10, 40]
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
    # fig.suptitle('Average of Channels 1-61', fontsize=12)
    if probeset_val == 8:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for chan_num in remaining_channs:
            make_plot = fig.add_subplot(14, 13, probe_set_val8[str(chan_num)][2])
            if props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial/fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(t_trial/fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            elif props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial/fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial/fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial/fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial/fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            x_ticks = [timing[0], 0, timing[1]]
            y_ticks = [c_min, c_max]
            make_plot.set_xlim(timing[0], timing[1])
            # make_plot.set_xticks(x_ticks)
            make_plot.set_ylim(c_min, c_max)
            make_plot.set_yticks(y_ticks)
            make_plot.set_title('Ch' + str(chan_num), fontsize=5, pad=1)
            make_plot.xaxis.set_major_locator(plt.MaxNLocator(3))
            # make_plot.yaxis.set_major_locator(plt.MaxNLocator(3))
            make_plot.tick_params(axis='both', labelsize=4, pad=1)
            make_plot.axvline(start, color='k', linewidth=1)
            make_plot.axvline(end, color='k', linewidth=1)

            ### plot individual channel
            if chan_num in channs_to_disp and 'grand_average' not in props:
                fig_chan, ax = plt.subplots(figsize=(7, 4))
                if props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial/fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(t_trial/fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                if props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                ax.grid()
                if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial/fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial/fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial/fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial/fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')

                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig), np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig),
                                                                           np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, 0.1)
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), 0.1)

                ### plot the two vertical lines
                ax.axvline(start, color='k', linewidth=2)
                ax.axvline(end, color='k', linewidth=2)
                ax.set_title('Avg. Concentration Change of Channel ' + str(chan_num), fontsize=12, fontweight='bold')
                ax.set_xlim(timing[0], timing[1])
                ax.set_xlabel('Time (s)', fontsize=12)
                ax.set_ylabel(r'$\Delta$ ' + 'c (mM*mm)', fontsize=12)
                fig_chan.legend()
                if 'grand_average' in props:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path_cond,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) + '.eps')
                else:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) +
                        props['signal_analysis_method'] + '_' + props['correction_mode'] + '.eps')
        

    elif probeset_val == 7:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for chan_num in remaining_channs:
            make_plot = fig.add_subplot(5, 17, probe_set_val7[str(chan_num)][2])
            if props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            elif props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            x_ticks = [timing[0], 0, timing[1]]
            y_ticks = [c_min, c_max]
            make_plot.set_xlim(timing[0], timing[1])
            # make_plot.set_xticks(x_ticks)
            make_plot.set_ylim(c_min, c_max)
            make_plot.set_yticks(y_ticks)
            make_plot.set_title('Ch' + str(chan_num), fontsize=5, pad=1)
            make_plot.xaxis.set_major_locator(plt.MaxNLocator(3))
            # make_plot.yaxis.set_major_locator(plt.MaxNLocator(3))
            make_plot.tick_params(axis='both', labelsize=4, pad=1)
            make_plot.axvline(start, color='k', linewidth=1)
            make_plot.axvline(end, color='k', linewidth=1)

            ### plot individual channel
            if chan_num in channs_to_disp and 'grand_average' not in props:
                fig_chan, ax = plt.subplots(figsize=(7, 4))
                if props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                if props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                ax.grid()
                if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')

                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig), np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig),
                                                                           np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, 0.1)
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), 0.1)

                ### plot the two vertical lines
                ax.axvline(start, color='k', linewidth=2)
                ax.axvline(end, color='k', linewidth=2)
                ax.set_title('Avg. Concentration Change of Channel ' + str(chan_num), fontsize=12, fontweight='bold')
                ax.set_xlim(timing[0], timing[1])
                ax.set_xlabel('Time (s)', fontsize=12)
                ax.set_ylabel(r'$\Delta$ ' + 'c (mM*mm)', fontsize=12)
                fig_chan.legend(loc='best')
                if 'grand_average' in props:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path_cond,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) + '.eps')
                else:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) +
                        props['signal_analysis_method'] + '_' + props['correction_mode'] + '.eps')
        

    elif probeset_val == 6:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for chan_num in remaining_channs:
            make_plot = fig.add_subplot(5, 11, probe_set_val6[str(chan_num)][2])
            if props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            elif props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            x_ticks = [timing[0], 0, timing[1]]
            y_ticks = [c_min, c_max]
            make_plot.set_xlim(timing[0], timing[1])
            # make_plot.set_xticks(x_ticks)
            make_plot.set_ylim(c_min, c_max)
            make_plot.set_yticks(y_ticks)
            make_plot.set_title('Ch' + str(chan_num), fontsize=5, pad=1)
            make_plot.xaxis.set_major_locator(plt.MaxNLocator(3))
            # make_plot.yaxis.set_major_locator(plt.MaxNLocator(3))
            make_plot.tick_params(axis='both', labelsize=4, pad=1)
            make_plot.axvline(start, color='k', linewidth=1)
            make_plot.axvline(end, color='k', linewidth=1)

            ### plot individual channel
            if chan_num in channs_to_disp and 'grand_average' not in props:
                fig_chan, ax = plt.subplots(figsize=(7, 4))
                if props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                if props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                ax.grid()
                if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')

                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig), np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig),
                                                                           np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, 0.1)
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), 0.1)

                ### plot the two vertical lines
                ax.axvline(start, color='k', linewidth=2)
                ax.axvline(end, color='k', linewidth=2)
                ax.set_title('Avg. Concentration Change of Channel ' + str(chan_num), fontsize=12, fontweight='bold')
                ax.set_xlim(timing[0], timing[1])
                ax.set_xlabel('Time (s)', fontsize=12)
                ax.set_ylabel(r'$\Delta$ ' + 'c (mM*mm)', fontsize=12)
                fig_chan.legend(loc='best')
                if 'grand_average' in props:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path_cond,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) + '.eps')
                else:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) +
                        props['signal_analysis_method'] + '_' + props['correction_mode'] + '.eps')
        

    elif probeset_val == 5:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for chan_num in remaining_channs:
            make_plot = fig.add_subplot(12, 21, probe_set_val5[str(chan_num)][2])
            if props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            elif props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            x_ticks = [timing[0], 0, timing[1]]
            y_ticks = [c_min, c_max]
            make_plot.set_xlim(timing[0], timing[1])
            # make_plot.set_xticks(x_ticks)
            make_plot.set_ylim(c_min, c_max)
            make_plot.set_yticks(y_ticks)
            make_plot.set_title('Ch' + str(chan_num), fontsize=5, pad=1)
            make_plot.xaxis.set_major_locator(plt.MaxNLocator(3))
            # make_plot.yaxis.set_major_locator(plt.MaxNLocator(3))
            make_plot.tick_params(axis='both', labelsize=4, pad=1)
            make_plot.axvline(start, color='k', linewidth=1)
            make_plot.axvline(end, color='k', linewidth=1)

            ### plot individual channel
            if chan_num in channs_to_disp and 'grand_average' not in props:
                fig_chan, ax = plt.subplots(figsize=(7, 4))
                if props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                if props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                ax.grid()
                if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')

                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig), np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig),
                                                                           np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, 0.1)
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), 0.1)

                ### plot the two vertical lines
                ax.axvline(start, color='k', linewidth=2)
                ax.axvline(end, color='k', linewidth=2)
                ax.set_title('Avg. Concentration Change of Channel ' + str(chan_num), fontsize=12, fontweight='bold')
                ax.set_xlim(timing[0], timing[1])
                ax.set_xlabel('Time (s)', fontsize=12)
                ax.set_ylabel(r'$\Delta$ ' + 'c (mM*mm)', fontsize=12)
                fig_chan.legend(loc='best')
                if 'grand_average' in props:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path_cond,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) + '.eps')
                else:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) +
                        props['signal_analysis_method'] + '_' + props['correction_mode'] + '.eps')
        

    elif probeset_val == 4:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for chan_num in remaining_channs:
            make_plot = fig.add_axes(probe_set_val4[str(chan_num)])
            if props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial/fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(t_trial/fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            elif props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            x_ticks = [timing[0], 0, timing[1]]
            y_ticks = [c_min, c_max]
            make_plot.set_xlim(timing[0], timing[1])
            # make_plot.set_xticks(x_ticks)
            make_plot.set_ylim(c_min, c_max)
            make_plot.set_yticks(y_ticks)
            make_plot.set_title('Ch' + str(chan_num), fontsize=5, pad=1)
            make_plot.xaxis.set_major_locator(plt.MaxNLocator(3))
            # make_plot.yaxis.set_major_locator(plt.MaxNLocator(3))
            make_plot.tick_params(axis='both', labelsize=4, pad=1)
            make_plot.axvline(start, color='k', linewidth=1)
            make_plot.axvline(end, color='k', linewidth=1)

            ### plot individual channel
            if chan_num in channs_to_disp and 'grand_average' not in props:
                fig_chan, ax = plt.subplots(figsize=(7, 4))
                if props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                if props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                ax.grid()
                if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')

                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig), np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig),
                                                                           np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, 0.1)
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), 0.1)

                ### plot the two vertical lines
                ax.axvline(start, color='k', linewidth=2)
                ax.axvline(end, color='k', linewidth=2)
                ax.set_title('Avg. Concentration Change of Channel ' + str(chan_num), fontsize=12, fontweight='bold')
                ax.set_xlim(timing[0], timing[1])
                ax.set_xlabel('Time (s)', fontsize=12)
                ax.set_ylabel(r'$\Delta$ ' + 'c (mM*mm)', fontsize=12)
                fig_chan.legend(loc='best')
                if 'grand_average' in props:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path_cond,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) + '.eps')
                else:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) +
                        props['signal_analysis_method'] + '_' + props['correction_mode'] + '.eps')
        

    elif probeset_val == 3:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for chan_num in remaining_channs:
            make_plot = fig.add_subplot(7, 17, probe_set_val3[str(chan_num)][2])
            if props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            elif props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            x_ticks = [timing[0], 0, timing[1]]
            y_ticks = [c_min, c_max]
            make_plot.set_xlim(timing[0], timing[1])
            # make_plot.set_xticks(x_ticks)
            make_plot.set_ylim(c_min, c_max)
            make_plot.set_yticks(y_ticks)
            make_plot.set_title('Ch' + str(chan_num), fontsize=5, pad=1)
            make_plot.xaxis.set_major_locator(plt.MaxNLocator(3))
            # make_plot.yaxis.set_major_locator(plt.MaxNLocator(3))
            make_plot.tick_params(axis='both', labelsize=4, pad=1)
            make_plot.axvline(start, color='k', linewidth=1)
            make_plot.axvline(end, color='k', linewidth=1)

            ### plot individual channel
            if chan_num in channs_to_disp and 'grand_average' not in props:
                fig_chan, ax = plt.subplots(figsize=(7, 4))
                if props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                if props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                ax.grid()
                if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig), np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig),
                                                                           np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, 0.1)
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), 0.1)

                ### plot the two vertical lines
                ax.axvline(start, color='k', linewidth=2)
                ax.axvline(end, color='k', linewidth=2)
                ax.set_title('Avg. Concentration Change of Channel ' + str(chan_num), fontsize=12, fontweight='bold')
                ax.set_xlim(timing[0], timing[1])
                ax.set_xlabel('Time (s)', fontsize=12)
                ax.set_ylabel(r'$\Delta$ ' + 'c (mM*mm)', fontsize=12)
                fig_chan.legend(loc='best')
                if 'grand_average' in props:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path_cond,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) + '.eps')
                else:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) +
                        props['signal_analysis_method'] + '_' + props['correction_mode'] + '.eps')
        

    elif probeset_val == 2:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for chan_num in remaining_channs:
            make_plot = fig.add_subplot(4, 10, probe_set_val2[str(chan_num)][2])
            if props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            elif props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            x_ticks = [timing[0], 0, timing[1]]
            y_ticks = [c_min, c_max]
            make_plot.set_xlim(timing[0], timing[1])
            # make_plot.set_xticks(x_ticks)
            make_plot.set_ylim(c_min, c_max)
            make_plot.set_yticks(y_ticks)
            make_plot.set_title('Ch' + str(chan_num), fontsize=5, pad=1)
            make_plot.xaxis.set_major_locator(plt.MaxNLocator(3))
            # make_plot.yaxis.set_major_locator(plt.MaxNLocator(3))
            make_plot.tick_params(axis='both', labelsize=4, pad=1)
            make_plot.axvline(start, color='k', linewidth=1)
            make_plot.axvline(end, color='k', linewidth=1)

            ### plot individual channel
            if chan_num in channs_to_disp and 'grand_average' not in props:
                fig_chan, ax = plt.subplots(figsize=(7, 4))
                if props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                if props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                ax.grid()
                if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')

                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig), np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig),
                                                                           np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, 0.1)
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), 0.1)

                ### plot the two vertical lines
                ax.axvline(start, color='k', linewidth=2)
                ax.axvline(end, color='k', linewidth=2)
                ax.set_title('Avg. Concentration Change of Channel ' + str(chan_num), fontsize=12, fontweight='bold')
                ax.set_xlim(timing[0], timing[1])
                ax.set_xlabel('Time (s)', fontsize=12)
                ax.set_ylabel(r'$\Delta$ ' + 'c (mM*mm)', fontsize=12)
                fig_chan.legend(loc='best')
                if 'grand_average' in props:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path_cond,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) + '.eps')
                else:
                    fig_chan.savefig(
                    os.path.join(data.analysis_path,
                                 data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) +
                    props['signal_analysis_method'] + '_' + props['correction_mode'] + '.eps')
        

    elif probeset_val == 1:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for chan_num in remaining_channs:
            make_plot = fig.add_subplot(5, 5, probe_set_val1[str(chan_num)][2])
            if props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            elif props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=1)
                make_plot.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=1)
            if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                make_plot.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1],
                               color=(1, 0.6, 0.5), linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
                make_plot.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                               linewidth=1, linestyle='dotted')
            x_ticks = [timing[0], 0, timing[1]]
            y_ticks = [c_min, c_max]
            make_plot.set_xlim(timing[0], timing[1])
            # make_plot.set_xticks(x_ticks)
            make_plot.set_ylim(c_min, c_max)
            make_plot.set_yticks(y_ticks)
            make_plot.set_title('Ch' + str(chan_num), fontsize=5, pad=1)
            make_plot.xaxis.set_major_locator(plt.MaxNLocator(3))
            # make_plot.yaxis.set_major_locator(plt.MaxNLocator(3))
            make_plot.tick_params(axis='both', labelsize=4, pad=1)
            make_plot.axvline(start, color='k', linewidth=1)
            make_plot.axvline(end, color='k', linewidth=1)

            ### plot individual channel
            if chan_num in channs_to_disp and 'grand_average' not in props:
                fig_chan, ax = plt.subplots(figsize=(7, 4))
                if props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                if props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5), linewidth=2, label='[oxy_Hb]')
                    ax.plot(deoxy_sig[:, chan_num - 1], color='b', linewidth=2, label='[deoxy_Hb]')
                ax.grid()
                if props['generate_std_plot'] and props['signal_imaging'] == 'Averaging over Trials':
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(t_trial / fs, deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                if props['generate_std_plot'] and props['signal_imaging'] == 'Continuous':
                    ax.plot(oxy_sig[:, chan_num - 1] + std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(oxy_sig[:, chan_num - 1] - std_oxy_sig[:, chan_num - 1], color=(1, 0.6, 0.5),
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] + std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')
                    ax.plot(deoxy_sig[:, chan_num - 1] - std_deoxy_sig[:, chan_num - 1], color='b',
                            linewidth=2, linestyle='dotted')

                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig), np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) > 0.1 and min(np.amin(oxy_sig),
                                                                           np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, max(np.amax(oxy_sig), np.amax(deoxy_sig)))
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) >= -0.1:
                    ax.set_ylim(-0.1, 0.1)
                if max(np.amax(oxy_sig), np.amax(deoxy_sig)) <= 0.1 and min(np.amin(oxy_sig),
                                                                            np.amin(deoxy_sig)) < -0.1:
                    ax.set_ylim(min(np.amin(oxy_sig), np.amin(deoxy_sig)), 0.1)

                ### plot the two vertical lines
                ax.axvline(start, color='k', linewidth=2)
                ax.axvline(end, color='k', linewidth=2)
                ax.set_title('Avg. Concentration Change of Channel ' + str(chan_num), fontsize=12, fontweight='bold')
                ax.set_xlim(timing[0], timing[1])
                ax.set_xlabel('Time (s)', fontsize=12)
                ax.set_ylabel(r'$\Delta$ ' + 'c (mM*mm)', fontsize=12)
                fig_chan.legend(loc='best')
                if 'grand_average' in props:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path_cond,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) + '.eps')
                else:
                    fig_chan.savefig(
                        os.path.join(data.analysis_path,
                                     data.file_name) + '_Conc_Chg_Avg' + '_Ch_' + str(chan_num) +
                        props['signal_analysis_method'] + '_' + props['correction_mode'] + '.eps')
        

    #image_class_string = props['chosen_condition']
    #c = [int(props['condition_markers'][marker]) for marker in range(len(props['available_conditions'])) if
     #    props['available_conditions'][marker] == image_class_string]
    if 'grand_average' in props:
        fig.savefig(
            os.path.join(data.analysis_path_cond, 'Channels_Average' + '.eps'))
    else:
        fig.savefig(
            os.path.join(data.analysis_path, data.file_name) + '_Channels_Average_' +
            props['signal_analysis_method'] + '_' + props['correction_mode'] + '.eps')

    '''
    elif probeset_val is 3:
        fig.subplots_adjust(hspace=0.4, wspace=0.8)
        for ix, channel_number in enumerate(included_channels):
            ax = fig.add_axes(probe_set_val3[str(channel_number)])
            ax.tick_params(axis='both', labelsize=5, pad=1)
            ax.set_xlabel('time [s]', size=5, labelpad=1)
            ax.plot(f_oxy[indx], 10 * np.log10(pxx_oxy[indx, ix]), color='r')
            ax.plot(f_oxy[indx], 10 * np.log10(pxx_deoxy[indx, ix]), color='b')
        # '''
