#!/usr/bin/env python
#
#   This script collect *.nam files and its variables, output to
#   nam_collector_year-month-date_hour-min-sec.csv and
#   nam_collector_diff_year-month-date_hour-min-sec.csv if -diff is specified
#
#   ref:argparse
#     https://docs.python.org/2/howto/argparse.html
#     https://stackoverflow.com/questions/29613487/multiple-lines-in-python-arigparse-help-display/29613565
#     https://stackoverflow.com/questions/43391084/argparse-default-for-positional-argument-not-working
#   ref: find files in python using find command
#     https://spectraldifferences.wordpress.com/2014/03/02/recursively-finding-files-in-python-using-the-find-command/
#   ref: pass a list to argparse
#     https://stackoverflow.com/questions/15753701/argparse-option-for-passing-a-list-as-option
#   ref: how/where to write a comments
#     https://www.digitalocean.com/community/tutorials/how-to-write-comments-in-python-3
#
#   Jerry
#
import os
import fnmatch
import datetime
import argparse
import numpy as np
import pandas as pd

version = "20190820"


# parser
#
# The The default help formatter re-wraps lines to fit your terminal
# (it looks at the COLUMNS environment variable to determine the output width,
# defaulting to 80 characters total).
# Use the RawTextHelpFormatter class instead to indicate that you already
# wrapped the lines .
# RawTextHelpFormatter maintains whitespace for all sorts of help text,
# including argument descriptions.
# parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(
    description="""
This script process all nam files in a directory tree recursively, searches for
*.nam pattern, collect nam files and variables, and output to
nam_collector_year-month-date_hour-min-sec.csv, a semicolon(;) is
used as separator. Open the file with excel and use semicolon as delimiter.
if -diff is specified, a nam_collector_diff_year-month-date_hour-min-sec.csv
file will be generated.

Default pattern = crtrs.nam
Default check_sp = 1
Default check_sub = False (only search for nam files in current folder)
Default check_diff = False (don't output difference)

example:
python3 nam_collector.py
python3 nam_collector.py crtrs.nam -sub -diff -sp 2
python3 nam_collector.py aa*.nam
python3 nam_collector.py .nam
""", formatter_class=argparse.RawTextHelpFormatter)


# positional argument:
# '+' == 1 or more.  '*' == 0 or more.  '?' == 0 or 1.
parser.add_argument(
    "pattern",
    nargs='*',
    default="crtrs.nam",
    help="""Search for this .nam pattern and compare files.""")


# optional argument
parser.add_argument("-v",
                    "--version",
                    action="version",
                    version="version: " + str(version))

parser.add_argument("-sp",
                    "--check_sp",
                    help="1: list species(default) 2: check + compare species")

# if -sub is specified, True will be assigned to it (store_true)
parser.add_argument("-sub",
                    "--check_sub",
                    action='store_true',
                    help="if you want to check nam files in sub-directories")

# if -diff is specified, True will be assigned to it (stire_true)
parser.add_argument("-diff",
                    "--check_diff",
                    action='store_true',
                    help="if you want to find the difference between nam file")


# get arguments from command line
args = parser.parse_args()
patternList = args.pattern

if args.check_sp:
    check_sp = int(args.check_sp)
    print("check_sp = {}".format(check_sp))
else:
    check_sp = 1
    print("check_sp is not specified, set check_sp = {}".format(check_sp))

if args.check_sub:
    check_sub = args.check_sub
    print("check_sub = {}".format(check_sub))
    print('search for nam files in all sub-directories')
else:
    check_sub = False
    print("check_sub is not specified, set check_sub = {}".format(check_sub))
    print('Only search for nam file in current directories')

if args.check_diff:
    check_diff = args.check_diff
    print("check_diff = {}".format(check_diff))
else:
    check_diff = False
    print("check_diff is not specified, set check_diff = " + str(check_diff))


# initialization
date_time = str(datetime.datetime.now()).split()
date = date_time[0]
time = date_time[1][:8].replace(':', '-')
inDIR = os.getcwd()     # get current path
fileDict = dict()       # using pathfile as key to store file name
pathDict = dict()       # using pathfile as key to store path
pathfileList = []       # path+file name, store as pathfile
varList = []            # varilable in nam list file
varDict = {}


print("")
print("Search for .nam file with this pattern:")
for pattern in patternList:
    print(pattern)

print("Searching begins ! \n")


# walk through directory
#
# dName = current directory,
# sdName = list of sub-directory in current directory,
# fList = list of files in current directoruy
# os.path.join = join one or more path components intelligently.
for (dName, sdName, fList) in os.walk(inDIR):

    print("Current directory: \n{}\n".format(dName))
    print("Sub-directory:\n{}\n".format(str(sdName)[1:-1] or None))
    print("check files in current directory ... \n")
    for pattern in patternList:
        for fileName in fList:
            # print("pattern, filename =", pattern, fileName)
            if (fnmatch.fnmatch(fileName, pattern)) or (pattern in fileName):
                # print("match!")
                pathfile = os.path.join(dName, fileName)
                pathfileList.append(pathfile)   # path + filename
                pathDict[pathfile] = dName      # path
                fileDict[pathfile] = fileName   # filename

    if check_sub:
        continue
    else:
        break

print("Files that match pattern:")
for f in pathfileList:
    print(f)
