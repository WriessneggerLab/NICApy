import numpy as np

def calculate_conc_change(nirx_conc):
    '''
    Calculates the concentration of the raw input signals
    @param nirx_conc: NIRx object of class data_dict including the loaded hdr and xdf data of the selected measurement
    @return: s_signal1: oxy-Hb
             s_signal2: deoxy-Hb
    '''
    ext_coeff = np.array([[0.1675, 0.06096], [0.07861, 0.11596]])  # [760nm;850nm] cope (new)
    x1 = 1  # DPF für 760nm (x_670)%6.2621
    x2 = 1  # DPF für 850nm (x_890)%4.9048
    d = 1
    inv_ext_coeff = np.linalg.inv(ext_coeff)
    s_signal1 = np.zeros([nirx_conc.nirx_data['wl760_signal'].shape[0], nirx_conc.nirx_data['wl760_signal'].shape[1]])
    s_signal2 = np.zeros([nirx_conc.nirx_data['wl850_signal'].shape[0], nirx_conc.nirx_data['wl850_signal'].shape[1]])

    for i in range(nirx_conc.nirx_data['wl760_signal'].shape[1]):
        raw_data = np.zeros([nirx_conc.nirx_data['wl760_signal'].shape[0], 2])
        raw_data[:, 0] = np.asarray(nirx_conc.nirx_data['wl760_signal'][:, i])
        raw_data[:, 1] = np.asarray(nirx_conc.nirx_data['wl850_signal'][:, i])
        raw_data0_temp = np.reshape(raw_data[:, 0], (raw_data[:, 0].shape[0], 1))
        raw_data1_temp = np.reshape(raw_data[:, 1], (raw_data[:, 1].shape[0], 1))

        data = np.concatenate((raw_data0_temp.T, raw_data1_temp.T), axis=0)
        A = np.zeros([data.shape[0], data.shape[1] - 1])
        A[0, :] = (np.log10(data[0, :-1] / data[0, 1:])) / (x1 * d)
        A[1, :] = (np.log10(data[1, :-1] / data[1, 1:])) / (x2 * d)

        C = np.zeros(A.shape).T  # Notwendig da sonst die alten Daten erhalten bleiben

        for g in range(A.shape[1]):
            C[g, 0] = np.dot(inv_ext_coeff[0, :], A[:, g])
            C[g, 1] = np.dot(inv_ext_coeff[1, :], A[:, g])

        concentration = np.cumsum(C, axis=0)

        s_signal1[:, i] = np.append(concentration[0, 0], concentration[:, 0])
        s_signal2[:, i] = np.append(concentration[0, 1], concentration[:, 1])

        del raw_data, data, A, C, concentration, raw_data0_temp, raw_data1_temp

    return s_signal1, s_signal2