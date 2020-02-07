"""This script generate variables to be plotted in crtrs.nam."""
import argparse
import os
# used before python 3.6:
# from CRTRS_utils import dat_utils
# used after python 3.6:
# https://stackoverflow.com/q/42263962/10764631
__path__=[os.path.dirname(os.path.abspath(__file__))]
import dat_utils

version = '20200206'


##############################################################################
def getArgs(argv=None):
    """Get arguments."""
    #
    # parser:
    # The The default help formatter re-wraps lines to fit your terminal
    # (it looks at the COLUMNS environment variable to determine the output
    # width, defaulting to 80 characters total).
    # Use the RawTextHelpFormatter class instead to indicate that you already
    # wrapped the lines .
    # RawTextHelpFormatter maintains whitespace for all sorts of help text,
    # including argument descriptions.
    # parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        description="""
    This script generate variables to be plotted in crtrs.nam

    -ty = plot_type, it can be instantaneous(ins), average(ave) or all(all),
          default = all
    -sp = species (or .dat file that contains species)

    example:
    python3 crtrs_spec_report.py -ty all -sp 'Ar, Cl, Cl*, Cl^, E'
    python3 crtrs_spec_report.py -ty all -sp crtrs.dat

    """, formatter_class=argparse.RawTextHelpFormatter)

    #
    # positional argument
    #

    #
    # optional argument
    #
    parser.add_argument("-v",
                        "--version",
                        action="version",
                        version="version: " + str(version))
    parser.add_argument("-ty", "--plot_type", help="ins, ave or all")
    parser.add_argument("-sp", "--species", help="species to be plotted")

    args = parser.parse_args()
#
    if args.plot_type:
        plot_type = str(args.plot_type)
        print("\nplot_type from command-line: {}".format(plot_type))
    else:
        plot_type = 'all'
        print("\nplot_type is not specified from command-line")
        print("set plot_type: {}".format(plot_type))
#
    if args.species:
        spe = args.species
        #  species is provided directly
        if spe.find(',') != -1:
            try:
                species = spe.split(',')
                species = [sp.strip() for sp in species if len(sp.strip()) > 0]
                print("\nspecies to be plotted = {} \n".format(str(species)))
            except:
                print('cannot parse {}, script exits!'.format(spe))
                exit()
        #  a .dat file is provided
        elif spe.find('.dat') != -1:
            species = spe
            print("\nspecies will be parsed from file {} \n".format(species))
        else:
            print("cannot parse {}, script exits!".format(spe))
            exit()
    else:
        print("\nspecies are not specified, script exits!")
        exit()
#
    return species, plot_type


###############################################################################
def crtrs_spec_report(spec=None, plot_type='all'):
    """Make a list of variables to be ploted in crtrs.nam.

    # Example
        crtrs_spec_report(spec=['AR,CL'],plot_type='all')
        crtrs_spec_report(spec=aa.dat,plot_type='all')

    # Arguments
        plot_type: type of variables. It can be 'all', 'ave' or 'ins'.
            'ave' plots average variables
            'ins' plots instantaneous variables
            'all' plots 'ave' and 'ins'

        spec: a list a species string or file from which species
              will be extracted.

    # Returns
        a dictionary with keys:
            plot_list: variables to be plotted
            sp_template: species info for crtrs.nam

    # version
        20191022

    """
    if spec is None:
        print('spec is not defined.')
        exit()

    plot_type = plot_type.lower()
    if (plot_type != 'all' and plot_type != 'ins' and plot_type != 'ave'):
        print('{} is not a valid plot_type(ave, ins or all)'.format(plot_type))
        print('set plot_type to all')
        plot_type = 'all'

    # a file is provided
    if isinstance(spec, str) and spec.find('.dat') != -1:
        file_path = os.path.realpath(spec)
        # print(file_path)
        if os.path.isfile(file_path):
            print('find the file {}, start parsing.'.format(file_path))
            spec = dat_utils.dat_get_species(file_path)
            print('species :', spec)
        else:
            print('cannot find the file {}, script exits!'.format(file_path))
            exit()
    elif isinstance(spec, list):
        # if species are provided
        spec = [ii.upper() for ii in spec]

    spec.sort()

    return_dict = {}

    # prepare template info for species in nam file
    # use tab as delimiter/seperator
    sep = '\t'
    sp_template = ''
    # number of positive/negative ions species
    num_pos_ion = 0
    num_neg_ion = 0
    den_init = 1.00e-06
    for sp in spec:
        gamma = 0.0
        if sp.upper() == 'E':
            continue
        if sp.endswith('^'):
            num_pos_ion = num_pos_ion + 1
            gamma = 0.1
        if sp.endswith('-'):
            num_neg_ion = num_neg_ion + 1
        # sp_name IPR Den_Init Gamma SCCMIN(1) SCCMIN(2) SCCMIN(3)
        den_init_str = '{:.3E}'.format(den_init)
        sp_template = sp_template + sp + sep + '1' + sep + den_init_str +    \
            sep + str(gamma) + sep + "0.0" + sep + "0.0" + sep + "0.0\n"
    # Electrons species
    gamma = 0.0
    den_init = (num_pos_ion-num_neg_ion)*den_init
    den_init_str = '{:.3E}'.format(den_init)
    sp_template = sp_template + 'E' + sep + '1' + sep + den_init_str + sep + \
        str(gamma) + sep + "0.0" + sep + "0.0" + sep + "0.0\n"

    # copy species info over to dictionary
    return_dict['sp_template'] = sp_template

    # prepare variables for plotting
    pre_spec_A = ['A', 'SA', 'PA', 'FRA', 'FZA']
    pre_spec_I = ['N', 'S', 'P', 'FR', 'FZ']
    extra_A = ['POTAVE', 'SCHGAVE', 'TEAVE', 'ERAVE', 'EZAVE', 'RHOAVE']
    extra_I = ['POT', 'SCHG', 'TE', 'ER', 'EZ', 'JR', 'JZ', 'RHO', 'COLF',
               'ET_ICP-M', 'ET_ICP-P', 'PICP']
    plot_list = []
    # plot average variables
    if (plot_type == 'all' or plot_type == 'ave'):
        pre_spec = pre_spec_A
        extra = extra_A
        for ex in extra:
            # plot_list.append(ex+'AVE')
            plot_list.append(ex)
        for pr in pre_spec:
            if pr == 'PA':
                plot_list.append(pr + '-E')
            for sp in spec:
                # 'PA' only goes with charge species
                if pr == 'PA':
                    if (sp.find('^') == -1 and sp.find('-') == -1):
                        continue
                plot_list.append(pr + '-' + sp)

    # plot instantaneous variables
    if (plot_type == 'all' or plot_type == 'ins'):
        pre_spec = pre_spec_I
        extra = extra_I
        for ex in extra:
            plot_list.append(ex)
        for pr in pre_spec:
            if pr == 'P':
                plot_list.append(pr + '-E')
            for sp in spec:
                # 'P' only goes with charge species
                if pr == 'P':
                    if (sp.find('^') == -1 and sp.find('-') == -1):
                        continue
                plot_list.append(pr + '-' + sp)

    # copy over variables to be plotted to dictionary
    return_dict['plot_list'] = plot_list

    return return_dict


###############################################################################
#
###############################################################################
def main():
    """The main function."""
    species, plot_type = getArgs()
    result_dict = crtrs_spec_report(spec=species, plot_type=plot_type)
    plot_list = result_dict['plot_list']
    sp_template = result_dict['sp_template']
    print('\nplot_list : \n{}'.format(plot_list))
    print('\nsp_template : \n{}'.format(sp_template))


###############################################################################
#
###############################################################################
if __name__ == '__main__':
    main()
