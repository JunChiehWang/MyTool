"""Utilities related to dat files. """


def dat_get_species(input_file):
    """get species from .dat file

    # Argument
        input_file: path of input .dat file

    # Example
        spec = dat_utils.dat_get_species(file_path)
        
    # Return
        a list of species

    # Date
        20191007
    """

    spe_list = []

    # Open and read file
    try:
        fin = open(input_file)
    except (OSError, IOError) as e:
        print("{} cannot be opened, script exits!".format(input_file))
        exit()

    for line in fin:
        line = line.strip()

        # ignore return species on following line
        if line.startswith('>'):
            continue

        # end of species block
        if line.startswith('*'):
            break

        spe_list.append(line.split()[0])

    spe_list.sort()
    return spe_list
