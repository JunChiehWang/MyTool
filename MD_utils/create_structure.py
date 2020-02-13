"""A python3 script to generate coordinates and species for MD model."""

import argparse
import os
import datetime
import numpy as np

# import my modules
# used before python 3.6:
# from MD_utils import io_utils
# from MD_utils import str_utils
# used after python 3.6:
# https://stackoverflow.com/q/42263962/10764631
__path__=[os.path.dirname(os.path.abspath(__file__))]
import io_utils
import str_utils

version = '20200213'


def getArgs(argv=None):
    """Get arguments from command line."""
    # parser:
    # The The default help formatter re-wraps lines to fit your terminal
    # (it looks at the COLUMNS environment variable to determine the output
    # width, defaulting to 80 characters total).
    # Use the RawTextHelpFormatter class instead to indicate that you already
    # wrapped the lines .
    # RawTextHelpFormatter maintains whitespace for all sorts of help text,
    # including argument descriptions.
    # parser = argparse.ArgumentParser()
    #
    # Using the same option multiple times in Python's argparse:
    # https://stackoverflow.com/q/36166225/10764631
    #
    parser = argparse.ArgumentParser(
        description="""
    This script generates coordinates of atoms for MD simulations.  It goes
    through all -c commands to create particles and go through -d commands
    to delete atoms.

    -c (--create) = create a structure. Several structures can be created using
        -c command in the same order.  The size of box in x, y direction
        depends on the first structure created with -c command.

        str: structure, available options are:
            si_001, sio2_beta_Cristobalite(or sio2_beta), 
            c_diamond,
        la: lattice constant for this structure (in Angstrum).
            Sometimes it might be possible to slightly tweak the lattice
            constant to match xc and yc at interface between structures.
            recommand:
                si_001: 5.431
                sio2_beta: 7.126
                c_diamond: 3.57
        xc: number of unit cell in x
        yc: number of unit cell in y
        zc: number of unit cell in z
            (xc, yc, zc will be converted to an integer)
        zs: starting position of this structure (in Angstrum). zs for first -c
            structure needs to be 0.0 (will be converted to 0.0)

    -d (--delete) = delete atoms inside/outside of a region. Several regions
        can be created using -d command in the same order.
        User need to create a container (con) and only particles in the
        container will be considered to be deleted.

        con: [xlo,xhi,ylo,yhi,zlo,zhi] (no space in [...])
        reg: region to be considered, available regions are:
             box, cylinder, sphere
        par: parameters for region (no space in [...])
        in: =1, particles inside the region and in container will be removed.
            =0,           outside               in

        zhi -------------------------  container
            |         _              |
            |        | | region      |
            |        |_|             |
            |                        |
        zlo -------------------------
            xlo                     xhi

    -o (--output_file) = output file
    (1) if filename extension = lammpstrj (LAMMPS dump file), coordinates will
        be in lammpstrj format.
        (currently no comment lines are allowed in this .lammpstrj format)
        default =./structure_date.lammpstrj

        example:

        ITEM: TIMESTEP
        7000
        ITEM: NUMBER OF ATOMS
        1000
        ITEM: BOX BOUNDS pp pp ff
        0.0000000000000000e+00 2.1719999999999999e+01
        0.0000000000000000e+00 2.7149999999999999e+01
        0.0000000000000000e+00 5.4299999999999997e+01
        ITEM: ATOMS id type x y z
        1 Si 0 0 0
        5 Si 1.36786 1.38317 1.31655
        9 Ar 5.43 0 0
        .
        ..
        ...

        Note that after the file has been generated, the species need to be
        converted to number so that LAMMPS can parse it. For example, we can
        use sed to replace Si with 1, O with 2
        (have a space next to species, so do "s/ Si /1/g" instead of
                                             "s/Si/1/g" )
        sed -e "s/ Si /1/g" -i file.lammpstrj
        sed -e "s/ O /2/g" -i file.lammpstrj

    (2) if filename extension = xyz, coordinates will be in xyz format.

        example:

        1000
        Atoms. Timestep: 0
        Si 0 0 0
        Si 1.3575 1.3575 1.3575
        Si 5.43 0 0
        Si 6.7875 1.3575 1.3575
        Si 10.86 0 0
        .
        ..
        ...

    example:
    python3 ./create_structure.py -c str=si_001 la=5.43 xc=4 yc=5 zc=6  zs=0
    python3 ./create_structure.py -c str=si_001 la=5.43 xc=4 yc=5 zc=6  zs=0.0
                                  -o 20190730_si_001_4_5_6_v01.xyz


    """, formatter_class=argparse.RawTextHelpFormatter)

    #
    # positional argument
    #

    #
    # optional argument
    #
    parser.add_argument(
            "-v", "--version", action="version",
            version="version: " + str(version))

    # arguments to create structures
    parser.add_argument(
            "-c", "--create", action='append',
            nargs='+',
            help="""
            -c
            str=structure
            la=lattice_constant in Angstrum
            xc(number of cell in x, integer)=..
            yc(number of cell in y, integer)=..
            zc(number of cell in z, integer)=..
            zs(starting position (in Angstrum) of this structure in z)=..
            """)
    create_arg_set = set(['str', 'la', 'xc', 'yc', 'zc', 'zs'])

    # arguments to delete atoms
    parser.add_argument(
            "-d", "--delete", action='append',
            nargs='+',
            help="""
            -d
            con=[xlo,xhi,ylo,yhi,zlo,zhi]
            reg=regin to be considered
            par=parameters for region
            in=0 or 1
            """)
    delete_arg_set = set(['con','reg','par','in'])

    # arguments to output file
    parser.add_argument("-o", "--output_file", help="output file")
    ext_set = set(['xyz', 'lammpstrj'])

    args = parser.parse_args()

    # current directory
    # current_dir = os.getcwd()

