# MyTool

1. Add path to jupyter notebook so that these modules can be found

ex:
if modules are in /home/e121341/bin/JunChieh_Wang/DS_utils
if you are going to use modules in plt_utils.py in DS_utils,

/home
    -e121341
        -bin
            -JunChieh_Wang
                -DS_utils
                    -__init.py__
                    -feature_utils.py
                    -plt_utils.py
                        -def xy1y2_plt(...)

(1) append this path in Jupyter notebook:
import sys
sys.path.append('/home/e121341/bin/JunChieh_Wang')

(2) import the tools:
from DS_utils import plt_utils

(3) use the tools:
plt_utils.xy1y2_plt(...)
