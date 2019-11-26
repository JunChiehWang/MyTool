#!/dat/usr/e121341/anaconda3/bin/python3

import argparse
import shutil
import os
import re
import datetime

version = '20190613'


##############################################################################
def getArgs(argv=None):

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
    This script generates a tecplot layout file which read all crtrs 1d files
    and show them in 1 layout so it's easier to compare with.

    -tp  = file of template to start with.
           default =
           '~/bin/JunChieh_Wang/tecplot/
           crtrs_1d_all_in_1_template_20190501.lay'
    -in  = input files
    -out = output layout
           default = ./crtrs_1d_datetime.plt.dat.lay'

    example:
    python3 crtrs_1d_all_in_1.py -in ./*25*/1d.plt.dat -out ./25mt_1d.plt.dat
    python3 crtrs_1d_all_in_1.py -in ./*25*/crtrs_1d.plt.dat -tp ./template.lay

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
    parser.add_argument("-tp", "--template", help="template layout file")
    parser.add_argument(
            "-in", "--input_file", nargs='*',
            help="input files to be plotted")
    parser.add_argument("-out", "--output_layout", help="output layout")

    args = parser.parse_args()

    # current directory
    # current_dir = os.getcwd()

#
    if args.template:
        template = str(args.template)
        print('\ntemplate file from: {}'.format(template))
    else:
        template = '~/bin/JunChieh_Wang/tecplot/' +                           \
                'crtrs_1d_all_in_1_template_20190501.lay'
        print('\ntemplate file is not specified from command-line')
        print('set template to : {}'.format(template))
#
    if args.input_file:
        input_file = args.input_file
        print('\ninput files to be included:')
        for inf in input_file:
            print(inf)
    else:
        print("\ninput files are not specified, script exits!")
        exit()
#
    if args.output_layout:
        output_layout = str(args.output_layout)
        print('\noutput_layout: {}'.format(output_layout))
    else:
        # date and time
        date = datetime.datetime.now()
        date = '{}{}{}'.format(date.year, date.month, date.day)
        output_layout = './crtrs_1d_{}.plt.dat.lay'.format(date)
        print('\noutput_layout is not specified from command-line')
        print('set output_layout to : {}'.format(output_layout))

    return template, input_file, output_layout


###############################################################################
def crtrs_1d_all_in_1(template, input_file, output_layout):

    # current directory
    current_dir = os.getcwd()

    # check if output_layout exist
    output_layout_path = os.path.realpath(output_layout)
    if not os.path.isfile(output_layout_path):
        print('\ncreate output_layout: {}'.format(output_layout_path))
    else:
        print('\noutput_layout exist: {}'.format(output_layout_path))
        overwrite = input('overwrite the file ? (yes or no) ')
        overwrite = overwrite.strip().lower()
        if overwrite == 'yes':
            print('overwrite it !')
        elif overwrite == 'no':
            print('not overwrite it, script exits!')
            exit()

    # check if template exist
    # ref: os.path.abspath, os.path.realpath, os.path.expanduser
    # https://stackoverflow.com/q/37863476/10764631
    template_path = os.path.realpath(os.path.expanduser(template))
    if not os.path.isfile(template_path):
        print('\ntemplate file not exists: {}'.format(template_path))
        print('\nexit!')
        exit()
    else:
        print('\ntemplate exists: {}'.format(template_path))
        print('\ncopy template layout over.')
        shutil.copy(template_path, output_layout)

    # files, variables and frame information to be included in layout file
    file_var = ''
    frame_setting = ''
    rename_dataset_zone = ''
    for count, f in enumerate(input_file, 1):

        # file to be included
        file_name = f.split('./')[1]
        file_path = os.path.realpath(file_name)
        if os.path.isfile(file_path):
            print('\nworking on file {}'.format(file_path))
        else:
            print('\nfile not found {}'.format(file_path))

        file_var = file_var + '\n' +                                          \
            '$!VarSet |LFDSFN{}| = \'\"{}\"\''.format(count, file_name)

        # empty variables is ok, tecplot will read variables from file
        file_var = file_var + '\n' + '$!VarSet |LFDSVL{}| = \'\''.format(count)

        # frame information
        if count > 1:
            frame = """
            $!READDATASET  '|LFDSFN{}|'
              INITIALPLOTTYPE = XYLINE
              INCLUDETEXT = NO
              INCLUDEGEOM = NO
              READDATAOPTION = APPEND
              RESETSTYLE = NO
              ASSIGNSTRANDIDS = YES
              VARLOADMODE = BYNAME
              VARNAMELIST = '|LFDSVL{}|'
            $!REMOVEVAR |LFDSVL{}|
            $!REMOVEVAR |LFDSFN{}|""".format(count, count, count, count)
            frame_setting = frame_setting + '\n' + frame

        # rename data set zone to file name
        dataset_zone = """
        $!RenameDataSetZone
          Zone = {}
          Name = '{}'""".format(count, file_name)
        rename_dataset_zone = rename_dataset_zone + dataset_zone

    # print(file_var)
    # print(frame_setting)
    # print(rename_dataset_zone)

    # read file and replace string in template
    with open(output_layout) as f:
        s = f.read()
    with open(output_layout, 'w') as f:
        old = '_replace_with_files_and_empty_variables_'
        new = file_var
        s = re.sub(old, new, s)

        old = '_replace_with_frame_setting_'
        new = frame_setting
        s = re.sub(old, new, s)

        old = '_replace_with_rename_dataset_zone_'
        new = rename_dataset_zone
        s = re.sub(old, new, s)

        f.write(s)
        f.close()

    return


###############################################################################
#
###############################################################################
def main():

    template, input_file, output_layout = getArgs()
    crtrs_1d_all_in_1(
            template=template,
            input_file=input_file,
            output_layout=output_layout)


###############################################################################
#
###############################################################################
if __name__ == '__main__':
    main()
