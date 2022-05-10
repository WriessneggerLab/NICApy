from scipy import stats
import numpy as np
import pickle
import os


def single_t_test(fname):
    '''
    Performs a one sample t-test in order to check if the averaged signal per channel is different from 0.
    @param fname: filename to load the pickle file
    @return: tt_output: list to display in the GUI
    '''
    with open(fname, 'rb') as nirx_obj:
        nirx_tt = pickle.load(nirx_obj)

    oxy_Hb = nirx_tt.nirx_data['avg_oxy'].T
    deoxy_Hb = nirx_tt.nirx_data['avg_deoxy'].T

    channels_excluded = nirx_tt.properties['excluded_channels']

    # take the absolute values, otherwise it could be that positive and negative values cancel out each other
    oxy_Hb = np.abs(oxy_Hb)
    deoxy_Hb = np.abs(deoxy_Hb)

    t_oxy, p_oxy = stats.ttest_1samp(oxy_Hb, popmean=0, axis=1)
    t_deoxy, p_deoxy = stats.ttest_1samp(deoxy_Hb, popmean=0, axis=1)

    nan_list = []
    if len(channels_excluded) != 0:
        # check if excluded channels agrees with nan-values in p-values

        excl_chans_nan_oxy = np.argwhere(np.isnan(p_oxy))
        excl_chans_nan_deoxy = np.argwhere(np.isnan(p_deoxy))
        try:
            excl_chans_nan_deoxy == excl_chans_nan_oxy
        except Exception:
            print('T-test not possible.')
            return

        for i in range(excl_chans_nan_oxy.shape[0]):
            nan_list.append(excl_chans_nan_oxy[0][i])

        try:
            sorted(nan_list) == sorted(channels_excluded)
        except Exception as err:
            print(err)
            return

    channs_ok_oxy = [indx+1 for indx, p in enumerate(p_oxy) if p < 0.05]
    channs_not_ok_oxy = [indx+1 for indx, p in enumerate(p_oxy) if p >= 0.05]

    channs_ok_deoxy = [indx + 1 for indx, p in enumerate(p_deoxy) if p < 0.05]
    channs_not_ok_deoxy = [indx + 1 for indx, p in enumerate(p_deoxy) if p >= 0.05]

    tt_output = []
    fname = os.path.splitext(fname)[0]
    with open(fname + '_T-Test_Output_File.txt', 'w') as f:
        f.write('T-test: Null hypothesis: mean of each channel = 0\n')
        tt_output.append('T-test: Null hypothesis: mean of each channels = 0')
        f.write('Reject Null hypothesis if p < 0.05 \n')
        tt_output.append('Reject Null hypothesis if p < 0.05')
        if len(channels_excluded) != 0:
            f.write('Excluded channels:\n')
            tt_output.append('Excluded channels:')
            f.writelines("%s ," % ch for ch in channels_excluded)
            f.write('\n')
            chans_to_disp = []
            for ch in channels_excluded:
                chans_to_disp.append('%s , ' % ch)
            str_to_disp = ''
            tt_output.append(str_to_disp.join(chans_to_disp))
            f.write('T-test for excluded channels is not possible.\n')
            tt_output.append('T-test for excluded channels is not possible.')

        if channs_ok_oxy == channs_ok_deoxy and channs_not_ok_oxy == channs_not_ok_deoxy:
            f.write('All included channels are ok!\n')
            tt_output.append('All included channels are ok!')
            f.write('Null Hypothesis can be rejected for both, oxy-Hb and deoxy-Hb.\n')
            tt_output.append('Null Hypothesis can be rejected for both, oxy-Hb and deoxy-Hb.')
        else:
            f.write('Check channels oxy-Hb or channels deoxy-Hb again.\n')
            tt_output.append('Check channels oxy-Hb or channels deoxy-Hb again.')

        if len(channs_ok_oxy) != 0:
            f.write('Channels of oxy-Hb for which the Null hypothesis is rejected: \n')
            tt_output.append('Channels of oxy-Hb for which the Null hypothesis is rejected:')
            f.writelines("%s ," % ch for ch in channs_ok_oxy)
            chans_to_disp = []
            for ch in channs_ok_oxy:
                chans_to_disp.append('%s , ' % ch)
            str_to_disp = ''
            tt_output.append(str_to_disp.join(chans_to_disp))
            f.write('\n')

        if len(channs_not_ok_oxy) != 0:
            f.write('Channels of oxy-Hb for which the Null hypothesis is not rejected: \n')
            tt_output.append('Channels of oxy-Hb for which the Null hypothesis is not rejected:')
            f.writelines("%s ," % ch for ch in channs_not_ok_oxy)
            chans_to_disp = []
            for ch in channs_not_ok_oxy:
                chans_to_disp.append('%s , ' % ch)
            str_to_disp = ''
            tt_output.append(str_to_disp.join(chans_to_disp))
            f.write('\n')

        if len(channs_ok_deoxy) != 0:
            f.write('Channels of deoxy-Hb for which the Null hypothesis is rejected: \n')
            tt_output.append('Channels of deoxy-Hb for which the Null hypothesis is rejected:')
            f.writelines("%s ," % ch for ch in channs_ok_deoxy)
            chans_to_disp = []
            for ch in channs_ok_deoxy:
                chans_to_disp.append('%s , ' % ch)
            str_to_disp = ''
            tt_output.append(str_to_disp.join(chans_to_disp))
            f.write('\n')

        if len(channs_not_ok_deoxy) != 0:
            f.write('Channels of deoxy-Hb for which the Null hypothesis is not rejected: \n')
            tt_output.append('Channels of deoxy-Hb for which the Null hypothesis is not rejected:')
            f.writelines("%s ," % ch for ch in channs_not_ok_deoxy)
            chans_to_disp = []
            for ch in channs_not_ok_deoxy:
                chans_to_disp.append('%s , ' % ch)
            str_to_disp = ''
            tt_output.append(str_to_disp.join(chans_to_disp))
            f.write('\n')


        f.write('t-statistics oxy-Hb: \n' + str(t_oxy) + '\n')
        f.write('p-value oxy-Hb: \n' + str(p_oxy) + '\n')

        f.write('t-statistics deoxy-Hb: \n' + str(t_deoxy) + '\n')
        f.write('p-value deoxy-Hb: \n' + str(p_deoxy) + '\n')

    del nirx_tt
    return tt_output
