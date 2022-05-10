import os
import numpy as np
import xlsxwriter
from data_sharing_objects.datadict_class import data_dict
import copy


def get_grand_average_data(data_ga, props):
    '''
    Prepares loaded data files for grand averages usage
    @param data_ga: Singleton object including parameters like analysis_path, file_name etc.
    @param props: dict object including all defined settings for grande average analysis
    @return: NIRx: NIRx object of class data_dict including the loaded hdr and xdf data of the selected measurement
             all_data: list containing a dict for each loaded file selected for grand average analysis
             props
    '''

    NIRx = data_dict()
    NIRx.add(nirx_data=dict())
    condition = props['chosen_condition']

    ga_path = os.path.join(data_ga.analysis_path_main, 'Grand Average')
    ga_path_condition = os.path.join(ga_path, condition)


    os.makedirs(ga_path_condition)
    data_ga.add(analysis_path_ga=ga_path)
    data_ga.add(analysis_path_cond=ga_path_condition)


    if props['probe_set'] == '12':
        props['probe_set_val'] = 1
    elif props['probe_set'] == '24':
        props['probe_set_val'] = 2
    elif props['probe_set'] == '38':
        props['probe_set_val'] = 3
    elif props['probe_set'] == '47':
        props['probe_set_val'] = 4
    elif props['probe_set'] == '50':
        props['probe_set_val'] = 5
    elif props['probe_set'] == 'Laboratory new':
        props['probe_set_val'] = 6
    elif props['probe_set'] == 'NIRx Sports old':
        props['probe_set_val'] = 7
    elif props['probe_set'] == 'NIRx Sports new':
        props['probe_set_val'] = 8

    file_names = data_ga.filenames_ga

    all_data = []

    for dat in file_names:
        single_data = {}
        with np.load(dat) as ga_data:
            single_data.update({'head_oxy': ga_data['head_oxy']})
            single_data.update({'head_deoxy': ga_data['head_deoxy']})
            single_data.update({'head_oxy_std': ga_data['head_oxy_std']})
            single_data.update({'head_deoxy_std': ga_data['head_deoxy_std']})
            single_data.update({'head_oxy_con': ga_data['head_oxy_con']})
            single_data.update({'head_deoxy_con': ga_data['head_deoxy_con']})
            single_data.update({'oxy_Hb': ga_data['oxy_Hb']})
            single_data.update({'deoxy_Hb': ga_data['deoxy_Hb']})
            single_data.update({'fs': ga_data['fs']})

        all_data.append(single_data)

    avg_oxy = []
    avg_deoxy = []
    avg_oxy_std = []
    avg_deoxy_std = []
    avg_oxy_con = []
    avg_deoxy_con = []

    # this could be done different, however, it is done in this way for easier debugging and for easier understanding
    # of the code for future software user. This can be changed in the future.

    for i in range(all_data[0]['head_oxy'].shape[1]):

        head_oxy_all = []
        head_deoxy_all = []
        head_oxy_std_all = []
        head_deoxy_std_all = []
        head_oxy_con_all = []
        head_deoxy_con_all = []

        for j in range(len(all_data)):
            head_oxy = all_data[j]['head_oxy'][:, i]
            head_deoxy = all_data[j]['head_deoxy'][:, i]
            head_oxy_std = all_data[j]['head_oxy_std'][:, i]
            head_deoxy_std = all_data[j]['head_deoxy_std'][:, i]
            head_oxy_con = all_data[j]['head_oxy_con'][:, i]
            head_deoxy_con = all_data[j]['head_deoxy_con'][:, i]

            head_oxy_all.append([head_oxy])
            head_deoxy_all.append([head_deoxy])
            head_oxy_std_all.append([head_oxy_std])
            head_deoxy_std_all.append([head_deoxy_std])
            head_oxy_con_all.append([head_oxy_con])
            head_deoxy_con_all.append([head_deoxy_con])

        head_oxy_all = np.asarray(head_oxy_all)
        head_deoxy_all = np.asarray(head_deoxy_all)
        head_oxy_std_all = np.asarray(head_oxy_std_all)
        head_deoxy_std_all = np.asarray(head_deoxy_std_all)
        head_oxy_con_all = np.asarray(head_oxy_con_all)
        head_deoxy_con_all = np.asarray(head_deoxy_con_all)

        avg_oxy.append(np.mean(np.reshape(head_oxy_all, (head_oxy_all.shape[0], head_oxy_all.shape[2])), axis=0))
        avg_deoxy.append(
            np.mean(np.reshape(head_deoxy_all, (head_deoxy_all.shape[0], head_deoxy_all.shape[2])), axis=0))
        avg_oxy_std.append(
            np.mean(np.reshape(head_oxy_std_all, (head_oxy_std_all.shape[0], head_oxy_std_all.shape[2])), axis=0))
        avg_deoxy_std.append(
            np.mean(np.reshape(head_deoxy_std_all, (head_deoxy_std_all.shape[0], head_deoxy_std_all.shape[2])), axis=0))
        avg_oxy_con.append(
            np.mean(np.reshape(head_oxy_con_all, (head_oxy_con_all.shape[0], head_oxy_con_all.shape[2])), axis=0))
        avg_deoxy_con.append(
            np.mean(np.reshape(head_deoxy_con_all, (head_deoxy_con_all.shape[0], head_deoxy_con_all.shape[2])), axis=0))

    data_avg_oxy = np.reshape(np.asarray(avg_oxy), (np.asarray(avg_oxy).shape[0], np.asarray(avg_oxy).shape[1])).T
    data_avg_deoxy = np.reshape(np.asarray(avg_deoxy), (np.asarray(avg_deoxy).shape[0], np.asarray(avg_deoxy).shape[1])).T
    data_avg_oxy_std = np.reshape(np.asarray(avg_oxy_std), (np.asarray(avg_oxy_std).shape[0], np.asarray(avg_oxy_std).shape[1])).T
    data_avg_deoxy_std = np.reshape(np.asarray(avg_deoxy_std), (np.asarray(avg_deoxy_std).shape[0], np.asarray(avg_deoxy_std).shape[1])).T
    data_avg_oxy_con = np.reshape(np.asarray(avg_oxy_con), (np.asarray(avg_oxy_con).shape[0], np.asarray(avg_oxy_con).shape[1])).T
    data_avg_deoxy_con = np.reshape(np.asarray(avg_deoxy_con), (np.asarray(avg_deoxy_con).shape[0], np.asarray(avg_deoxy_con).shape[1])).T

    NIRx.nirx_data['avg_oxy'] = data_avg_oxy
    NIRx.nirx_data['avg_deoxy'] = data_avg_deoxy
    NIRx.nirx_data['avg_oxy_std'] = data_avg_oxy_std
    NIRx.nirx_data['avg_deoxy_std'] = data_avg_deoxy_std
    NIRx.nirx_data['all_trials_oxy_continuous'] = data_avg_oxy_con
    NIRx.nirx_data['all_trials_deoxy_continuous'] = data_avg_deoxy_con
    fs = []
    for i in range(len(all_data)):
        fs.append(all_data[i]['fs'])  # change to without min, when fs saving works, is problem of pycharm
    NIRx.add(properties=props)
    NIRx.properties['fs'] = np.mean(np.asarray(fs))  # 4

    return NIRx, all_data, props

