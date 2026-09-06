#!/bin/bash

# code to copy today's WRF forecast files from klone to kopah

if [ -f "$HOME/.bashrc" ]; then source "$HOME/.bashrc"; fi

CURRENT_USER=$(whoami)

dstr=`date -u +%Y%m%d`00

if [[ "$CURRENT_USER" == *"kmhewett"* ]]; then
    # Kate has two sets of access keys, this pulls MACC from her bashrc 
    export AWS_ACCESS_KEY_ID="${MACC_KEY:-}"
    export AWS_SECRET_ACCESS_KEY="${MACC_SECRET:-}"
    export S3_ENDPOINT_URL="${S3_ENDPOINT_URL:-}" 
    echo "--- Running with Kate's macc credentials (User: $CURRENT_USER) ---"
    indir0=/gscratch/macc/kmhewett/LO_data/wrf/
    indir=$indir0$dstr/
    echo $indir > /gscratch/macc/kmhewett/LO/driver/wrf_to_kopah.log
    s5cmd_bin=$(command -v s5cmd || echo "/usr/local/bin/s5cmd")
    $s5cmd_bin sync $indir s3://liveocean-kmhewett/LO_data/wrf/$dstr/ >> /gscratch/macc/kmhewett/LO/driver/wrf_to_kopah.log

elif [[ "$CURRENT_USER" == *"parker"* ]]; then
    echo "--- Running with macc credentials (User: $CURRENT_USER) ---"
    indir0=/gscratch/macc/parker/LO_data/wrf/
    indir=$indir0$dstr/
    echo $indir > /gscratch/macc/parker/LO/driver/wrf_to_kopah.log
    s5cmd_bin=$(command -v s5cmd || echo "/usr/local/bin/s5cmd")
    $s5cmd_bin sync $indir s3://liveocean-pmacc/LO_data/wrf/$dstr/ >> /gscratch/macc/parker/LO/driver/wrf_to_kopah.log
    
else  
    echo "ERROR: NO MATCHING USER FOUND ($CURRENT_USER). EXITING Script." >> /gscratch/macc/$CURRENT_USER/LO/driver/wrf_to_kopah.log 
    exit 1
fi


