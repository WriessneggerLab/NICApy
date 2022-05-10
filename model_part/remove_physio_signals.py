from model_part.car_nirx import car_NIRx
from model_part.corr_nirx import corr_NIRx


def remove_physio(nirx_physio, props, data):
    '''
    Applies selected method for physiological artefact removal to oxy and deoxy signals. CAR or TF possible.
    @param nirx_physio: NIRx object of class data_dict including the loaded hdr and xdf data of the selected
    @param props: dict object including all defined settings
    @param data: Singleton object including parameters like analysis_path, file_name etc.
    @return: nirx_physio: NIRx object of class data_dict including the loaded hdr and xdf data of the selected
             text: list including prints displayed to self.output_gb in build_gui()
    '''
    text = []
    ### Removal of physiological signals
    oxy_signal = nirx_physio.nirx_data['Concentration']['clean']['oxy']
    deoxy_signal = nirx_physio.nirx_data['Concentration']['clean']['deoxy']
    if props['signal_analysis_method'] == 'CAR (Common Average Reference)':
        try:
            oxy_signal, deoxy_signal = car_NIRx(oxy_signal, deoxy_signal, props)
            nirx_physio.nirx_data['Concentration']['clean']['oxy'] = oxy_signal
            nirx_physio.nirx_data['Concentration']['clean']['deoxy'] = deoxy_signal
            print('Physiological Artefacts Removal successful')
            text.append('Physiological Artefacts Removal successful')
        except Exception:
            print('Could not calculate CAR signals.')
            text.append('Could not calculate CAR signals.')
            raise
    elif props['signal_analysis_method'] == 'TF (Transfer Function Models)':
        try:
            oxy_signal, deoxy_signal, NIRx, text = corr_NIRx(oxy_signal, deoxy_signal, nirx_physio, props=props,
                                                             txt=text, data=data)
            nirx_physio.nirx_data['Concentration']['clean']['oxy'] = oxy_signal
            nirx_physio.nirx_data['Concentration']['clean']['deoxy'] = deoxy_signal
            print('Physiological Artefacts Removal successful')
            text.append('Physiological Artefacts Removal successful')
        except Exception:
            print('Could not calculate TF-removed signals.')
            text.append('Could not calculate TF-removed signals.')
            raise

    return nirx_physio, text
