#!/bin/bash
#
#  this script convert *.plt (ASCII) to .plt.dat (binary)
#
#   ref: getopts
#     https://stackoverflow.com/questions/18003370/script-parameters-in-bash
#     https://stackoverflow.com/questions/7069682/how-to-get-arguments-with
#             -flags-in-bash-script
#   ref: shift $(($OPTIND - 1))
#     https://unix.stackexchange.com/questions/214141/explain-the-shell-command
#             -shift-optind-1/214151
#   ref: use a wildcard with a getopts in a bash script
#     https://stackoverflow.com/questions/9024119/how-do-i-use-a-wildcard-with
#             -a-getopts-in-a-bash-script
#   ref: function
#     https://ryanstutorials.net/bash-scripting-tutorial/bash-functions.php
#

#
#   function to output usage and version
#
function usage_version {
 echo "Example: Duplicate all tecplot plt files in directory JJ and preplot it."
 echo "         The output file will be xxx.plt.dat"
 echo "         Use -d to duplicate the plt files and preplot it"
 echo "         Use -o to preplot the original plt files"
 echo "preplot_plt.sh -d ./JJ/*.plt"
 echo "  -v: version and help"
 echo "  -h: version and help"
 echo "  -d: preplot duplicated plt file (use this option when the case is still running)"
 echo "  -o: preplot original plt file (use this option when the case is done)"
 echo "version : 20190427"
}

#
#   arguments from command line
#
all_argum=$@
#echo "all arguments: $all_argum"
num_argum=$#
#echo "number of arguments: $num_argum"

#
#   default parameters
#
if_cp="-d"
if_err="true"

while getopts ":vhdo" OPT;
do
   case $OPT in
      v ) echo "-v: version" ;;
      h ) echo "-h: help" ;;
      d ) echo "-d: preplot duplicated plt file"
          if_cp="-d"
	      if_err="false" ;;
      o ) echo "-o: preplot original plt file"
          if_cp="-o"
	      if_err="false" ;;
      ? ) echo 'Bad options used.' ;;
    esac
done

shift $(($OPTIND - 1))
fileList=("$@")

#
#   function to preplot the plt files
#
if [ $if_err == "false" ]; then
  if [ ${#fileList[@]} -eq 0 ]; then
    echo "What files are you preploting ?"
    if_err="true"
  else
    for file in "${fileList[@]}"; do
      if [ ! -f $file ]; then
        echo "File not found:" $file
	continue
      fi
      if [ $if_cp == '-d' ]; then
        echo "Preplot the duplicated file: $file"
        cp $file $file.tmp
        preplot $file.tmp $file.dat
        rm $file.tmp
      elif [ $if_cp == '-o' ]; then
        echo "Preplot the original file: $file"
        preplot $file $file.dat
      fi
    done
    exit 0
  fi
fi
#
#   output usage and version if the argument format is incorrect
#
if [ "$if_err" == "true" ]; then
  usage_version
  exit 1
fi
