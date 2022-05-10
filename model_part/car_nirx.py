import numpy as np

def car_NIRx(oxy_signal, deoxy_signal, props):
    '''
    Applies Common Average (CAR) method to oxy and deoxy signals
    @param oxy_signal: oxy signal
    @param deoxy_signal: deoxy signal
    @param props: dict object including all defined settings
    @return: oxy_signal: oxy signal after applied CAR
             deoxy_signal: deoxy signal after applied CAR
    '''

    refused_channels = []

    if props['optode_failure_val']:
        optode_failure = props['optode_failure_list']
        failed_channs = []
        for i in range(len(optode_failure[0])):
            failed_channs.append(optode_failure[0][i])

        for i in range(len(failed_channs)):
            refused_channels.append(failed_channs[i])

    excluded_channels = props['excluded_channels']

    if len(excluded_channels) != 0:
        for i in range(len(excluded_channels)):
            refused_channels.append(excluded_channels[i])

    refused_channels = np.unique(np.asarray(refused_channels))
    car_chans = np.arange(oxy_signal.shape[1])

    # tries if refused_channels is not empty, otherwise jumps into except block
    try:
        car_chans = np.delete(car_chans, refused_channels-1)  # -1 for indexing: channel nr -1 since in python it starts with 0
    except:
        car_chans = car_chans

    mean_oxy_signal = np.mean(oxy_signal[:, car_chans], 1)
    mean_deoxy_signal = np.mean(deoxy_signal[:, car_chans], 1)

    for tt in range(oxy_signal.shape[1]):
        oxy_signal[:, tt] = oxy_signal[:, tt] - mean_oxy_signal
        deoxy_signal[:, tt] = deoxy_signal[:, tt] - mean_deoxy_signal

    return oxy_signal, deoxy_signal