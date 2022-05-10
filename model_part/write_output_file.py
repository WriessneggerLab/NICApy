import numpy as np
import xlsxwriter
import os
import json
import pickle

def write_output_file(nirx_output, props, data):
    '''
    Writes final oxy-Hb and deoxy-Hb values to a separate xlsx file and saves data to a *.npz file
    @param nirx_output: NIRx object of class data_dict including the loaded hdr and xdf data of the selected measurement
    @param props: dict object including all defined settings
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @return: text: list including prints displayed to self.output_gb in build_gui()
    '''
    text = []
    text.append('Write Output Files start')
    filename_oxy = os.path.join(data.analysis_path, data.file_name) + '_' + props['task_name'] + '_' + props[
        'chosen_condition'] + '_signal_oxy.xlsx'
    filename_deoxy = os.path.join(data.analysis_path, data.file_name) + '_' + props['task_name'] + '_' + props[
        'chosen_condition'] + '_signal_deoxy.xlsx'
    oxy = nirx_output.nirx_data['oxy_Hb'].T
    deoxy = nirx_output.nirx_data['deoxy_Hb'].T

    cell_1 = 'time (s)'
    time_points = np.linspace(1, oxy.shape[1], oxy.shape[1], endpoint=True, dtype=int)
    chan_list = ['Ch' + str(ch + 1) for ch in range(0, 61)]

    # create xlsx sheets
    data_oxy = xlsxwriter.Workbook(filename_oxy)
    oxy_worksheet = data_oxy.add_worksheet('oxy-Hb')
    data_deoxy = xlsxwriter.Workbook(filename_deoxy)
    deoxy_worksheet = data_deoxy.add_worksheet('deoxy-Hb')

    # write first cell
    oxy_worksheet.write(0, 0, cell_1)
    deoxy_worksheet.write(0, 0, cell_1)

    # write first col
    for chan in range(len(chan_list)):
        oxy_worksheet.write(chan + 1, 0, chan_list[chan])
        deoxy_worksheet.write(chan + 1, 0, chan_list[chan])

    # write first row
    for point in range(len(time_points)):
        oxy_worksheet.write(0, point + 1, time_points[point])
        deoxy_worksheet.write(0, point + 1, time_points[point])

    # write data
    for line_oxy, row_oxy in enumerate(oxy):
        for single_oxy in range(len(row_oxy)):
            oxy_worksheet.write(line_oxy + 1, single_oxy + 1, row_oxy[single_oxy])

    for line_deoxy, row_deoxy in enumerate(deoxy):
        for single_deoxy in range(len(row_deoxy)):
            deoxy_worksheet.write(line_deoxy + 1, single_deoxy + 1, row_deoxy[single_deoxy])

    data_oxy.close()
    data_deoxy.close()

    head_oxy = nirx_output.nirx_data['avg_oxy']
    head_deoxy = nirx_output.nirx_data['avg_deoxy']
    head_oxy_std = nirx_output.nirx_data['avg_oxy_std']
    head_deoxy_std = nirx_output.nirx_data['avg_deoxy_std']
    head_oxy_con = nirx_output.nirx_data['all_trials_oxy_continuous']
    head_deoxy_con = nirx_output.nirx_data['all_trials_deoxy_continuous']
    oxy_Hb = nirx_output.nirx_data['oxy_Hb']
    deoxy_Hb = nirx_output.nirx_data['deoxy_Hb']
    fs = int(nirx_output.properties['fs'])

    # save data necessary for grand average analysis to npz file
    np.savez(os.path.join(data.analysis_path, data.file_name + '_for_GA'), head_oxy=head_oxy, head_deoxy=head_deoxy,
             head_oxy_std=head_oxy_std, head_deoxy_std=head_deoxy_std, head_oxy_con=head_oxy_con,
             head_deoxy_con=head_deoxy_con, oxy_Hb=oxy_Hb, deoxy_Hb=deoxy_Hb, fs=fs
             )

    fname_props = os.path.join(data.analysis_path, data.file_name + '_Settings.json')
    fname_nirx = os.path.join(data.analysis_path, data.file_name + '_NIRx.pickle')

    # write final settings to json file
    open_file = open(fname_props, "w")
    json.dump(props, open_file, indent=3)
    open_file.close()

    # save nirx_output object to pickle file
    with open(fname_nirx, 'wb') as f:
        pickle.dump(nirx_output, f)

    text.append('Write Output Files successful')
    return text