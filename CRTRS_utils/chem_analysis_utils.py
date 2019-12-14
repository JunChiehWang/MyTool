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

        # get number of timestamp
        NumTimeStamp = 0
        for line in self.content_list:
            if line.startswith('Time ='):
                NumTimeStamp = NumTimeStamp + 1
        self.NumTimeStamp = NumTimeStamp

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

        assert len(time) == self.NumTimeStamp

        return time

    def get_te(self, dtype='float32'):
        """get electron temperature (eV) of each output.

        format of electron temperature in chem_analysis.dat :
        ..
        ...
        ****************************************

        Electron Temperature =   6.14 eV

        ****************************************
        ..

        # Argument
            dtype: dtype of numpy array
               'str', 'float32', 'float64',....

        # Exampe
            chem = chem_analysis_utils.chem_analysis(chem_analysis_path)
            time = chem.get_te()

        # Return
            numpy array of electron temperature (eV)

        # Date
            20191212
        """

        te = [line.split()[3] for line in self.content_list
              if line.startswith('Electron Temperature = ')]
        te = np.array(te, dtype=dtype)

        assert len(te) == self.NumTimeStamp

        return te

    def get_species(self, dtype='float32'):
        """get species and its density(m-3) and fraction(%)

        format of species in chem_analysis.dat :

        ****************************************
        Species Densities & Concentrations
        ****************************************
        Species    Density (m-3)   Density (%)
        E            3.61137E+14    0.00007484
        O2^          1.78914E+14    0.00003708
        ...
        ********************

        # Argument
            dtype: dtype of numpy array
               'str', 'float32', 'float64',....

        # Exampe
            chem = chem_analysis_utils.chem_analysis(chem_analysis_path)
            den, fra = chem.get_species()

        # Return
            dictionary of density(m-3) and fraction(%)
            Ex:
            den['E'] = array([3.61137E+14,...], dtype = float32)
            fra['E'] = array([0.00007484,...], dtype = float32)

        # Date
            20191213
        """
        if_find_data = False
        spe = []  # species
        den = []  # density
        fra = []  # fraction
        den_dict = {}
        fra_dict = {}
        for line in self.content_list:
            # find data block
            if line.startswith('Species    Density (m-3)   Density (%)'):
                if_find_data = True
                continue

            # end of data block, append data from list to dictionary
            if if_find_data and line.startswith('*****'):
                # check if dictionary empty, len gives number of keys (species)
                # if empty(no species), create empty list for each species
                if len(den_dict) == 0:
                    for sp in spe:
                        den_dict[sp] = []
                        fra_dict[sp] = []

                for ind, sp in enumerate(spe):
                    den_dict[sp].append(den[ind])
                    fra_dict[sp].append(fra[ind])

                if_find_data = False
                spe.clear()
                den.clear()
                fra.clear()
                continue

            # parse data
            if if_find_data:
                line = line.split()
                spe.append(line[0])
                den.append(line[1])
                fra.append(line[2])
                continue

        # convert type
        for key in den_dict:
            den_dict[key] = np.array(den_dict[key], dtype=dtype)
            fra_dict[key] = np.array(fra_dict[key], dtype=dtype)
            assert len(den_dict[key]) == self.NumTimeStamp
            assert len(fra_dict[key]) == self.NumTimeStamp

        return den_dict, fra_dict