def grand_average_output_file(all_data, nirx_ga_output, props, data_ga):
    '''
    Generates the final grand average output file
    @param all_data: list containing a dict for each loaded file selected for grand average analysis
    @param nirx_ga_output: NIRx object of class data_dict including the loaded hdr and xdf data of the selected measurement
    @param props: dict object including all defined settings for grande average analysis
    @param data_ga: Singleton object including parameters like analysis_path, file_name etc.
    @return:
    '''
    ### grand average output file

    timing = np.asarray([-int(props['pre_task_length']),
                         int(props['task_length']) + int(props['post_task_length'])])

    timing_steps = np.round(timing[1] / 4)
    time_point_list = []
    time_point_list.append([timing[0], 0])
    time_point_list.append([0, timing_steps])
    time_point_list.append([timing_steps, timing_steps * 2])
    time_point_list.append([timing_steps * 2, timing_steps * 3])
    time_point_list.append([timing_steps * 3, timing[1]])

    ROIs_temp_list = props['grand_average_rois']
    ROIs = []
    for i in range(len(ROIs_temp_list)):
        ROIs.append({'channels': ROIs_temp_list[i]})

    vpn = []

    # for each subject
    for subject in range(len(all_data)):
        ROI = copy.deepcopy(ROIs)
        head_oxy = all_data[subject]['head_oxy']
        head_deoxy = all_data[subject]['head_deoxy']
        time_points = []
        t = np.arange(timing[0], timing[1], 1 / nirx_ga_output.properties['fs'])
        if t.shape[0] > head_oxy.shape[0]:
            t = t[0:head_oxy.shape[0]]

        # for each time point (e.g. -5 - 10, 10 - 25 etc.) in seconds
        for k in range(len(time_point_list)):
            time_point = time_point_list[k]
            # extract data for head
            mat_val_oxy = np.zeros((head_oxy.shape[1]))
            mat_val_deoxy = np.zeros((head_deoxy.shape[1]))
            if len(time_point) == 2:
                tp_idx = np.arange(np.amin(np.where(t > time_point[0])),
                                   np.amax(np.where(t < time_point[1])) + 1)  # +1 for including endpoint
            else:
                tp_idx = np.array([np.amin(np.where(t > time_point[0]))])

            # calculate the mean of Hbo for each channel for the corresponding time interval
            for ch in range(head_oxy.shape[1]):
                mat_val_oxy[ch] = np.mean(head_oxy[tp_idx, ch])
                mat_val_deoxy[ch] = np.mean(head_deoxy[tp_idx, ch])

            # exclude channels, separate properties for grand average
            exclude_channs_ga = props['excluded_channels']
            if len(exclude_channs_ga) != 0:
                mat_val_oxy[np.asarray(exclude_channs_ga) - 1] = 0
                mat_val_deoxy[np.asarray(exclude_channs_ga) - 1] = 0

            time_points.append({'oxy': mat_val_oxy, 'deoxy': mat_val_deoxy})

        # for each ROI
        for i in range(len(ROI)):
            channels = ROI[i]['channels']
            oxy = []
            deoxy = []
            for k in range(len(time_points)):
                oxy.append(np.mean(time_points[k]['oxy'][np.asarray(channels) - 1]))
                deoxy.append(np.mean(time_points[k]['deoxy'][np.asarray(channels) - 1]))

            ROI[i].update({'oxy': np.asarray(oxy), 'deoxy': np.asarray(deoxy)})

        vpn.append(ROI)




    image_class_string = props['chosen_condition']
    c = [int(props['condition_markers'][marker]) for marker in range(len(props['available_conditions'])) if
         props['available_conditions'][marker] == image_class_string]  # need to enter condition and markers for grand average
    filename_oxy = (os.path.join(data_ga.analysis_path_cond, 'Grand_Average_oxy' + 'C_' + str(c[0]) + '.xlsx'))
    filename_deoxy = (os.path.join(data_ga.analysis_path_cond, 'Grand_Average_deoxy' + 'C_' + str(c[0]) + '.xlsx'))
    data_oxy = xlsxwriter.Workbook(filename_oxy)
    oxy_worksheet = data_oxy.add_worksheet('Grand_Average_oxy_Condition_' + str(c[0]))
    data_deoxy = xlsxwriter.Workbook(filename_deoxy)
    deoxy_worksheet = data_deoxy.add_worksheet('Grand_Average_deoxy_Condition_' + str(c[0]))


    for v in range(len(vpn)):
        col = 0
        oxy_worksheet.write(v + 1, 0, 'VP' + str(v + 1))  # can be changed to 'Subject' if desired
        deoxy_worksheet.write(v + 1, 0, 'VP' + str(v + 1))
        for roi in range(len(vpn[v])):
            abc = len(vpn[v][roi]['oxy'])
            for t_point in range(len(vpn[v][roi]['oxy'])):
                if v == 0:
                    oxy_worksheet.write(v, col + 1, 'ROI' + str(roi + 1) + '_C' + str(c[0]) + '_t' + str(t_point + 1))
                    deoxy_worksheet.write(v, col + 1, 'ROI' + str(roi + 1) + '_C' + str(c[0]) + '_t' + str(t_point + 1))
                oxy_worksheet.write(v + 1, col + 1, vpn[v][roi]['oxy'][t_point])
                deoxy_worksheet.write(v + 1, col + 1, vpn[v][roi]['deoxy'][t_point])
                col += 1
    data_oxy.close()
    data_deoxy.close()