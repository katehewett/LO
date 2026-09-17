"""
Shared helper functions for the forcing code, especially for argument passing.

"""
import os
import argparse
import sys
from lo_tools import Lfun

import shutil
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
    # This kopah flag sets the destination bucket in the macc group's kopah storage 
    # that will recieve history files. If you have access to macc group kopah storage, then 
    # Enter your username that is used on klone. Please do not use -kuser pmacc unless you are Kate or Parker. 
    parser.add_argument('-kuser','--kopah_user', type=str, default = None) 

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
    'gtagex','roms_out_num','do_bio','trapsP','to_kopah','test_to_kopah','kopah_user']:
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

        # parker is current_user = pmacc and remote_user = parker (on klone); kate is the same either way
        current_user = os.environ.get('USER') #Ldir['local_user'] 

        # if no kopah_user exit
        if (Ldir['kopah_user'] is None): 
            print(f"Error: -kuser, kopah_user, is blank. Enter your kopah user name for macc storage. \n \
            If you do not have macc storage credentials check with Kate or Parker.")
            sys.exit()

        # if not kate or parker, and kuser does not equal current_user exit 
        if (current_user not in ('parker', 'pmacc', 'kmhewett', 'katehewett')) and (current_user is not Ldir['kopah_user']):
            print(f"Error: kopah_user and current user do not match. Make sure you are not sending to another users kopah storage.") 
            sys.exit()

        # set bucket name if pass tests 
        if (Ldir['kopah_user'] == 'pmacc'):
            if (current_user in ('parker', 'pmacc', 'kmhewett', 'katehewett')):
                bucket_name = 'liveocean-pmacctest'
                print(f"Sending forcing files to kopah bucket: liveocean-pmacc")
            else: 
                print(f"Error: can not send to liveocean-pmacc. Check kopah credentials.")
                sys.exit()
        else:
            bucket_name = 'liveocean-' + Ldir['kopah_user']
            print(f"Sending forcing files to kopah bucket: {bucket_name}")

        # Get Kopah access keys. Calls Lfun function get_s5cmd_env
        # And send forcing files to macc group kopah storage 
        s5cmd_env = Lfun.get_macc_s5cmd_env(current_user)
        if s5cmd_env is None:
            print(f"Error: missing valid access key format for user '{current_user}'. Check your bashrc (bash_profile).")
        else:
            print(f"s5cmd env successfully loaded for '{current_user}'")

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
    

