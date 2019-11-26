"""Utilities to parse tecplt related outpul files."""

import numpy as np
# import os


def get_file_head(file_path):
    """Parse the tecplot file and get file head.

    If line.strip().split() is an list of numbers, it means that
    line contains datas, the script terminates there.

    # Argument
        file_path: file (with full path) to be parsed

    # Exampe
        file_head_dict = parse_utils.get_file_head(crtrs_1d_plt_path)

    # Return
        it returns a dictionary with keys:
            'file_path'
            'title'
            'variables'
            'zone'
            'f'

    # Date
        20191015
    """
    filehead_dict = dict()
    filehead_dict['file_path'] = file_path
    find_variable = False
    find_zone = False
    variable_array = []

    try:
        fin = open(file_path, 'r')
        # print('Opening file {}'.format(file_path))
    except OSError:
        print('File {} cannot be opened.'.format(file_path))

    for line in fin:
        line = line.strip()

        # skip comment line
        if line.startswith('#'):
            continue

        # title
        if line.lower().startswith('title'):
            ii = line.find('=')
            filehead_dict['title'] = line[ii+1:].strip()
            continue

        # variable
        if line.lower().startswith('variables'):
            find_variable = True
            var_tmp = line.split('=')[1].split(',')
            for var in var_tmp:
                # if " is found after variables=,
                # it means there are variables we need to take into account
                if var.find('\"') != -1:
                    variable_array.append(var.strip())
            continue

        # zone
        if line.lower().startswith('zone'):
            find_variable = False
            filehead_dict['variables'] = variable_array
            find_zone = True
            filehead_dict['zone'] = line

            # f= .. seems to be different from DATAPACKING=...
            if line.lower().find('f=') != -1:
                if line.lower().find('point') != -1:
                    filehead_dict['f'] = 'point'
                elif line.lower().find('block') != -1:
                    filehead_dict['f'] = 'block'

            continue

        # variables
        if find_variable:
            var_tmp = line.split(',')
            for var in var_tmp:
                if var.find('\"') != -1:
                    variable_array.append(var.strip())
            continue

        # data
        try:
            tmp = float(line.split()[0])
            # print('find values, exit !')
            find_zone = False
            break
        except ValueError:
            if find_zone:
                filehead_dict['zone'] += line
                continue
            else:
                print('Unknow format: {}'.format(line))
                exit()

    fin.close()

    return filehead_dict


def get_1d_final(file_path, num, f='point'):
    """Parse 1d tecplot (crtrs_1d.plt) and get data from the bottom of file.

    # Argument
        file_path: file (with full path) to be parsed
        f: 'block' or 'point'
        num: number of data (variables) to read in

    # Exampe
        data = parse_utils.get_1d_final(crtrs_1d_plt_path, num_var, f='point')

    # Return
        numpy array contains num of data from bottom of file

    # Date
        20191015
    """
    if not isinstance(num, int):
        raise ValueError('{} is not an integer !'.format(num))

    f = f.lower().strip()
    if not (f == 'point' or f == 'block'):
        raise ValueError('Unknown format:{}'.format(f))

    try:
        with open(file_path, 'r') as content_file:
            content = content_file.read()
            # print('Opening file {}'.format(file_path))
    except OSError:
        print('File {} cannot be opened.'.format(file_path))
        exit()

    data_array = []

    if f == 'point':
        data_array = np.array([content.split()[-1*num:]], dtype=float)
        return data_array
    else:
        print('Not defined yet')
        return None


def get_fluxes(file_path, var_array, f='point'):
    """Parse the fluxes.plt tecplot file

    # Argument
        file_path: file (with full path) to be parsed
        f: 'block' or 'point'
        var_array: array of variables

    # Exampe

    # Return
        numpy array contains data of all variables from the file

    # Date
        20191016
    """
    if not isinstance(var_array, list):
        raise ValueError('{} is not an list !'.format(var_array))
    num_var = len(var_array)
    flux_dict = {var: [] for var in var_array}

    f = f.lower().strip()
    if not (f == 'point' or f == 'block'):
        raise ValueError('Unknown format:{}'.format(f))

    try:
        with open(file_path, 'r') as content_file:
            # readlines return lines of file as elements and store in list
            # if the file is too large, it might cause a problem.
            # use generator to fix it later !!
            content_list = content_file.readlines()
    except OSError:
        print('File {} cannot be opened.'.format(file_path))
        exit()

    # apply strip to element (=line in file) of list
    content_list = [line.strip() for line in content_list]

    if f == 'point':
        # find line number of "ZONE F=POINT", data begins next line
        try:
            line_zone = content_list.index("ZONE F=POINT")
        except:
            print("Cannot find 'ZONE F=POINT' in file, script exits")
            exit()

        # each group of data contains num_var data points,
        # these data points belong to position r, z
        # for example, the fluxes.plt might like this:
        #
        #   Title="Fluxes to Wafer Material"
        #   Variables= "R(m)","Z(m)",
        #             "F-E         (1/m2/s)",
        #             "F-SF4^      (1/m2/s)",
        #             "F-SF3^      (1/m2/s)",
        #   ZONE F=POINT
        #   0.00000E+00  2.54000E-02  1.54002E+19  2.57425E+17
        #   3.77816E+18
        #   6.35000E-03  2.54000E-02  1.54089E+19  2.57687E+17
        #   3.77977E+18
        #   1.27000E-02  2.54000E-02  1.54483E+19  2.58198E+17
        #   3.78017E+18
        #
        # in this case, num_var = 5 (R, Z, F-E, F-SF4^, F-SF3^), and
        # there are 3 groups (stands for 3 different R values)
        #
        num_var_read = 0
        var_array_read = []
        # data begins from element (line_zone+1) in the list
        for line in content_list[line_zone+1:]:
            line = np.array(line.strip().split(), dtype=float)
            num_var_in_line = len(line)

            if num_var_read < num_var:
                num_var_read = num_var_read + num_var_in_line
                for val in line:
                    var_array_read.append(val)
            elif num_var_read > num_var:
                print("num_var_read {} > num_var {}".format(num_var_read,
                                                            num_var))
                print("script exists.")
                exit()

            if num_var_read == num_var:
                # copy over to dictionary
                for indx, value in enumerate(var_array_read):
                    var = var_array[indx]
                    flux_dict[var].append(value)
                num_var_read = 0
                var_array_read.clear()

        return flux_dict
    else:
        print('Not defined yet')
        return None
