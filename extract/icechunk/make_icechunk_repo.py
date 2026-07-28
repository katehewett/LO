"""
Code to create an icechunk repo for a sequence of history of average ROMS files.
"""

# General imports
import warnings
import os
import pandas as pd
import fsspec
import xarray as xr
from pathlib import Path
from time import time

# Icechunk related imports
import icechunk
from obstore.store import from_url
from virtualizarr import open_virtual_dataset
from virtualizarr.parsers import HDFParser
from obspec_utils.registry import ObjectStoreRegistry
from obstore.store import S3Store

# Set some variables by hand. Eventually these should be generated
# from command line arguments.

gtagex = 'cas7_t2_x11b'
list_type = 'hourly' # hourly (history files) or daily (average files)
ds0 = '' # first day to start an empty repo ('' to use existing repo)
ds1 = '2026.01.03' # last day to append to repo

# Ignore some warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Avoid some random bug
os.environ['AWS_REQUEST_CHECKSUM_CALCULATION']='when_required'
os.environ['AWS_RESPONSE_CHECKSUM_VALIDATION']='when_required'

# ---------------------------------------------------------------

# Load credentials

# Configuration
storage_endpoint = "https://s3.kopah.uw.edu"
storage_bucket = "liveocean-pmacc"
storage_name = 'icechunk-test-2'
bucket_url = f"s3://{storage_bucket}"
# Note the use of f-strings in this code. Clean.

# Setup Filesystem
fs = fsspec.filesystem('s3', anon=False, endpoint_url=storage_endpoint, 
                       skip_instance_cache=True, use_listings_cache=False)

# ---------------------------------------------------------------

# Define Icechunk Storage & Config

storage = icechunk.s3_storage(
    bucket=storage_bucket,
    prefix=f"icechunk/{storage_name}",
    from_env=True,
    endpoint_url=storage_endpoint,
    region='not-used',
    force_path_style=True,
)

config = icechunk.RepositoryConfig.default()
config.set_virtual_chunk_container(
    icechunk.VirtualChunkContainer(
        url_prefix=f"{bucket_url}/",
        store=icechunk.s3_store(region="not-used", anonymous=False, s3_compatible=True, 
                                force_path_style=True, endpoint_url=storage_endpoint),
    ),
)

credentials = icechunk.containers_credentials(
    {f"{bucket_url}/": icechunk.s3_credentials(anonymous=False)}
)

store_obj = S3Store(
    bucket=storage_bucket,
    endpoint=storage_endpoint,
    region="not-used",
)

registry = ObjectStoreRegistry({bucket_url: store_obj})
parser = HDFParser()

# ---------------------------------------------------------------

# --- 1. Get Dates from Icechunk Repo (set_repo) ---
# set repo is just a list of days (unordered) - could rework logic here
try:
    repo = icechunk.Repository.open(storage, config, authorize_virtual_chunk_access=credentials)
    session = repo.readonly_session("main")
    ds = xr.open_zarr(session.store, consolidated=False, chunks={})
    
    if 'ocean_time' in ds.coords:
        # Extract dates as YYYY.MM.DD strings
        dates = pd.to_datetime(ds.ocean_time.values)
        set_repo = set(dates.strftime('%Y.%m.%d'))
    else:
        set_repo = set()
        
except Exception as e:
    print(f"Repo access failed or empty ({e}). Assuming set_repo is empty.")
    repo = None
    set_repo = set()

print(f"set_repo: {len(set_repo)} dates found.")

# ---------------------------------------------------------------

# --- 2. Get Dates from Cloud Bucket (set_cloud) ---
print("Scanning S3 for liveocean files...")

# Note the name "nos" is just leftover from the version of this code I got from
# Rich Signell around 6/2026. We retain it here to avoid extra editing.

# day 1
#nos_files = fs.glob(f'{bucket_url}/LO_roms/cas7_t2_x11b/f2026.01.01/ocean_his*.nc')

# day 2+
nos_files = fs.glob(f'{bucket_url}/LO_roms/{gtagex}/f{ds1}/ocean_his*.nc')
nos_files = nos_files[1:] # drop hour zero because it was done in previous day


nos_urls = []
for f in nos_files:
    nos_path = f's3://{f}'
    nos_urls.append(nos_path)

# ---------------------------------------------------------------

# --- Process NOS ---

tt0 = time()

print(f"Virtualizing {len(nos_urls)} NOS files...")

nos_list = [
    open_virtual_dataset(url, parser=parser, registry=registry, loadable_variables=['ocean_time'])
    for url in nos_urls
]
print('created nos_list (%0.1f sec)' % (time()-tt0))
# this is the slow step (100 sec for 25 files)

# ---------------------------------------------------------------

# Concatenate the virtual datasets

# Avoid a warning message
xr.set_options(use_new_combine_kwarg_defaults=True)

combined_nos = xr.concat(
    nos_list, dim="ocean_time", coords="minimal", compat="override", combine_attrs="override"
)

print('done')
# this is fast

# ---------------------------------------------------------------

# Append the dataset to the repo

ds_final = combined_nos

if ds_final is not None:
    # Ensure we have a valid repo object
    # Note I had to delete the existing repo to make this work.
    if repo is None:
        repo = icechunk.Repository.create(storage, config, authorize_virtual_chunk_access=credentials)
        initial_session = repo.writable_session("main")

        # Append
        print(f"Writing {len(ds_final.ocean_time)} time steps to Icechunk...")
        ds_final.virtualize.to_icechunk(initial_session.store)
    
        # Commit
        msg = f"Initialized with forecast data:"# {new_dates[0]} to {new_dates[-1]}"
        initial_session.commit(msg)
        print(f"Commit successful: '{msg}'")
    # Create Writable Session
    else:
        append_session = repo.writable_session("main")

        # Append
        print(f"Appending {len(ds_final.ocean_time)} time steps to Icechunk...")
        ds_final.virtualize.to_icechunk(append_session.store, append_dim="ocean_time")
    
        # Commit
        msg = f"Appended forecast data:"# {new_dates[0]} to {new_dates[-1]}"
        append_session.commit(msg)
        print(f"Commit successful: '{msg}'")

    # Verify History
    history = repo.ancestry(branch="main")
    latest = next(history)
    print(f"Latest Commit [{latest.written_at}]: {latest.message}")
    
else:
    print("Nothing to append.")

# ---------------------------------------------------------------

# ---------------------------------------------------------------

# ---------------------------------------------------------------



