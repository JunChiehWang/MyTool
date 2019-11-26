#!/bin/bash
#
#  this script compress *.xxx (ASCII) to *.xxx.tar.gz or
#              extract  *.xxx.tar.gz to *.xxx
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
#   ref: extract directory from a path:
#    https://stackoverflow.com/questions/6509650/extract-directory-from-path
#   ref: strip-components
#    https://serverfault.com/questions/330127/tar-remove-leading-directory-components-on-extraction
#

#
#   function to output usage and version
#
function usage_version {
 echo "Example: Use -z to compress the .xxx file to .xxx.tar.gz"
 echo "         Use -x to extract the .xxx.tar.gz to the .xxx files"
 echo "compress.sh -z ./JJ/*.plt"
 echo "compress.sh -x ./JJ/*.tar.gz"
 echo "  -v: version and help"
 echo "  -h: version and help"
 echo "  -z: compress plt file"
 echo "  -x: extract plt.tar.gz"
 echo "version : 20191021"
}

#
#   arguments from command line
#
all_argum=$@
echo "all arguments: $all_argum"
num_argum=$#
echo "number of arguments: $num_argum"

if_cp="-z"
if_err="true"

while getopts ":vhzx" OPT;
do
   case $OPT in
      v ) echo "-v: version" ;;
      h ) echo "-h: help" ;;
      z ) echo "-z: compress files"
          if_cp="-z"
	      if_err="false" ;;
      x ) echo "-x: extract files"
          if_cp="-x"
	      if_err="false" ;;
      ? ) echo 'Bad options used.' ;;
    esac
done

#
#   default parameters
shift $(($OPTIND - 1))
fileList=("$@")

#
#   function to compress/extract the plt files
#
if [ $if_err == "false" ]; then
  if [ ${#fileList[@]} -eq 0 ]; then
    echo "What files are you compress/extract ?"
    if_err="true"
  else
    for file in "${fileList[@]}"; do
      if [ ! -f $file ]; then
        echo "File not found:" $file
	continue
      fi
      if [ $if_cp == '-z' ]; then
        echo "Compress file: $file"
        tar -czf $file.tar.gz $file
        echo "Done ..."
        echo ""
      elif [ $if_cp == '-x' ]; then
        dir="$(dirname "$file")/extract_file/"
        # create directory if it doesn't exist
        if [ ! -d "$dir" ]; then
          mkdir $dir
        fi
        echo "Extract the file $file to $dir"
        #tar -xzvf $file --strip-components=2 -C $dir
        tar -xzf $file --strip-components=2 -C $dir
        echo "Done ..."
        echo ""
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
