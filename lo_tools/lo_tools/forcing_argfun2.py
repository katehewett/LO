"""
Shared helper functions for the forcing code, especially for argument passing.

"""
import os
import argparse
import sys
from lo_tools import Lfun

from subprocess import Popen as Po
from subprocess import PIPE as Pi
from time import time

def intro():
    parser = argparse.ArgumentParser()
    # required arguments
    parser.add_argument('-g', '--gridname', type=str)   # e.g. cas6
    parser.add_argument('-f', '--frc', type=str)        # e.g. tide
    parser.add_argument('-tP', '--trapsP', type=str, default='trapsP01') # LO/pre/trapsP## version
    parser.add_argument('-r', '--run_type', type=str)   # backfill or forecast
    parser.add_argument('-s', '--start_type', type=str, default='continuation') # new, continuation, or perfect
    parser.add_argument('-d', '--date_string', type=str) # e.g. 2019.07.04
    # optional arguments
    parser.add_argument('-test', '--testing', default=False, type=Lfun.boolean_string)
    parser.add_argument('-test_planB', default=False, type=Lfun.boolean_string)
    
    # optional arguments used only for ocnN, to determine what to nest inside
    parser.add_argument('-gtx', '--gtagex', default='cas7_t2_x11b', type=str) # e.g. cas7_t2_x11b
    parser.add_argument('-ro', '--roms_out_num', type=int, default=0) # 1 = Ldir['roms_out1'], etc.
    parser.add_argument('-do_bio', default=True, type=Lfun.boolean_string) # True to add bio vars to ocn forcing

    # Specialized flags to send output to kopah.
    parser.add_argument('-k','--to_kopah', default=False, type=Lfun.boolean_string)
    parser.add_argument('-ktest','--test_to_kopah', default=False, type=Lfun.boolean_string)
    
    # get the args
    args = parser.parse_args()
    
    # test that required arguments were provided
    argsd = args.__dict__
    for a in ['gridname', 'frc', 'run_type', 'start_type', 'date_string']:
        if argsd[a] == None:
            print('*** Missing required argument to forcing_argfun.intro(): ' + a)
            sys.exit()
        
    # get the dict Ldir
    Ldir = Lfun.Lstart(gridname=args.gridname)
    # add more entries to Ldir for use by make_forcing_main.py
    for a in ['frc', 'run_type', 'start_type', 'date_string', 'testing','test_planB',
    'gtagex','roms_out_num','do_bio','trapsP','to_kopah','test_to_kopah']:
        Ldir[a] = argsd[a]
    # set where to look for model output
    if Ldir['roms_out_num'] == 0:
        pass
    elif Ldir['roms_out_num'] > 0:
        Ldir['roms_out'] = Ldir['roms_out' + str(Ldir['roms_out_num'])]
        
    # create the expected output directories if needed
    # (a convenience when running make_forcing_main.py on its own while testing)
    out_dir = Ldir['LOo'] / 'forcing' / Ldir['gridname'] / ('f' + Ldir['date_string']) / Ldir['frc']
    Lfun.make_dir(out_dir)
    Lfun.make_dir(out_dir / 'Info')
    Lfun.make_dir(out_dir / 'Data')

    return Ldir.copy()
    
def finale(Ldir, result_dict):
    out_dir = Ldir['LOo'] / 'forcing' / Ldir['gridname'] / ('f' + Ldir['date_string']) / Ldir['frc']
    time_format = '%Y.%m.%d %H:%M:%S'
    total_sec = (result_dict['end_dt']-result_dict['start_dt']).total_seconds()
    if 'note' in result_dict.keys():
        pass
    else:
        result_dict['note'] = 'none'
        
    s1 = ('* frc=%s, day=%s, result=%s, note=%s\n' %
        (Ldir['frc'], Ldir['date_string'], result_dict['result'], result_dict['note']))
    
    s2 = ('  start=%s (took %d sec)\n' %
        (result_dict['start_dt'].strftime(time_format), int(total_sec)))
    
    s3 = ('  %s\n' % (str(out_dir)))
    
    with open(out_dir / 'Info' / 'results.txt', 'w') as ffout:
        ffout.write(s1 + s2 + s3)

    # copy the forcing to kopah
    # This will only write the output of the first day of a forecast.
    if Ldir['to_kopah']:
        tt0 = time()

        # parker is local_user = pmacc and remote_user = parker; kate is the same either way
        local_user = Ldir['local_user'] 

        # Get Kopah access keys
        # calls Lfun function get_s5cmd_env
        s5cmd_env = Lfun.get_macc_s5cmd_env(local_user)
        if s5cmd_env is None:
            print(f"Error: missing valid access key format for user '{local_user}'. Check your bashrc (bash_profile).")
        elif local_user == 'BLANK':
            print(f"Error: Missing a valid local user, did not send to kopah")
        else:
            print(f"s5cmd env successfully loaded for '{local_user}'")

            bucket_name = 'liveocean-' + local_user
            s5cmd_base = shutil.which('s5cmd') or '/usr/local/bin/s5cmd'                 # find the binary path
            s5cmd_bin = [s5cmd_base, '--endpoint-url', s5cmd_env['S3_ENDPOINT_URL']]     # bundle the endpoint to target Kopah automatically, as entered in our bashrc as https://s3.kopah.uw.edu'
            
            cmd_list = s5cmd_bin + ['sync',str(out_dir)+'/*',
                                    's3://'+bucket_name+'/LO_output/forcing/'+Ldir['gridname']+'/f'+Ldir['date_string']+'/'+Ldir['frc']+'/']
            proc = Po(cmd_list, stdout=Pi, stderr=Pi, env=s5cmd_env)
            stdout, stderr = proc.communicate()
            if len(stderr) > 0:
                print('Copy to Kopah stderr')
                # always print errors
                print(stderr.decode())
            print(' - time to copy to kopah = %d sec' % (time()-tt0))
            sys.stdout.flush()
    

