"""
Functions to use with the new HYCOM code.  Works for both backfill and forecast files.

"""

# setup
import os
import sys
pth = os.path.abspath('../../alpha')
if pth not in sys.path:
    sys.path.append(pth)
import Lfun

Ldir = Lfun.Lstart()
fn_out = Ldir['LOo'] + 'misc/hycom_test.nc'

import time
from datetime import datetime, timedelta

import netCDF4 as nc

from urllib.request import urlretrieve
from urllib.error import URLError
from socket import timeout

import hfun
from importlib import reload
reload(hfun)

# ** USER **********************************

run_type = 'backfill_u' # 'backfill_u', 'backfill_y', or 'forecast'
    
testing = True # limit requested variables

# ******************************************

aa = hfun.aa

# specify output file
# get rid of the old version, if it exists
try:
    os.remove(fn_out)
except OSError:
    pass # assume error was because the file did not exist

# specify time limits
# get date string in LO format
if run_type == 'forecast':
    dstr00 = datetime.now().strftime('%Y.%m.%d')
elif run_type == 'backfill_u':
    dstr00 = datetime(2012,1,25).strftime('%Y.%m.%d')
elif run_type == 'backfill_y':
    dstr00 = datetime(2018,12,5).strftime('%Y.%m.%d')
    
dt00 = datetime.strptime(dstr00, '%Y.%m.%d')
# put them in ncss format
dstr0 = dt00.strftime('%Y-%m-%d-T00:00:00Z')
dstr1 = dt00.strftime('%Y-%m-%d-T00:00:00Z')

# specify spatial limits
north = aa[3]
south = aa[2]
west = aa[0] + 360
east = aa[1] + 360

if testing == True:
    var_list = 'surf_el'
else:
    var_list = 'surf_el,water_temp,salinity,water_u,water_v'
    
# create the request url
if run_type == 'forecast':
    url = ('http://ncss.hycom.org/thredds/ncss/GLBy0.08/expt_93.0/data/forecasts/FMRC_best.ncd'+
        '?var='+var_list +
        '&north='+str(north)+'&south='+str(south)+'&west='+str(west)+'&east='+str(east) +
        '&disableProjSubset=on&horizStride=1' +
        '&time_start='+dstr0+'&time_end='+dstr1+'&timeStride=8' +
        '&vertCoord=&addLatLon=true&accept=netcdf4')
elif run_type == 'backfill_u':
    url = ('http://ncss.hycom.org/thredds/ncss/GLBu0.08/expt_93.0' + 
        '?var='+var_list +
        '&north='+str(north)+'&south='+str(south)+'&west='+str(west)+'&east='+str(east) +
        '&disableProjSubset=on&horizStride=1' +
        '&time_start='+dstr0+'&time_end='+dstr1+'&timeStride=8' +
        '&vertCoord=&addLatLon=true&accept=netcdf4')
elif run_type == 'backfill_y':
    url = ('http://ncss.hycom.org/thredds/ncss/GLBy0.08/expt_93.0' + 
        '?var='+var_list +
        '&north='+str(north)+'&south='+str(south)+'&west='+str(west)+'&east='+str(east) +
        '&disableProjSubset=on&horizStride=1' +
        '&time_start='+dstr0+'&time_end='+dstr1+'&timeStride=8' +
        '&vertCoord=&addLatLon=true&accept=netcdf4')

"""
NOTES
    
Errors: any malformation of the url results in ee.reason == 400 (failed to reach server).
This happens when we request an out-of-range date.

Grids: note that GLBu and GLBy have different grid spacing.  Also they are 0-360 longitude format.
                
Valid time range for forecasts seems to be about a week into the past and maybe 10 days
into the future.
    
Performance:
    3-16 sec to get just surf_el for one day
    70 sec to get all fields for one day
    
If we use:
    accept=netcdf we get "root group (NETCDF3_CLASSIC data model, file format NETCDF3)"
    accept=netcdf4 we get "root group (NETCDF4 data model, file format HDF5)"
and I will assume netcdf4 is better.

The "&vertCoord=" flag adds the "depth" variable to the output as long as
any the requested variables have depth (so not if we only ask for surf_el).

For backfill the resulting fields are MASKED ARRAYS regardless of which netcdf I chose.
        
For the FMRC_best forecast files, the returned file has this difference. Variables pulled
from the Dataset) arrive as NUMPY ARRAYS WITH NAN'S.  This can affect later processing.
Oddly, pulling a varible from the Dataset throws this warning:
    /Applications/anaconda/bin/ipython:1: RuntimeWarning: invalid value encountered in greater
    #!/Applications/anaconda/bin/python

The fields have a singleton time dimension that is NOT automatically removed:
u = ds['water_u'][:]
u.shape => (1, 40, 351, 126) [packed t, z, y, x]
    
The field "depth" has length 40, is packed TOP-TO-BOTTOM, and goes from 0 to 5000, with
spacing 2 (top 6 cells) to 1000 m (deepest 2 cells).  It is positive.

The "time" has values like: array([166560.]) for 2019.01.01
and its attributes are:
long_name: Valid Time
units: hours since 2000-01-01 00:00:00
time_origin: 2000-01-01 00:00:00

The backfill url string was initially auto-generated by making choices on this website:
https://ncss.hycom.org/thredds/ncss/grid/GLBy0.08/expt_93.0/dataset.html
which sometimes is slow to come up.
** Also, it ONLY WORKED AFTER I changed https to http. **
    
"""

print('Working on ' + dstr00)
# get the data and save as a netcdf file
counter = 1
got_file = False
while (counter <= 3) and (got_file == False):
    print('Attempting to get data, counter = ' + str(counter))
    tt0 = time.time()
    try:
        (a,b) = urlretrieve(url,fn_out)
        # a is the output file name
        # b is a message you can see with b.as_string()
    except URLError as ee:
        if hasattr(ee, 'reason'):
            print(' *We failed to reach a server.')
            print(' -Reason: ', ee.reason)
        elif hasattr(ee, 'code'):
            print(' *The server could not fulfill the request.')
            print(' -Error code: ', ee.code)
    except timeout:
        print(' *Socket timed out')
    else:
        got_file = True
        print(' Worked fine')
    print(' -took %0.1f seconds' % (time.time() - tt0))
    counter += 1

if got_file:
    # check results
    ds = nc.Dataset(fn_out)
    print('\nVariables:')
    for vn in ds.variables:
        print('- '+vn)
    #ds.close()
