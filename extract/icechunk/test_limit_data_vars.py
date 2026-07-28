"""
Code to test limiting data_vars when using xr.concat().
"""

import xarray as xr
from lo_tools import Lfun

Ldir = Lfun.Lstart()

in_dir = Ldir['roms_out'] / 'cas7_t1_x11b' / 'f2025.06.20'
fn1 = in_dir / 'ocean_his_0001.nc'
fn2 = in_dir / 'ocean_his_0002.nc'
ds1 = xr.open_dataset(fn1)
ds2 = xr.open_dataset(fn2)

# limit variables
ds11 = ds1[['salt','temp']]
ds22 = ds2[['salt','temp']]

# this avoids a warning message
xr.set_options(use_new_combine_kwarg_defaults=True)
ds = xr.concat(
    [ds11,ds22], dim="ocean_time", coords="minimal", compat="override", combine_attrs="override"
)