#
    # parse the information for creating structures, and pass it to a
    # multi-dimensional dictionary
    if args.create:
        create = args.create
        num_create = len(create)  # number of structures are given
        create_dict = {}
        print('\ninformation of {} structures are given:'.format(num_create))
        for indx_create, each_create in enumerate(create, 1):
            print('{}: {}'.format(indx_create, each_create))
            for indx_argu, each_argu in enumerate(each_create, 1):
                try:
                    if each_argu.find('=') > -1:
                        var = each_argu.split('=')[0]
                        value = each_argu.split('=')[1]
                    else:
                        print('cannot find "=" in {}'.format(each_argu))
                        exit()
                except (OSError, IOError, IndexError) as e:
                    print(e.message, e.args)
                    print('Invalid format, use -h for help.')
                if (var not in create_arg_set):
                    print('invalid argument "{}" for -c'.format(var))
                    print('only use valid argument for -c: ', create_arg_set)
                    exit()
                create_dict[(indx_create, var)] = value
    else:
        print('no -c is given, use -h to get help.')
        exit()
#
    # parse the information for deleting particles, and pass it to a
    # multi-dimensional dictionary
    if args.delete:
        delete = args.delete
        num_delete = len(delete)  # number of structures are given
        delete_dict = {}
        print('\ninformation of {} delete regions are given:'.format(num_delete))
        for indx_delete, each_delete in enumerate(delete, 1):
            print('{}: {}'.format(indx_delete, each_delete))
            for indx_argu, each_argu in enumerate(each_delete, 1):
                try:
                    if each_argu.find('=') > -1:
                        var = each_argu.split('=')[0]
                        value = each_argu.split('=')[1]
                    else:
                        print('cannot find "=" in {}'.format(each_argu))
                        exit()
                except (OSError, IOError, IndexError) as e:
                    print(e.message, e.args)
                    print('Invalid format, use -h for help.')
                if (var not in delete_arg_set):
                    print('invalid argument "{}" for -d'.format(var))
                    print('only use valid argument for -d: ', delete_arg_set)
                    exit()
                delete_dict[(indx_create, var)] = value
    else:
        print('\nno -d is given.')
        #exit()
#
    # parse the information for creating output files
    # use filename extension to determine which format will be output
    if args.output_file:
        output_file = str(args.output_file)
        print('\noutput_file: {}'.format(output_file))
        try:
            ext = output_file.split('.')[1]
        except (IndexError) as e:
            print('error : ', e.args)
            print('filename extension is not specified, use -h for help.')
            exit()
        if ext.lower() not in ext_set:
            print('Invalid filename extension for {}'.format(output_file))
            print('Only {} are available'.format(ext_set))
            exit()
        print('output to {} format'.format(ext))
    else:
        date = datetime.datetime.now()
        date = '{}{}{}'.format(date.year, date.month, date.day)
        output_file = 'structure_{}.lammpstrj'.format(date)
        print('\noutput_file is not specified from command-line')
        print('set output_file to : {}'.format(output_file))


    arg_pack = [num_create, create_arg_set, create_dict, output_file]
    #return num_create, create_arg_set, create_dict, output_file
    return arg_pack


