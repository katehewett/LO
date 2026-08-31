#!/bin/bash

# code to copy today's WRF forecast files to kopah

# Map your unique profile keys to standard s5cmd variables
if [[ "$USER" == *"kmhewett"* ]]; then
    export AWS_ACCESS_KEY_ID=$MACC_KEY
    export AWS_SECRET_ACCESS_KEY=$MACC_SECRET
else
    export AWS_ACCESS_KEY_ID=$access_key
    export AWS_SECRET_ACCESS_KEY=$secret_key
fi
export AWS_REGION='us-west-2' 

# 2. Run a quick check to make sure they mapped correctly
LOG_FILE="/gscratch/macc/kmhewett/LO/driver/wrf_to_kopah_map.log"
if [ -z "$AWS_ACCESS_KEY_ID" ]; then
    echo "ERROR: Script subshell could not read keys from environment." > "$LOG_FILE"
    exit 1
fi

dstr=`date -u +%Y%m%d`00
indir0=/gscratch/macc/kmhewett/LO_data/wrf/
indir=$indir0$dstr/
echo $indir > /gscratch/macc/kmhewett/LO/driver/wrf_to_kopah.log
s5cmd_bin=$(command -v s5cmd || echo "/usr/local/bin/s5cmd")
$s5cmd_bin sync $indir s3://liveocean-kmhewett/LO_data/wrf/$dstr/ >> /gscratch/macc/kmhewett/LO/driver/wrf_to_kopah.log
