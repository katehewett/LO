"""
Program to plot historical records for rivers. Saves a sequence of png's.
"""

import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from lo_tools import Lfun
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-ctag', type=str, default='lo_base')
args = parser.parse_args()
ctag = args.ctag

Ldir = Lfun.Lstart()

ctag = 'lo_base'

# location of historical data to plot
riv_dir0 = Ldir['LOo'] / 'pre' / 'river1' / ctag
riv_dir = riv_dir0 / 'Data_historical'
plot_dir = riv_dir0 / 'Data_historical_plots'
Lfun.make_dir(plot_dir)
all_df = pd.read_pickle(riv_dir / 'ALL_flow.p')

tt = all_df.index
year0 = tt.year[0]
year1 = tt.year[-1]
dt0 = datetime(year0,1,1)
dt1 = datetime(year1,12,31)

plt.close('all')
ii = 0
fig_num = 0
for rn in all_df.columns:
    r = all_df[rn]
    if np.mod(ii,9) == 0:
        fig_num += 1
        fig = plt.figure(figsize=(20,10))
        jj = 1
    ax = fig.add_subplot(3,3,jj)
    r.plot(ax = ax)
    ax.text(.05, .9, '%s: mean = %d $[m^{3}s^{-1}]$' % (rn.title(), int(r.mean())),
        transform=ax.transAxes, weight='bold')
    ax.set_xlim(dt0,dt1)
    if jj < 7:
        ax.set_xticklabels([])
    jj += 1 # increment panel counter
    ii += 1 # increment figure counter
    if (np.mod(ii,9) == 0) or (rn == all_df.columns[-1]):
        fig.savefig(plot_dir / ('ALL_flow_plot_' + str(fig_num) + '.png'))

# plt.show()



