import os
import os.path
import sys
import re;
import json;
import os
import numpy as np
from IPython.display import *
import pandas as pd
from datetime import timedelta;
import datetime;
from random import randint
from collections import defaultdict
from pylab import rcParams

import matplotlib.pyplot as plt
import pandas as pd
import glob;
import re;
import platform
import matplotlib

import dateutil;
import json;
import urllib.request;
from IPython import get_ipython
import os
import Jupytils

from datetime import timedelta;
from random import randint
from collections import defaultdict
%matplotlib inline
from pylab import rcParams
rcParams['figure.figsize'] = 3, 3
import os;
import datetime
import re

def readFile(file):
    with open(file, "rb") as f:
        c = f.read().decode().replace('\r\n', '\n')
        return c;

def jlog(*args, debug=False, end=' ', **kwargs):
    if (not debug or 'debug' in kwargs and not kwargs(debug) ):
        return;

    for a in args:
        print(a, end=end)
    for k,v in kwargs.items():
        print ("%s = %s" % (k, v))

def LoadJupytils(abspath=None, debug=False):
    
    ip = get_ipython()
    if(abspath is None):
        abspath =os.path.dirname(Jupytils.__file__)
    if(debug):
        print("loading jupytils ... from: "+abspath);
        
    ip.run_line_magic(magic_name="run", line=abspath+"/jcommon.ipynb")
    ip.run_line_magic(magic_name="run", line=abspath+"/DataFrameUtils.py")
    ip.run_line_magic(magic_name="run", line=abspath+"/Features.py")
    ip.run_line_magic(magic_name="run", line=abspath+"/DisplayUtils.py")
    ip.run_line_magic(magic_name="run", line=abspath+"/Classification.py")
    ip.run_line_magic(magic_name="run", line=abspath+"/StatUtils.py")
    ip.run_line_magic(magic_name="run", line=abspath+"/DBUtils.py")
    c = readFile(abspath+"/ajax.html")
    display(HTML(c))
    #print(c)
