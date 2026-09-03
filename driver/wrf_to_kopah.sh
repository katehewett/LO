#!/bin/bash

# code to copy today's WRF forecast files to kopah
# flexible for Parker and Kate to run forecast

if [ -f "$HOME/.bash_profile" ]; then source "$HOME/.bash_profile"; fi
if [ -f "$HOME/.bashrc" ]; then source "$HOME/.bashrc"; fi

CURRENT_USER=$(whoami)

# UW Kopah s5cmd relies on S3_endpoint_url so this should work
export S3_ENDPOINT_URL='https://s3.kopah.uw.edu'

if [ "$CURRENT_USER" = "kmhewett" ] || [ "$CURRENT_USER" = "katehewett" ]; then
    # Kate has two sets of access keys, this pulls MACC from her bashrc 
    export AWS_ACCESS_KEY_ID="${MACC_KEY:-}"
    export AWS_SECRET_ACCESS_KEY="${MACC_SECRET:-}"
    echo "--- Running with Kate's macc credentials (User: $CURRENT_USER) ---"
else
    echo "--- Running with macc credentials (User: $CURRENT_USER) ---"
fi

dstr=`date -u +%Y%m%d`00
indir0=/gscratch/macc/$CURRENT_USER/LO_data/wrf/
indir=$indir0$dstr/
echo $indir > /gscratch/macc/$CURRENT_USER/LO/driver/wrf_to_kopah.log
s5cmd_bin=$(command -v s5cmd || echo "/usr/local/bin/s5cmd")

if [[ "$CURRENT_USER" == *"kmhewett"* ]]; then
    $s5cmd_bin sync $indir s3://liveocean-kmhewett/LO_data/wrf/$dstr/ >> /gscratch/macc/$CURRENT_USER/LO/driver/wrf_to_kopah.log 
elif [[ "$CURRENT_USER" == *"parker"* ]]; then
    $s5cmd_bin sync $indir s3://liveocean-pmacc/LO_data/wrf/$dstr/ >> /gscratch/macc/$CURRENT_USER/LO/driver/wrf_to_kopah.log 
else  
    echo "ERROR: NO MATCHING USER FOUND ($CURRENT_USER). EXITING Script." >> /gscratch/macc/$CURRENT_USER/LO/driver/wrf_to_kopah.log 
    exit 1
fi


