def check_probeset(nirx_check, props):
    '''
    Reduces several data related properties stored in NIRx object to the size of the selected probe set.
    Adds new props entry probe_set_val
    @param nirx_check: NIRx object of class data_dict including the loaded hdr and xdf data of the selected measurement
    @param props: dict object including all defined settings
    @return: nirx_check: NIRx object of class data_dict including the loaded hdr and xdf data of the selected
             measurement
             props: dict object including all defined settings
    '''

    probeset_value = props['probe_set']
    if probeset_value == '12':
        props['probe_set_val'] = 1
        channels = 12
        if props['excluded_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        if props['displayed_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        nirx_check.hdr['Sources'][0] = 5
        nirx_check.hdr['Detectors'][0] = 4
        nirx_check.hdr['Gains'][0] = nirx_check.hdr['Gains'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.hdr['SD Mask'][0] = nirx_check.hdr['SD Mask'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.nirx_data['wl760_signal'] = nirx_check.nirx_data['wl760_signal'][:, 0:channels]
        nirx_check.nirx_data['wl850_signal'] = nirx_check.nirx_data['wl850_signal'][:, 0:channels]

    elif probeset_value == '24':
        props['probe_set_val'] = 2
        channels = 24
        if props['excluded_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        if props['displayed_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        nirx_check.hdr['Sources'][0] = 9
        nirx_check.hdr['Detectors'][0] = 24
        nirx_check.hdr['Gains'][0] = nirx_check.hdr['Gains'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.hdr['SD Mask'][0] = nirx_check.hdr['SD Mask'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.nirx_data['wl760_signal'] = nirx_check.nirx_data['wl760_signal'][:, 0:channels]
        nirx_check.nirx_data['wl850_signal'] = nirx_check.nirx_data['wl850_signal'][:, 0:channels]

    elif probeset_value == '38':
        channels = 38
        if props['excluded_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        if props['displayed_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        props['probe_set_val'] = 3
        nirx_check.hdr['Sources'][0] = 9
        nirx_check.hdr['Detectors'][0] = 24
        nirx_check.hdr['Gains'][0] = nirx_check.hdr['Gains'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.hdr['SD Mask'][0] = nirx_check.hdr['SD Mask'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.nirx_data['wl760_signal'] = nirx_check.nirx_data['wl760_signal'][:, 0:channels]
        nirx_check.nirx_data['wl850_signal'] = nirx_check.nirx_data['wl850_signal'][:, 0:channels]

    elif probeset_value == '47':
        channels = 47
        if props['excluded_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        if props['displayed_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        props['probe_set_val'] = 4
        nirx_check.hdr['Sources'][0] = 16
        nirx_check.hdr['Detectors'][0] = 15
        nirx_check.hdr['Gains'][0] = nirx_check.hdr['Gains'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.hdr['SD Mask'][0] = nirx_check.hdr['SD Mask'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.nirx_data['wl760_signal'] = nirx_check.nirx_data['wl760_signal'][:, 0:channels]
        nirx_check.nirx_data['wl850_signal'] = nirx_check.nirx_data['wl850_signal'][:, 0:channels]

    elif probeset_value == '50':  # PSEUDO CASE
        channels = 50
        if props['excluded_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        if props['displayed_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        props['probe_set_val'] = 5
        nirx_check.hdr['Sources'][0] = 16
        nirx_check.hdr['Detectors'][0] = 15
        nirx_check.hdr['Gains'][0] = nirx_check.hdr['Gains'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.hdr['SD Mask'][0] = nirx_check.hdr['SD Mask'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.nirx_data['wl760_signal'] = nirx_check.nirx_data['wl760_signal'][:, 0:channels]
        nirx_check.nirx_data['wl850_signal'] = nirx_check.nirx_data['wl850_signal'][:, 0:channels]

    elif probeset_value == 'Laboratory new':  # is 99:  # Laboratory new
        channels = 24
        if props['excluded_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        if props['displayed_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        props['probe_set_val'] = 6
        nirx_check.hdr['Sources'][0] = 5
        nirx_check.hdr['Detectors'][0] = 4
        nirx_check.hdr['Gains'][0] = nirx_check.hdr['Gains'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.hdr['SD Mask'][0] = nirx_check.hdr['SD Mask'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.nirx_data['wl760_signal'] = nirx_check.nirx_data['wl760_signal'][:, 0:24]
        nirx_check.nirx_data['wl850_signal'] = nirx_check.nirx_data['wl850_signal'][:, 0:24]

    elif probeset_value == 'NIRx Sports old':  # is 777:  # sportsfNIRS_old
        channels = 42
        if props['excluded_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        if props['displayed_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        props['probe_set_val'] = 7
        nirx_check.hdr['Sources'][0] = 14
        nirx_check.hdr['Detectors'][0] = 13
        nirx_check.hdr['Gains'][0] = nirx_check.hdr['Gains'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.hdr['SD Mask'][0] = nirx_check.hdr['SD Mask'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.nirx_data['wl760_signal'] = nirx_check.nirx_data['wl760_signal'][:, 0:42]
        nirx_check.nirx_data['wl850_signal'] = nirx_check.nirx_data['wl850_signal'][:, 0:42]

    elif probeset_value == 'NIRx Sports new':  # is 888:
        channels = 61
        if props['excluded_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        if props['displayed_channels'] != []:
            props['excluded_channels'] = [ex_ch for ex_ch in props['excluded_channels'] if ex_ch <= channels]
        props['probe_set_val'] = 8
        nirx_check.hdr['Sources'][0] = 16
        nirx_check.hdr['Detectors'][0] = 22
        nirx_check.hdr['Gains'][0] = nirx_check.hdr['Gains'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.hdr['SD Mask'][0] = nirx_check.hdr['SD Mask'][0][0:nirx_check.hdr['Sources'][0], 0:nirx_check.hdr['Detectors'][0]]
        nirx_check.nirx_data['wl760_signal'] = nirx_check.nirx_data['wl760_signal'][:, 0:61]
        nirx_check.nirx_data['wl850_signal'] = nirx_check.nirx_data['wl850_signal'][:, 0:61]

    return nirx_check, props