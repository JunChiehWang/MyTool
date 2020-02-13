"""Utilities related to disk/file I/O """

import numpy as np


def write_lammpstrj(
        output_file,
        box,
        atom_id,
        atom_type,
        x,
        y,
        z,
        timestep=0,
        status='w',
        bounds="pp pp ff"
        ):

    """output data to lammpstrj format

    # Argument
        output_file: file name of output file
        status: file status ('w', 'r', 'a')
        atom_id: id of atoms
        atom_type: type of atoms
        x: x coordinates of atoms
        y: y
        z: z
        box: an array with 6 elements, it's size of simulation box in Angstrum,
            index of array :
            0 - 5 stands for x_min, x_max, y_min, y_max, z_min, z_max
        timestep: default timestep = 0
        bounds: default bounds = 'pp pp ff'
    # Example

    # Date
        20190729
    """
    # open output_file and write header
    fout = open(output_file, status)
    fout.write('ITEM: TIMESTEP\n')
    fout.write('{}\n'.format(timestep))
    fout.write('ITEM: NUMBER OF ATOMS\n')
    fout.write('{}\n'.format(np.size(x)))
    fout.write('ITEM: BOX BOUNDS {}\n'.format(bounds))
    fout.write('{} {} \n'.format(box[0], box[1]))
    fout.write('{} {} \n'.format(box[2], box[3]))
    fout.write('{} {} \n'.format(box[4], box[5]))
    fout.write('ITEM: ATOMS id type x y z \n')

    for indx, AtomId in enumerate(atom_id):
        AtomType = atom_type[indx]
        xx = x[indx]
        yy = y[indx]
        zz = z[indx]
        line = '{}  {}  {}  {}  {} \n'.format(AtomId, AtomType, xx, yy, zz)
        fout.write(line)

    fout.close()

    return None


def write_xyz(
        output_file,
        atom_id,
        atom_type,
        x,
        y,
        z,
        timestep=0,
        status='w'
        ):

    """output data to xyz format

    # Argument
        output_file: file name of output file
        status: file status ('w', 'r', 'a')
        atom_id: id of atoms (use it as index to output)
        atom_type: type of atoms
        x: x coordinates of atoms
        y: y
        z: z
        box: an array with 6 elements, it's size of simulation box in Angstrum,
            index of array :
            0 - 5 stands for x_min, x_max, y_min, y_max, z_min, z_max
        timestep: default timestep = 0
    # Example

    # Date
        20190729
    """

    # open output_file and write header
    fout = open(output_file, status)
    fout.write('{}\n'.format(np.size(x)))
    fout.write('Atoms. Timestep: {}\n'.format(timestep))

    for indx, AtomId in enumerate(atom_id):
        AtomType = atom_type[indx]
        xx = x[indx]
        yy = y[indx]
        zz = z[indx]
        line = '{}  {}  {}  {} \n'.format(AtomType, xx, yy, zz)
        fout.write(line)

    fout.close()

    return None