###############################################################################
#def create_structure(num_create, create_arg_set, create_dict, output_file):
def create_structure(arg_pack):
    [num_create, create_arg_set, create_dict, output_file] = arg_pack
    # current directory
    # current_dir = os.getcwd()

    # check if output_file exist, and get it's extension
    ext = output_file.split('.')[1].lower()
    output_file_path = os.path.realpath(output_file)
    if not os.path.isfile(output_file_path):
        print('\ncreate output_file: {}'.format(output_file_path))
    else:
        print('\noutput_file exist: {}'.format(output_file_path))
        overwrite = input('overwrite or append the file ? (y or n) ')
        overwrite = overwrite.strip().lower()
        if overwrite == 'y':
            print('overwrite it !')
        elif overwrite == 'n':
            print('not overwrite it, script exits!')
            exit()
        else:
            print('invalid input, only y or n are available')
            exit()

    # print('')
    # print(num_create)
    # print(create_arg_set)
    # print(create_dict)
    # print(output_file)

    # create empty list for atom_id, atom_type, x, y, z
    atom_id = []
    atom_type = []
    x = []
    y = []
    z = []
    Ncount = 0

    # create atoms
    for indx_str in np.arange(1, num_create+1):

        # get info of structure
        try:
            structure = create_dict[indx_str, 'str'].lower()
            lattice = float(create_dict[indx_str, 'la'])
            num_x_cell = int(float(create_dict[indx_str, 'xc']))
            num_y_cell = int(float(create_dict[indx_str, 'yc']))
            num_z_cell = int(float(create_dict[indx_str, 'zc']))
            z_start = float(create_dict[indx_str, 'zs'])
        except (ValueError) as e:
            print('ValueError! Invalid structure info (-c) is given!')
            print(e)
            exit()

        # lower and upper bound of this structure
        if indx_str == 1 and z_start != 0.0:
            print('')
            print('z_start for first structure needs to be 0.0')
            print('set z_start ({}) to 0.0'.format(z_start))
            z_start = 0.0
        x_lo = 0.0
        y_lo = 0.0
        z_lo = z_start
        x_hi = num_x_cell * lattice
        y_hi = num_y_cell * lattice
        z_hi = z_lo + num_z_cell * lattice
        xyz_bound = [x_lo, x_hi, y_lo, y_hi, z_lo, z_hi]

        # get size of box in x, y dimension based on the first structure
        if indx_str == 1:
            x_box_min = 0.0
            x_box_max = x_hi
            y_box_min = 0.0
            y_box_max = y_hi
            z_box_min = z_lo
        else:
            if x_lo < x_box_min:
                print('x_lo ({}) < x_box_min ({})'.format(x_lo, x_box_min))
                exit()
            if y_lo < y_box_min:
                print('y_lo ({}) < y_box_min ({})'.format(y_lo, y_box_min))
                exit()
            if z_lo < z_box_min:
                print('z_lo ({}) < z_box_min ({})'.format(z_lo, z_box_min))
                exit()
            if x_hi > x_box_max:
                print('x_hi ({}) > x_box_max ({})'.format(x_hi, x_box_max))
                exit()
            if y_hi > y_box_max:
                print('y_hi ({}) > y_box_max ({})'.format(y_hi, y_box_max))
                exit()

        print('')
        print('information used for creating structure:')
        print('(number of cells will be converted to an integer)')
        print('structure  : {}'.format(structure))
        print('lattice    : {}'.format(lattice))
        print('num_x_cell : {}'.format(num_x_cell))
        print('num_y_cell : {}'.format(num_y_cell))
        print('num_z_cell : {}'.format(num_z_cell))
        print('boundary in each dimension:')
        print('x_lo       : {}'.format(x_lo))
        print('x_hi       : {}'.format(x_hi))
        print('y_lo       : {}'.format(y_lo))
        print('y_hi       : {}'.format(y_hi))
        print('z_lo       : {}'.format(z_lo))
        print('z_hi       : {}'.format(z_hi))

        # build atoms
        if ((structure == 'si_001') or 
            (structure == 'c_diamond')):
            print('start building {} structure...'.format(structure))
            tmp_id, tmp_type, tmp_x, tmp_y, tmp_z = str_utils.si_001(
                    num_x_cell,
                    num_y_cell,
                    num_z_cell,
                    xyz_bound,
                    lattice=lattice)

            # increment of atom_id if there are more than 1 structure
            tmp_id = np.array(tmp_id) + Ncount

            # accumulate total number of atoms
            Ncount = Ncount + len(tmp_id)

            atom_id = np.append(atom_id, tmp_id)
            atom_type = np.append(atom_type, tmp_type)
            x = np.append(x, tmp_x)
            y = np.append(y, tmp_y)
            z = np.append(z, tmp_z)

        elif ((structure == 'sio2_beta') or
              (structure == 'sio2_beta_Cristobalite')):

            print('start building {} structure...'.format(structure))

            tmp_id, tmp_type, tmp_x, tmp_y, tmp_z =                           \
                str_utils.sio2_beta_Cristobalite(num_x_cell,
                                                 num_y_cell,
                                                 num_z_cell,
                                                 xyz_bound,
                                                 lattice=lattice)

            # increment of atom_id if there are more than 1 structure
            tmp_id = np.array(tmp_id) + Ncount

            # accumulate total number of atoms
            Ncount = Ncount + len(tmp_id)

            atom_id = np.append(atom_id, tmp_id)
            atom_type = np.append(atom_type, tmp_type)
            x = np.append(x, tmp_x)
            y = np.append(y, tmp_y)
            z = np.append(z, tmp_z)
        else:
            print('Invalid structure {}, use -h for help'.format(structure))
            exit()

    # atom_id needs to be integers
    atom_id = atom_id.astype(int)

    # remove particles if it is not inside of region
    print(atom_id.shape)

    # box
    #region = [18, 68, 18, 68, 10000]
    # cylinder
    #region = ['z', 20, 30, 0, 1000, 20]
    #region = ['x', 20, 30, 20, 1000, 10]
    #region = ['y', 30, 20, 1000, 10]
    # sphere
    region = [-40, -50, -60, 10]
    mask = np.ones(len(atom_id), dtype=bool)
    for indx, aid in enumerate(atom_id):
        xtmp = x[indx]
        ytmp = y[indx]
        ztmp = z[indx]
        coor = [xtmp, ytmp, ztmp]

        # if str_utils.inside_box(coor, region):
        # if str_utils.inside_cylinder(coor, region):
        # if not str_utils.inside_cylinder(coor, region):
        if str_utils.inside_sphere(coor, region):
            mask[indx] = False
    x = x[mask]
    y = y[mask]
    z = z[mask]
    atom_id = atom_id[mask]
    atom_type = atom_type[mask]
    print(atom_id.shape)

    #
    z_box_max = np.max(z)
    box = np.array([
        x_box_min, x_box_max,
        y_box_min, y_box_max,
        z_box_min, z_box_max
        ])

    # write coordinate of atom
    # status = 'w' : write
    #          'a' : append
    if ext == 'lammpstrj':
        io_utils.write_lammpstrj(output_file,
                                 box,
                                 atom_id,
                                 atom_type,
                                 x, y, z,
                                 timestep=0,
                                 status='w')
    elif ext == 'xyz':
        io_utils.write_xyz(output_file,
                           atom_id,
                           atom_type,
                           x, y, z,
                           timestep=0,
                           status='w')
    else:
        print('Unknow file extension!')

    print('')
    print('Min/Max of particle coordinates:')
    print('x min       : {}'.format(np.min(x)))
    print('x max       : {}'.format(np.max(x)))
    print('y min       : {}'.format(np.min(y)))
    print('y max       : {}'.format(np.max(y)))
    print('z min       : {}'.format(np.min(z)))
    print('z max       : {}'.format(np.max(z)))
    print('Challenge accomplished !!')


    return


###############################################################################
#
###############################################################################
def main():

    #num_create, create_arg_set, create_dict, output_file = getArgs()
    arg_pack = getArgs()
    #create_structure(num_create, create_arg_set, create_dict, output_file)
    create_structure(arg_pack)


###############################################################################
#
###############################################################################
if __name__ == '__main__':
    main()
