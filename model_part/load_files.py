import re as re
from configparser import RawConfigParser
import os
import pyxdf
import numpy as np
from model_part.calcHRlin import EHK_calcHRlin
from data_sharing_objects.datadict_class import data_dict

def load_files(data, props):
    '''
    load hdr and xdf files of selected data files
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @param props: dict object including all defined settings
    @return: NIRx: object of class data_dict including the loaded hdr and xdf data of the selected measurement
             text: list including prints displayed to self.output_gb in build_gui()
    uses the method to load xdf data used by Chadwick Boulay in
    https://github.com/xdf-modules/pyxdf/blob/d642dbf86f17b8dd94cce56ff339dd57e6d3774a/example/example.py
    '''
    text = []
    files = dict()
    nirx = dict()
    hdr = dict()

    # Available Data Streams
    hdr['Bool'] = dict()
    hdr['Bool']['BP'] = False
    hdr['Bool']['NIRS'] = False
    hdr['Bool']['Marker'] = False
    hdr['Bool']['gUSBamp'] = False
    hdr['Bool']['paradigm'] = False


    def _open(file):
        return open(file, 'r', encoding='latin-1')

    version = 'NIRScout'
    nr_trials = props['nr_trials']
    filename_hdr = os.path.join(data.hdr['path'], data.hdr['name'])

    nr_xdf = len(data.xdf['selected_xdf_files'])  # returns length of list
    filename_xdf = []
    if nr_xdf == 1:
        filename_xdf.append(os.path.join(data.xdf['path'], data.xdf['selected_xdf_files'][0]))
    else:
        for i in range(len(data.xdf['selected_xdf_files'])):
            filename_xdf.append(os.path.join(data.xdf['path'], data.xdf['selected_xdf_files'][i]))
        del i
    # until now, do it only for one xdf file
    for j in range(len(filename_xdf)):

        k = 0
        print('Loading... %s' % filename_hdr)  # needs to be shown in output text box and saved to txt file
        text.append('Loading... %s' % filename_hdr)

        startpoint = []
        with _open(filename_hdr) as f:
            hdr_str = f.read()

        for indx, char in enumerate(hdr_str):
            if char == '#':
                startpoint.append(indx)

        hdr_if_other_version = hdr_str
        hdr_if_other_version = hdr_if_other_version.splitlines()  # for future use
        # do the next whole procedure for reading out the values between #  # (table format of NIRStar) to put them
        # into a string to make it readable for ConfigParser. They will then be reformatted into a np.array when needed
        gains_extracted = hdr_str[startpoint[0] + 2:startpoint[1]]
        events_extracted = hdr_str[startpoint[2] + 2:startpoint[3]]
        sd_mask_extracted = hdr_str[startpoint[4] + 2:startpoint[5]]

        gains_formatted = re.sub(r"\D", ',', gains_extracted)
        events_formatted = re.sub(r"\D", ',', events_extracted)
        sd_mask_formatted = re.sub(r"\D", ',', sd_mask_extracted)
        del gains_extracted, events_extracted, sd_mask_extracted

        hdr_list = list(hdr_str)
        if True:  # do in reverse order, otherwise you need to keep track of the indices, because they then change
            hdr_list[startpoint[4] + 1:startpoint[5]] = sd_mask_formatted
            hdr_list[startpoint[2] + 1:startpoint[3]] = events_formatted
            hdr_list[startpoint[0] + 1:startpoint[1]] = gains_formatted
        del sd_mask_formatted, events_formatted, gains_formatted
        hdr_str = ''.join(hdr_list)
        hdr_str = hdr_str.replace('#', '')
        # procedure ends here

        hdr_rawcnfg = RawConfigParser()
        hdr_rawcnfg.read_string(hdr_str)

        if version == 'NIRScout':
            # [GeneralInfo]
            file_name = hdr_rawcnfg['GeneralInfo']['FileName'].strip('"')
            date = hdr_rawcnfg['GeneralInfo']['Date'].strip('"')
            time = hdr_rawcnfg['GeneralInfo']['Time'].strip('"')
            nirstar_version = hdr_rawcnfg['GeneralInfo']['NIRStar'].strip('"')
            # [ImagingParameters]
            sources = int(hdr_rawcnfg['ImagingParameters']['Sources'])
            detectors = int(hdr_rawcnfg['ImagingParameters']['Detectors'])
            wavelengths = hdr_rawcnfg['ImagingParameters']['Wavelengths']  # wird im neuen header anders abgespeichert

            # wavelengths = 2  # hdr['ImagingParameters']['Wavelengths'] wird im neuen header anders abgespeichert
            trig_ins = int(hdr_rawcnfg['ImagingParameters']['TrigIns'])
            trig_outs = int(hdr_rawcnfg['ImagingParameters']['TrigOuts'])
            an_ins = int(hdr_rawcnfg['ImagingParameters']['AnIns'])
            sampling_rate = float(hdr_rawcnfg['ImagingParameters']['SamplingRate'])
            # [Paradigm]
            stimulus_type = hdr_rawcnfg['Paradigm']['StimulusType'].strip('"')
            # [ExperimentNotes]
            notes = hdr_rawcnfg['ExperimentNotes']['Notes'].strip('"')
            # [GainSettings]
            gains_str = hdr_rawcnfg['GainSettings']['Gains'].strip('"')
            gains = np.fromstring(gains_str, dtype=int, sep=',').reshape(sources, detectors)
            del gains_str
            # [Mask]
            sd_mask_str = hdr_rawcnfg['DataStructure']['S-D-Mask'].strip('"')
            sd_mask = np.fromstring(sd_mask_str, dtype=int, sep=',').reshape(sources, detectors)
            del sd_mask_str

            print('HDR read out successful')
            text.append('HDR read out successful')
        else:
            # read out file if not NIRScout version, with hdr_if_other_version
            pass

        hdr.setdefault('Filename', []).append(file_name)
        hdr.setdefault('Date', []).append(date)
        hdr.setdefault('Time', []).append(time)
        del file_name, date, time
        hdr.setdefault('NIRStar Version', []).append(nirstar_version)
        hdr.setdefault('Sources', []).append(sources)
        hdr.setdefault('Detectors', []).append(detectors)
        hdr.setdefault('Wavelengths', []).append(wavelengths)
        hdr.setdefault('Trig Ins', []).append(trig_ins)
        hdr.setdefault('Trig Outs', []).append(trig_outs)
        hdr.setdefault('An Ins', []).append(an_ins)
        hdr.setdefault('Sampling Rate', []).append(sampling_rate)
        del sampling_rate, an_ins, trig_outs, trig_ins, wavelengths
        hdr.setdefault('Stymulus Type', []).append(stimulus_type)
        del stimulus_type
        hdr.setdefault('Notes', []).append(notes)
        hdr.setdefault('Gains', []).append(gains)
        hdr.setdefault('SD Mask', []).append(sd_mask)
        del notes, gains, sd_mask
        NIRx = data_dict()
        NIRx.add(hdr=hdr)
        print('hdr dict got all necessary values')
        text.append('hdr dict got all necessary values')
        ### load xdf files
        print('Loading... %s' % filename_xdf[j])
        text.append('Loading... %s' % filename_xdf[j])
        streams, fileheader = pyxdf.load_xdf(filename_xdf[j])
        print("Found {} streams:".format(len(streams)))
        text.append("Found {} streams:".format(len(streams)))
        for ix, stream in enumerate(streams):
            print("Stream {}: {} - type {} - uid {} - shape {} at {} Hz (effective {} Hz)".format(
                ix + 1, stream['info']['name'][0],
                stream['info']['type'][0],
                stream['info']['uid'][0],
                (int(stream['info']['channel_count'][0]), len(stream['time_stamps'])),
                stream['info']['nominal_srate'][0],
                stream['info']['effective_srate'])
            )
            text.append("Stream {}: {} - type {} - uid {} - shape {} at {} Hz (effective {} Hz)".format(
                ix + 1, stream['info']['name'][0],
                stream['info']['type'][0],
                stream['info']['uid'][0],
                (int(stream['info']['channel_count'][0]), len(stream['time_stamps'])),
                stream['info']['nominal_srate'][0],
                stream['info']['effective_srate']))
            if any(stream['time_stamps']):
                print("\tDuration: {} s".format(stream['time_stamps'][-1] - stream['time_stamps'][0]))
                text.append("\tDuration: {} s".format(stream['time_stamps'][-1] - stream['time_stamps'][0]))
        print("Done.")
        text.append("Done.")
        nirstar = streams[0]
        print(streams[0]['info']['name'][0])
        text.append(streams[0]['info']['name'][0])

        for l in streams:  # the search algorithm is done in this way, because the order of the streams is not clarified and unique
            if l['info']['name'][0] == 'NIRStar':
                nirx = l
                hdr['Bool']['NIRS'] = True

                # how many channels are used within the mask
                channels = len(nirx['info']['desc'][0]['channels'][0]['channel']) - 3
                txt = '%s found in XDF. Channels: %s' % (nirx['info']['source_id'][0], str(channels))
                print(txt)
                text.append(txt)

                continue

            elif l['info']['name'][0] == 'CNAP-BP':
                cnap = l
                hdr['Bool']['BP'] = True
                txt = '%s found in XDF.' % cnap['info']['source_id'][0]
                print(txt)
                text.append(txt)
                continue

            elif l['info']['name'][0] == 'g.USBamp-1':
                gusbamp = l
                hdr['Bool']['gUSBamp'] = True
                txt = '%s found in XDF.' % gusbamp['info']['source_id'][0]
                print(txt)
                text.append(txt)
                continue

            elif l['info']['name'][0] == 'g.USBamp-2':
                gusbamp = l
                hdr['Bool']['gUSBamp'] = True
                txt = '%s found in XDF.' % gusbamp['info']['source_id'][0]
                print(txt)
                text.append(txt)
                continue

            elif l['info']['name'][0] == 'paradigm':
                hdr['Bool']['paradigm'] = True
                marker_nirx = l
                txt = '%s found in XDF.' % marker_nirx['info']['source_id'][0]
                print(txt)
                text.append(txt)
                if hdr['Bool']['Marker']:
                    txt = 'NIRS-Marker will be overwritten by paradigm-Marker!'
                    print(txt)
                    text.append(txt)
                hdr['Bool']['Marker'] = True

                # remove all markers without information / not sure if !=0 or is not None, read docs for that
                markers_class = np.asarray(marker_nirx['time_series'][marker_nirx['time_series'] != 0])
                markers_time = np.asarray(marker_nirx['time_stamps'][marker_nirx['time_stamps'] != 0])
                # Get time series from run when it is active, start/stop
                # trigger=1
                #print(markers_time[0])
                #text.append(markers_time[0])
                run_start_stop = np.array([markers_time[0], markers_time[-1]])
                #print(run_start_stop)
                #text.append(run_start_stop)
                continue
        del l

        if hdr['Bool']['NIRS']:  # nirx:  # crop NIRS data, values inside run
            crop = np.array(
                np.logical_and(run_start_stop[0] <= nirx['time_stamps'], nirx['time_stamps'] <= run_start_stop[1]))
            nirx['time_stamps'] = nirx['time_stamps'][crop]
            nirx['time_series'] = nirx['time_series'][crop, :]

        # cnap is not used anymore, but this would be the loading
        if hdr['Bool']['BP']:  # cnap:  # crop cnap data, values inside run
            crop = np.array(
                np.logical_and(run_start_stop[0] <= cnap['time_stamps'], cnap['time_stamps'] <= run_start_stop[1]))
            cnap['time_stamps'] = cnap['time_stamps'][crop]
            cnap['time_series'] = cnap['time_series'][crop, :]
            cnap_bp = np.asarray(cnap['time_stamps'])
            cnap_bp = np.reshape(cnap_bp, (cnap_bp.shape[0], 1))  # reshaping for getting the dimensions
            cnap_time = np.asarray(
                cnap['time_series'])  # TODO: maybe check again for data types, float, double ect. (if it doesn't work)

        if hdr['Bool']['gUSBamp']:  # gusbamp:  # crop gusbamp, values inside run
            crop = np.array(
                np.logical_and(run_start_stop[0] <= gusbamp['time_stamps'], gusbamp['time_stamps'] <= run_start_stop[1]))
            gusbamp['time_stamps'] = gusbamp['time_stamps'][crop]
            gusbamp['time_series'] = gusbamp['time_series'][crop, :]
            gUSBamp_resp = np.asarray(gusbamp['time_series'][:, 4])
            # gUSBamp_resp = np.reshape(gUSBamp_resp, (gUSBamp_resp.shape[0], 1))
            gUSBamp_ecg = np.asarray(gusbamp['time_series'][:, 0])  # 1. Spalte * (-1)
            # gUSBamp_ecg = np.reshape(gUSBamp_ecg, (gUSBamp_ecg.shape[0], 1))
            gUSBamp_time = np.asarray(gusbamp['time_stamps'])
            gUSBamp_time = np.reshape(gUSBamp_time, (gUSBamp_time.shape[0], 1))

        del crop

        #############################
        ### sum all up
        #############################
        # Read wavelengths into temporary variables
        wl1_signal = nirx['time_series'][:, 0:channels]
        wl2_signal = nirx['time_series'][:, channels:2 * channels]
        nirx_time = nirx['time_stamps']
        del detectors, sources, channels
        #print(nirx['time_series'][:][nirx['time_series'][:] <= 1])
        #text.append(nirx['time_series'][:][nirx['time_series'][:] <= 1])
        #print(len(nirx['time_series'][:][nirx['time_series'][:] <= 1]))
        #text.append(len(nirx['time_series'][:][nirx['time_series'][:] <= 1]))

        # Markers
        hdr['markers'] = dict()
        hdr['markers'].update(
            {'time': markers_time})  # sollte eigentlich nicht im main gebraucht werden. (siehe NICA, Matlab)
        hdr['markers'].update({'class': markers_class})
        hdr['markers'].update({'frame': 'markers_time'})  # is this one even needed?, would be length(wl760_signla)

        wl760_signal = wl1_signal
        wl850_signal = wl2_signal

        NIRx_time = nirx_time

    # leave it out in the meantime
    del j, markers_class, markers_time
    # print(gusbamp['info']['effective_srate'])
    NIRx.add(nirx_data=dict())
    NIRx.add(time=dict())

    if gUSBamp_time.size:
        NIRx.nirx_data['Respiration'] = gUSBamp_resp
        try:
            NIRx.nirx_data['Heart Rate'] = EHK_calcHRlin(gUSBamp_ecg, round(gusbamp['info']['effective_srate']), props, data, txt=text)
        except:
            print('Could not calculate Heart-Rate signal')
            text.append('Could not calculate Heart-Rate signal')
        NIRx.nirx_data['ECG'] = gUSBamp_ecg
        NIRx.time['gUSBamp'] = gUSBamp_time
        NIRx.hdr['gUSBamp_sampling_rate'] = round(gusbamp['info']['effective_srate'])

    NIRx.nirx_data['wl760_signal'] = wl760_signal
    NIRx.nirx_data['wl850_signal'] = wl850_signal
    NIRx.time['NIRS'] = NIRx_time

    return NIRx, text