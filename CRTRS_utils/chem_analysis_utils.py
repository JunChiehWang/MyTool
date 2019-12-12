"""Utilities related to chem_analysis.dat files. """
import numpy as np
from platform import python_version

# print version of packages
print("Import PyPlt:")
print("python version: ", python_version())
print("numpy version: ", np.version.version)


class chem_analysis:
    """Parse chem_analysis.dat and get data.

    # Argument
        file_path: file (with full path) to be parsed

    # Exampe
        data = 

    # Return

    # Date
        20191015
    """

    def __init__(self, file_path):

        self.filename = file_path

        try:
            with open(file_path, 'r') as file:
                # store line with content in a list
                # use line[:-1] to get rid of \n in each line
                self.content_list = [line[:-1] for line in file.readlines()
                                     if line.strip()]
        except OSError:
            print('File {} cannot be opened.'.format(file_path))
            exit()

    def get_time(self, dtype='float32'):
        """get time stamp of each output.

        format of time stamp in chem_analysis.dat :
        ..
        ...
        ****************************************
        Time =     7.14286E-08 s
        ****************************************
        ..

    # Argument
        file_path: file (with full path) to be parsed
        dtype: dtype of numpy array
               'str', 'float32', 'float64',....

    # Exampe
            chem = chem_analysis_utils.chem_analysis(chem_analysis_path)
            time = chem.get_time()

    # Return
        numpy array of time stamp

    # Date
        20191212
    """

        time = [line.split()[2] for line in self.content_list
                if line.startswith('Time =')]
        time = np.array(time, dtype=dtype)
        return time
