"""Utilities related to structure."""

import numpy as np


# ref:
#
# lattice constant:
# https://physics.nist.gov/cgi-bin/cuu/Value?asil
#
def si_001(num_x_cell,
           num_y_cell,
           num_z_cell,
           xyz_bound,
           lattice=5.431):
    """Generate coordinate of si 001 structure.

    # Arguments
        lattice: lattice constant of this structure, default = 5.431 A
        num_x_cell: number of unit cell in x
        num_y_cell: number of unit cell in y
        num_z_cell: number of unit cell in z
        xyz_bound:[x_lo, x_hi, y_lo, y_hi, z_lo, z_hi] of this structure

    # Return
        array of
        x : coordinate in x direction
        y :               y
        z :               z
        atom_id : atom id of each atom
        atom_type : type of each atom

    # Example

    # Date
        20190821
    """
    # warning if lattice constant is different from default value
    lattice_default = 5.431
    if abs(lattice - lattice_default) > 1.e-6:
        print('Warning:')
        print('Different lattice constant {} from default {} for si_001.'.
              format(lattice, lattice_default))

    # lower and upper bound of this structure
    x_lo = xyz_bound[0]
    x_hi = xyz_bound[1]
    y_lo = xyz_bound[2]
    y_hi = xyz_bound[3]
    z_lo = xyz_bound[4]
    z_hi = xyz_bound[5]

    atom_id = []
    atom_type = []
    x = []
    y = []
    z = []
    Ncount = 0

    for k in np.arange(num_z_cell):  # z direction
        for m in [1, 2, 3, 4]:
            for j in np.arange(num_y_cell):  # y direction
                for i in np.arange(num_x_cell):  # x direction
                    # print(k,m,j,i)

                    if m == 1:
                        if z_lo + k * lattice > z_hi:
                            continue

                        # atom in the origin of cubic unit cell
                        x.append(x_lo + i*lattice)
                        y.append(y_lo + j*lattice)
                        z.append(z_lo + k*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                        # atom on face
                        x.append(x_lo + (i+0.5)*lattice)
                        y.append(y_lo + (j+0.5)*lattice)
                        z.append(z_lo + k*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                    if m == 2:
                        if z_lo + (k+0.25)*lattice > z_hi:
                            continue

                        # atom in cell
                        x.append(x_lo + (i+0.25)*lattice)
                        y.append(y_lo + (j+0.25)*lattice)
                        z.append(z_lo + (k+0.25)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                        x.append(x_lo + (i+0.75)*lattice)
                        y.append(y_lo + (j+0.75)*lattice)
                        z.append(z_lo + (k+0.25)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                    if m == 3:
                        if z_lo + (k+0.5)*lattice > z_hi:
                            continue

                        # atom on face
                        x.append(x_lo + (i+0.5)*lattice)
                        y.append(y_lo + j*lattice)
                        z.append(z_lo + (k+0.5)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                        x.append(x_lo + i*lattice)
                        y.append(y_lo + (j+0.5)*lattice)
                        z.append(z_lo + (k+0.5)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                    if m == 4:
                        if z_lo + (k+0.75)*lattice > z_hi:
                            continue

                        # atom in cell
                        x.append(x_lo + (i+0.75)*lattice)
                        y.append(y_lo + (j+0.25)*lattice)
                        z.append(z_lo + (k+0.75)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                        x.append(x_lo + (i+0.25)*lattice)
                        y.append(y_lo + (j+0.75)*lattice)
                        z.append(z_lo + (k+0.75)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

    return atom_id, atom_type, x, y, z


#
# generate coordinates of Beta Cristobalite SiO2
#
# ref:
# https://homepage.univie.ac.at/michael.leitner/lattice/struk/c9.html
# http://phycomp.technion.ac.il/~ira/types.html#SiO2
#
# lattice constant:
# https://staff.aist.go.jp/nomura-k/common/struc-coord/b-Cristobalite-c.htm
#
def sio2_beta_Cristobalite(num_x_cell,
                           num_y_cell,
                           num_z_cell,
                           xyz_bound,
                           lattice=7.126):
    """Generate Beta (high temperature) Cristobalite SiO2 structure.

    The silicon atoms occupy the positions they take in the diamond (A4)
    structure, while the oxygen atoms form bridges between them.

    # Arguments
        lattice: lattice constant of this structure, default = 7.126 A
        num_x_cell: number of unit cell in x
        num_y_cell: number of unit cell in y
        num_z_cell: number of unit cell in z
        xyz_bound:[x_lo, x_hi, y_lo, y_hi, z_lo, z_hi] of this structure

    # Return
        array of
        x : coordinate in x direction
        y :               y
        z :               z
        atom_id : atom id of each atom
        atom_type : type of each atom

    # Example

    # Date
        20190821
    """
    # warning if lattice constant is different from default value
    lattice_default = 7.126
    if abs(lattice - lattice_default) > 1.e-6:
        print('Warning:')
        print('Different lattice constant {} from default {} for sio2_beta.'.
              format(lattice, lattice_default))

    # lower and upper bound of this structure
    x_lo = xyz_bound[0]
    x_hi = xyz_bound[1]
    y_lo = xyz_bound[2]
    y_hi = xyz_bound[3]
    z_lo = xyz_bound[4]
    z_hi = xyz_bound[5]

    atom_id = []
    atom_type = []
    x = []
    y = []
    z = []
    Ncount = 0

    for k in np.arange(num_z_cell):  # z direction
        for m in [1, 2, 3, 4, 5, 6, 7, 8]:
            for j in np.arange(num_y_cell):  # y direction
                for i in np.arange(num_x_cell):  # x direction
                    # print(k,m,j,i)

                    if m == 1:
                        if z_lo + k*lattice > z_hi:
                            continue

                        # Si atom in the origin of cubic unit cell
                        x.append(x_lo + i*lattice)
                        y.append(y_lo + j*lattice)
                        z.append(z_lo + k*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                        # Si atom on face
                        x.append(x_lo + (i+0.5)*lattice)
                        y.append(y_lo + (j+0.5)*lattice)
                        z.append(z_lo + k*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                    if m == 2:
                        if z_lo + (k+0.125)*lattice > z_hi:
                            continue

                        # O atoms
                        x.append(x_lo + (i+0.125)*lattice)
                        y.append(y_lo + (j+0.125)*lattice)
                        z.append(z_lo + (k+0.125)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                        x.append(x_lo + (i+0.375)*lattice)
                        y.append(y_lo + (j+0.375)*lattice)
                        z.append(z_lo + (k+0.125)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                        x.append(x_lo + (i+0.625)*lattice)
                        y.append(y_lo + (j+0.625)*lattice)
                        z.append(z_lo + (k+0.125)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                        x.append(x_lo + (i+0.875)*lattice)
                        y.append(y_lo + (j+0.875)*lattice)
                        z.append(z_lo + (k+0.125)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                    if m == 3:
                        if z_lo + (k+0.25)*lattice > z_hi:
                            continue

                        # Si atom in cell
                        x.append(x_lo + (i+0.25)*lattice)
                        y.append(y_lo + (j+0.25)*lattice)
                        z.append(z_lo + (k+0.25)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                        x.append(x_lo + (i+0.75)*lattice)
                        y.append(y_lo + (j+0.75)*lattice)
                        z.append(z_lo + (k+0.25)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                    if m == 4:
                        if z_lo + (k+0.375)*lattice > z_hi:
                            continue

                        # O atoms
                        x.append(x_lo + (i+0.125)*lattice)
                        y.append(y_lo + (j+0.375)*lattice)
                        z.append(z_lo + (k+0.375)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                        x.append(x_lo + (i+0.375)*lattice)
                        y.append(y_lo + (j+0.125)*lattice)
                        z.append(z_lo + (k+0.375)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                        x.append(x_lo + (i+0.625)*lattice)
                        y.append(y_lo + (j+0.875)*lattice)
                        z.append(z_lo + (k+0.375)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                        x.append(x_lo + (i+0.875)*lattice)
                        y.append(y_lo + (j+0.625)*lattice)
                        z.append(z_lo + (k+0.375)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                    if m == 5:
                        if z_lo + (k+0.5)*lattice > z_hi:
                            continue

                        # Si atom on face
                        x.append(x_lo + (i+0.5)*lattice)
                        y.append(y_lo + j*lattice)
                        z.append(z_lo + (k+0.5)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                        x.append(x_lo + i*lattice)
                        y.append(y_lo + (j+0.5)*lattice)
                        z.append(z_lo + (k+0.5)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                    if m == 6:
                        if z_lo + (k+0.625)*lattice > z_hi:
                            continue

                        # O atoms
                        x.append(x_lo + (i+0.625)*lattice)
                        y.append(y_lo + (j+0.125)*lattice)
                        z.append(z_lo + (k+0.625)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                        x.append(x_lo + (i+0.875)*lattice)
                        y.append(y_lo + (j+0.375)*lattice)
                        z.append(z_lo + (k+0.625)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                        x.append(x_lo + (i+0.125)*lattice)
                        y.append(y_lo + (j+0.625)*lattice)
                        z.append(z_lo + (k+0.625)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                        x.append(x_lo + (i+0.375)*lattice)
                        y.append(y_lo + (j+0.875)*lattice)
                        z.append(z_lo + (k+0.625)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                    if m == 7:
                        if z_lo + (k+0.75)*lattice > z_hi:
                            continue

                        # atom in cell
                        x.append(x_lo + (i+0.75)*lattice)
                        y.append(y_lo + (j+0.25)*lattice)
                        z.append(z_lo + (k+0.75)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                        x.append(x_lo + (i+0.25)*lattice)
                        y.append(y_lo + (j+0.75)*lattice)
                        z.append(z_lo + (k+0.75)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('Si')

                    if m == 8:
                        if z_lo + (k+0.875)*lattice > z_hi:
                            continue

                        # O atoms
                        x.append(x_lo + (i+0.125)*lattice)
                        y.append(y_lo + (j+0.875)*lattice)
                        z.append(z_lo + (k+0.875)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                        x.append(x_lo + (i+0.375)*lattice)
                        y.append(y_lo + (j+0.625)*lattice)
                        z.append(z_lo + (k+0.875)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                        x.append(x_lo + (i+0.625)*lattice)
                        y.append(y_lo + (j+0.375)*lattice)
                        z.append(z_lo + (k+0.875)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

                        x.append(x_lo + (i+0.875)*lattice)
                        y.append(y_lo + (j+0.125)*lattice)
                        z.append(z_lo + (k+0.875)*lattice)
                        Ncount = Ncount + 1
                        atom_id.append(Ncount)
                        atom_type.append('O')

    return atom_id, atom_type, x, y, z


def inside_box(coord, region):
    """Check if the point is inside of a box region.

    # Arguments
        coord: an array with coordinates to be checked = [x, y, z]
        region: an array with property of this region. For box, it's
        [x_lo, x_hi, y_lo, y_hi, z_lo, z_hi]

    # Return
        True: if the coordinates is inside of box
        False:                   is not

    # Example

    # Date
        20190819
    """
    try:
        x = coord[0]
        y = coord[1]
        z = coord[2]

        x_lo = region[0]
        x_hi = region[1]
        y_lo = region[2]
        y_hi = region[3]
        z_lo = region[4]
        z_hi = region[5]
    except (IndexError) as e:
        print('IndexError in inside_box() !!')
        print(e)
        print('your coord: {}'.format(coord))
        print('your region: {}'.format(region))
        print('coord shoudl be: [x, y, z]')
        print('region should be: [x_lo, x_hi, y_lo, y_hi, z_lo, z_hi]')
        exit()

    if (x >= x_lo) & (x <= x_hi) & \
       (y >= y_lo) & (y <= y_hi) & \
       (z >= z_lo) & (z <= z_hi):
        return True
    else:
        return False


def inside_cylinder(coord, region):
    """Check if the point is inside of a cylinder region.

    # Arguments
        coord: an array with coordinates to be checked = [x, y, z]
        region: an array with property of this region. For cylinder, it's
        [axis, x_lo, y_lo, z_lo, height, radius], where
        axis : lower case string, x or y or z
        x_lo, y_lo, z_lo: lowest point of cylinder along axis
        height: height of the cylinder
        radius: radius of the cylinder

    # Return
        True: if the coordinates is inside of box
        False:                   is not

    # Example

    # Date
        20190820
    """
    try:
        x = coord[0]
        y = coord[1]
        z = coord[2]

        axis = region[0].lower().strip()
        x_lo = region[1]
        y_lo = region[2]
        z_lo = region[3]
        height = region[4]
        radius = region[5]
    except (IndexError) as e:
        print('IndexError in inside_cylinder() !!')
        print(e)
        print('your coord: {}'.format(coord))
        print('your region: {}'.format(region))
        print('coord shoudl be: [x, y, z]')
        print('region should be: [axis, x_lo, y_lo, z_lo, height, radius]')
        exit()

    if (axis == 'z'):
        if (z < z_lo) | (z > z_lo + height):
            return False
        d2 = (x - x_lo)**2 + (y - y_lo)**2
        if (d2 <= radius**2):
            return True
        else:
            return False

    elif (axis == 'x'):
        if (x < x_lo) | (x > x_lo + height):
            return False
        d2 = (y - y_lo)**2 + (z - z_lo)**2
        if (d2 <= radius**2):
            return True
        else:
            return False

    elif (axis == 'y'):
        if (y < y_lo) | (y > y_lo + height):
            return False
        d2 = (x - x_lo)**2 + (z - z_lo)**2
        if (d2 <= radius**2):
            return True
        else:
            return False

    else:
        print('Unknow axis: {}, script exits'.format(axis))
        exit()


def inside_sphere(coord, region):
    """Check if the point is inside of a spherical region.

    # Arguments
        coord: an array with coordinates to be checked = [x, y, z]
        region: an array with property of this region. For sphere, it's
        [cx, cy, cz, radius], where
        cx, cy, cz: center of sphere
        radius: radius of the cylinder

    # Return
        True: if the coordinates is inside of box
        False:                   is not

    # Example

    # Date
        20190820
    """
    try:
        x = coord[0]
        y = coord[1]
        z = coord[2]

        cx = region[0]
        cy = region[1]
        cz = region[2]
        radius = region[3]
    except (IndexError) as e:
        print('IndexError in inside_sphere() !!')
        print(e)
        print('your coord: {}'.format(coord))
        print('your region: {}'.format(region))
        print('coord shoudl be: [x, y, z]')
        print('region should be: [cx, cy, cz, radius]')
        exit()

    d2 = (x - cx)**2 + (y - cy)**2 + (z - cz)**2
    if (d2 <= radius**2):
        return True
    else:
        return False
