#!/usr/bin/env python -i

# Script:  logplot.py
# Purpose: use GnuPlot to plot two columns from a LAMMPS log file
# Syntax:  logplot.py log.lammps X Y
#          log.lammps = LAMMPS log file
#          X,Y = plot Y versus X where X,Y are thermo keywords
#          once plot appears, you are in Python interpreter, type C-D to exit
# Author:  Steve Plimpton (Sandia), sjplimp at sandia.gov

import sys,os
import matplotlib.pyplot as plt
from time import sleep
path = os.environ["LAMMPS_PYTHON_TOOLS"]

# path=''
# print("here")
# if(not path):
# 	os.system('export LAMMPS_PYTHON_TOOLS="' + os.path.dirname(os.path.realpath('README')) + '"')
# 	path = os.environ["LAMMPS_PYTHON_TOOLS"]

sys.path.append(path)
sys.path.append('/media/windows-share/Downloads/lammps-30Jul16/lammps-30Jul16/tools/python/pizza')

from log import log
from gnu import gnu

if len(sys.argv) != 4:
  raise StandardError, "Syntax: logplot.py log.lammps X Y"

logfile = sys.argv[1]
xlabel = sys.argv[2]
ylabel = sys.argv[3]

lg = log(logfile)
x,y = lg.get(xlabel,ylabel)

fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
# ax.plot([0,1,2], [10,20,3])

plt.plot(x,y)
# plt.title()
fig.savefig('to.png')   # save the figure to file
plt.show()
plt.close(fig)  

# g = gnu()
# g.plot(x,y)
# # g('set grid')
# g("set term png")
# g('set out "output.png"')

sleep(20)
print "Type Ctrl-D to exit Python"
