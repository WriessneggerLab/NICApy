import os
from PyQt5 import QtCore as qtc
import os.path


def create_eval_path(self, data, props):
    '''
    Creates analysis folder in selected analysis path
    @param self:
    @param data: Singleton object including parameters like analysis_path_main etc.
    @param props: dict object including all defined settings
    @return: data: Singleton object including file related parameters with added analysis_path, file_name
    '''
    # self is the self
    nr_xdf = len(data.xdf['selected_xdf_files'])  # returns length of list
    filename_xdf = []
    if nr_xdf == 1:
        filename_xdf.append(os.path.join(data.xdf['path'], data.xdf['selected_xdf_files'][0]))
    else:
        for i in range(len(data.xdf['selected_xdf_files'])):
            filename_xdf.append(os.path.join(data.xdf['path'], data.xdf['selected_xdf_files'][i]))
        del i
    # until now, do it only for one xdf file
    file_path = os.path.join(data.analysis_path_main, 'Analysis')
    file_name = os.path.splitext(os.path.basename(os.path.normpath(filename_xdf[0])))[0]
    xdf_path = data.xdf['path']
    task = props['task_name']
    condition = props['chosen_condition']
    folder_name = os.path.basename(os.path.normpath(xdf_path))
    folder_name = folder_name + '/' + file_name
    file_name = file_name + '_' + task + '_' + condition
    analysis_path = os.path.join(file_path, folder_name, condition)
    try:
        if not os.path.exists(analysis_path):
            os.makedirs(analysis_path)
            data.add(analysis_path=analysis_path)
            data.add(file_name=file_name)
            return data
        else:
            raise Exception('Analysis Path already exists.')
    except Exception:
        raise
        #error = str(error)
        #self.returnflag = True
        #self.submit_error.emit(error)
        #print(error)