#!/usr/bin/env python
#
#   This script search for files with certain pattern in its name, and
#   rename it based on the flags users provide.
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
import argparse

version = "20191024"

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
This script walks through all files in a directory tree recursively, searches
for patterns in file name, rename the files based on the flags that user
provide. Keep in mind that :
(1) Files will be renamed only if -inplace is given.
(2) Use -maxdepth to specify maximum depth to search for files.
    -maxdepth 1 means only search for current directory

Default pattern = all files
Default inplace = False (files will not be renamed)
Default replace = ' /_'
    (replace space with _)
Default maxdepth = 1

example:
python3 rename.py "cpp" -re ' /_' -lower -maxdepth 2
python3 rename.py "pptx" -inplace -re '__/_' -upper
""", formatter_class=argparse.RawTextHelpFormatter)


# positional argument:
# '+' == 1 or more.  '*' == 0 or more.  '?' == 0 or 1.
parser.add_argument(
    "pattern",
    nargs='*',
    default="*",
    help="""Search for this pattern.""")

# optional argument
parser.add_argument("-v",
                    "--version",
                    action="version",
                    version="version: " + str(version))

parser.add_argument("-maxdepth",
                    "--maxdepth",
                    help="maximum depth to search for files")

# if -inplace is specified, True will be assigned to it (store_true)
parser.add_argument("-inplace",
                    "--inplace",
                    action='store_true',
                    help="if you want to rename files")

# if -verbose is specified, True will be assigned to it (store_true)
parser.add_argument("-vervose",
                    "--verbose",
                    action='store_true',
                    help="if you want to show detail process info.")

# if -lower is specified, True will be assigned to it (store_true)
parser.add_argument("-lower",
                    "--lower",
                    action='store_true',
                    help="use lower case")

# if -upper is specified, True will be assigned to it (store_true)
parser.add_argument("-upper",
                    "--upper",
                    action='store_true',
                    help="use upper case")

# replace S (=source) with T (=target)
parser.add_argument("-re", "--replace", help="replace 'S' with 'T': -re 'S/T'")

# get arguments from command line
args = parser.parse_args()
patternList = args.pattern

if args.maxdepth:
    maxdepth = int(args.maxdepth)
    print("maxdepth = {}\n".format(maxdepth))
else:
    maxdepth = 1
    print("maxdepth is not specified, set maxdepth = {}\n".format(maxdepth))

if args.inplace:
    inplace = args.inplace
    print("inplace = {}".format(inplace))
    print('Files will be renamed.\n')
else:
    inplace = False
    print("-inplace is not specified, set -inplace = {}".format(inplace))
    print('Files will not be renamed.\n')

if args.verbose:
    verbose = args.verbose
    print("verbose = {}".format(verbose))
    print('Detail info will be shown.\n')
else:
    verbose = False
    print("-verbose is not specified, set -verbose = {}".format(verbose))
    print('Detail info will not be shown.\n')

if args.lower:
    lower = args.lower
    print("lower = {}, use lower case.\n".format(lower))
else:
    lower = False
    print("-lower is not specified, set -lower = {}\n".format(lower))

if args.upper:
    upper = args.upper
    print("upper = {}, use upper case.\n".format(upper))
else:
    upper = False
    print("-upper is not specified, set -upper = {}\n".format(upper))

# replace'S' with 'T' (S = source, T = target)
default_re = True
if args.replace:
    try:
        arg = args.replace.split('/')
        S = arg[0]
        T = arg[1]
        print("-re arguments: {}".format(arg))
        print("Replace '{}' with '{}'".format(S, T))
        default_re = False
    except:
        print("Fails to parse -re arguments, use default arguments")
else:
    print("-re arguments are not specified, use default arguments.")

if default_re:
    S = ' '
    T = '_'
    print("Replace '{}' with '{}'".format(S, T))

inDIR = os.getcwd()     # get current path
fileDict = dict()       # using pathfile as key to store file name
pathDict = dict()       # using pathfile as key to store path
pathfileList = []       # path+file name, store as pathfile
varList = []            # varilable in nam list file
varDict = {}

print("")
print("Search for files with this pattern:")
for pattern in patternList:
    print(pattern)

print("Searching begins ! \n")
# walk through directory
#
# dName = current directory,
# sdName = list of sub-directory in current directory,
# fList = list of files in current directoruy
# os.path.join = join one or more path components intelligently.
print("Initial directory: \n{}".format(inDIR))
inDIR_depth = inDIR.count(os.path.sep)
# when maxdepth = 1, only search for current directory
max_depth = inDIR_depth + maxdepth - 1
print('Depth of initial path: {}'.format(inDIR_depth))
print('Max. depth for searching: {} \n'.format(max_depth))

for (dName, sdName, fList) in os.walk(inDIR):
    if verbose:
        print('')
        print("Current directory: \n{}".format(dName))
    dName_depth = dName.count(os.path.sep)
    if verbose:
        print('Depth of current path: {}'.format(dName_depth))
    if dName_depth > max_depth:
        if verbose:
            print("Current depth {} > max. depth {}".format(dName_depth,
                                                            max_depth))
            print("Skip the directory")
        continue
    if verbose:
        print("Sub-directory:\n{}".format(str(sdName)[1:-1] or None))
        print("check files in directory {}".format(dName))

    for pattern in patternList:
        for fileName in fList:
            if verbose:
                print("pattern, filename = ", pattern, fileName)
            if (fnmatch.fnmatch(fileName, pattern)) or (pattern in fileName):
                # print("match!")
                pathfile = os.path.join(dName, fileName)
                pathfileList.append(pathfile)   # path + filename
                pathDict[pathfile] = dName      # path
                fileDict[pathfile] = fileName   # filename

print('')
print("Files that match pattern:")
for f in pathfileList:
    print(f)
print("")

num_of_file = 0
num_of_rename = 0
for pathfile in pathfileList:
    num_of_file = num_of_file + 1
    path = pathDict[pathfile]
    filename = fileDict[pathfile]
    spList = []   # a list contains species

    old_name = filename
    new_name = old_name

    # change to lower or upper cases
    if lower and upper:
        print('-lower and -upper cannot be set to True at the same time.')
        print('Set both to False.\n')
        lower = False
        upper = False
    if lower:
        new_name = new_name.lower()
    if upper:
        new_name = new_name.upper()

    # repalce characters
    new_name = new_name.replace(S, T)

    # only display message if new_name != old_name
    if new_name == old_name:
        continue

    old_pathfile = pathfile
    new_pathfile = pathfile.replace(old_name, new_name)

    if not inplace:
        print('Candidates to be renamed: ')
        print('Source file: {}'.format(old_pathfile))
        print('Target file: {}'.format(new_pathfile))
    else:
        print('Rename file...')
        print('Source file: {}'.format(old_pathfile))
        print('Target file: {}'.format(new_pathfile))
        os.rename(old_pathfile, new_pathfile)

    num_of_rename = num_of_rename + 1

print('')
print("{} files will be/have been renamed.".format(num_of_rename))
print("Done with rename process.\n")
