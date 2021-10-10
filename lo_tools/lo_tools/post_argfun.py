"""
Shared helper functions for the extraction code, especially for argument passing.

"""
import argparse
import sys
from lo_tools import Lfun

def intro():
    parser = argparse.ArgumentParser()
    # which run to use
    parser.add_argument('-gtx', '--gtagex', type=str)   # e.g. cas6_v3_l08b
    parser.add_argument('-ro', '--roms_out_num', type=int, default=0) # 1 = Ldir['roms_out1'], etc.
    # select time period and frequency
    parser.add_argument('-r', '--run_type', type=str)   # backfill or forecast
    parser.add_argument('-d', '--date_string', default='', type=str) # e.g. 2019.07.04
    parser.add_argument('-job', default='', type=str) # e.g. surface0
    parser.add_argument('-test', '--testing', default=False, type=Lfun.boolean_string)
    # get the args and put into Ldir
    args = parser.parse_args()
    argsd = args.__dict__
    for a in ['gtagex', 'roms_out_num', 'run_type', 'date_string', 'testing', 'job']:
        if argsd[a] == None:
            print('*** Missing required argument to forcing_argfun.intro(): ' + a)
            sys.exit()
    gridname, tag, ex_name = args.gtagex.split('_')
    # get the dict Ldir
    Ldir = Lfun.Lstart(gridname=gridname, tag=tag, ex_name=ex_name)
    # add more entries to Ldir
    for a in argsd.keys():
        if a not in Ldir.keys():
            Ldir[a] = argsd[a]
    # set where to look for model output
    if Ldir['roms_out_num'] == 0:
        pass
    elif Ldir['roms_out_num'] > 0:
        Ldir['roms_out'] = Ldir['roms_out' + str(Ldir['roms_out_num'])]

    # create the expected output directories if needed
    # (a convenience when running make_forcing_main.py on its own while testing)
    out_dir = Ldir['LOo'] / 'post' / Ldir['gtagex'] / ('f' + Ldir['date_string']) / Ldir['job']
    Lfun.make_dir(out_dir)
    Lfun.make_dir(out_dir / 'Info')
    Lfun.make_dir(out_dir / 'Data')

    return Ldir.copy()
    
def finale(Ldir, result_dict):
    out_dir = Ldir['LOo'] / 'post' / Ldir['gtagex'] / ('f' + Ldir['date_string']) / Ldir['job']
    time_format = '%Y.%m.%d %H:%M:%S'
    total_sec = (result_dict['end_dt']-result_dict['start_dt']).total_seconds()
    if 'note' in result_dict.keys():
        pass
    else:
        result_dict['note'] = 'NONE'
        
    s1 = ('* post=%s, day=%s, result=%s, note=%s\n' %
        (Ldir['frc'], Ldir['date_string'], result_dict['result'], result_dict['note']))
    
    s2 = ('  start=%s (took %d sec)\n' %
        (result_dict['start_dt'].strftime(time_format), int(total_sec)))
    
    with open(out_dir / 'Info' / 'results.txt', 'w') as ffout:
        ffout.write(s1 + s2)
    