print("")


print("Indexing begins !")
num_of_file = 0
for pathfile in pathfileList:
    num_of_file = num_of_file + 1
    path = pathDict[pathfile]
    filename = fileDict[pathfile]
    spList = []   # a list contains species

    print('Indexing {} ...'.format(filename))

    # Open and read file
    input_file = pathfile
    try:
        fin = open(input_file)
    except (OSError, IOError) as e:
        print("File cannot be opened:", input_file)
        exit()

    switch = 0
    switch_sp = 0
    for line in fin:
        line = line.strip()

        # condiser species, it will always be on the top of .nam file
        # this code should be moved to a function later !!!
        if check_sp >= 1:
            line = line.lower()
            if ('sp_name' in line) and                                        \
               ('den_init' in line) and                                       \
               ('gamma' in line):
                switch_sp = 1
                continue
            elif (switch_sp == 1) and (line.startswith('*')):
                switch_sp = 0
                continue

            if switch_sp == 1:
                if line.startswith('!') or line.startswith('#'):
                    continue
                line = line.split()

                # species
                var = 'sp_name'
                sp = line[0].strip().upper()
                spList.append(sp)
                if var not in varList:
                    varList.append(var)
                spList.sort()
                varDict[(pathfile, var)] = str(spList)

                if check_sp != 2:
                    continue

                # IPR
                var = line[0].strip().upper() + '_ipr'
                val = line[1].strip()
                if var not in varList:
                    varList.append(var)
                varDict[(pathfile, var)] = val

                # Den_Init
                var = line[0].strip().upper() + '_den_init'
                val = line[2].strip()
                if var not in varList:
                    varList.append(var)
                varDict[(pathfile, var)] = val

                # Gamma
                var = line[0].strip().upper() + '_gamma'
                val = line[3].strip()
                if var not in varList:
                    varList.append(var)
                varDict[(pathfile, var)] = val

                # SCCMIN
                num_sccmin = len(line) - 4
                for isccm in np.arange(1, num_sccmin+1, 1, dtype=int):
                    var = line[0].strip().upper() + '_sccmin_' + str(isccm)
                    val = line[3 + isccm].strip()
                    if var not in varList:
                        varList.append(var)
                    varDict[(pathfile, var)] = val

                continue

        # consider lines in $datain blocks
        if line.startswith('$datain'):
            switch = 1
        elif line.startswith('$end'):
            switch = 0

        if switch == 0:
            continue
        elif switch == 1:
            # neglect comments and space
            if line.startswith('!') or                                        \
               line.startswith('$') or                                        \
               len(line) == 0:
                continue
            if line.find('!') > -1:
                temp = line.find('!')
                line = line[0:temp]
                line = line.strip()
            if line.find('=') > -1:
                line = line.split('=')
                var = line[0].strip().lower()
                val = line[1].strip()
            else:
                val = val + line.strip()
            if var not in varList:
                varList.append(var)
            varDict[(pathfile, var)] = val
    fin.close()

if num_of_file == 0:
    print("Find no .nam files")
    exit()

print("Done with searching/indexing \n")

# output
print('output begins ...')

# Open the output file
outfile = 'nam_collector_{}_{}.csv'.format(date, time)
print("Output to file {}\n".format(outfile))
fout = open(outfile, 'w')

# output sep for csv to recgonize it
delim = ';'
line_out = 'sep={}'.format(delim)
fout.write(line_out+'\n')

# output headline :
line_out = 'file_name' + delim
for var in varList:
    line_out = line_out + var + delim
fout.write(line_out+'\n')

# output values :
line_out = ''

# loop over files
for pathfile in pathfileList:
    val_out = ''
    line_out = pathfile + delim

    # for file 'pathfile', loop over variables in varList
    for var in varList:
        ifind_var = 0
        for (pathfile_tmp, var_tmp) in varDict:
            if ifind_var == 0 and pathfile == pathfile_tmp and var == var_tmp:
                ifind_var = 1
                val_out = val_out + varDict[(pathfile, var)] + delim
                break
        if ifind_var == 0:
            val_out = val_out + '***' + delim
    line_out = line_out + val_out + '\n'
    fout.write(line_out)

fout.close()


# find the difference between nam files
if check_diff:
    print('find the difference between nam files...')

    # Open the output_diff file
    outfile_diff = 'nam_collector_diff_{}_{}.csv'.format(date, time)

    print("Output to file {} \n".format(outfile_diff))
    fout = open(outfile_diff, 'w')

    # output sep for csv to recgonize it
    line_out = 'sep={}'.format(delim)
    fout.write(line_out+'\n')

    df = pd.read_csv(outfile, delimiter=delim, header=1, index_col=0)
    df = df.loc[:, ~df.columns.str.match('Unnamed')]
    df_diff = df
    variables = df_diff.columns
    cases = df_diff.index
    for var in variables:
        case_base = None
        var_same = True
        for case in cases:
            if case_base is None:
                case_base = case
                continue
            else:
                if df_diff.loc[case, var] != df_diff.loc[case_base, var]:
                    var_same = False
                    break
        if var_same:
            df_diff.drop(var, axis=1, inplace=True)
    df_diff.to_csv(outfile_diff, sep=delim)
    fout.close()
    print(df_diff)
