#!/bin/bash

# code to copy today's WRF forecast files to kopah

# user needs to update this based on their .bashrc 
# Kate's has MACC_KEY and HEWETT_KEY 
export AWS_ACCESS_KEY_ID=$MACC_KEY
export AWS_SECRET_ACCESS_KEY=$MACC_SECRET
export AWS_REGION='us-west-2'

dstr=`date -u +%Y%m%d`00
indir0=/gscratch/macc/kmhewett/LO_data/wrf/
indir=$indir0$dstr/
echo $indir > /gscratch/macc/kmhewett/LO/driver/wrf_to_kopah.log
s5cmd_bin=$(command -v s5cmd || echo "/usr/local/bin/s5cmd")
$s5cmd_bin sync $indir s3://liveocean-kmhewett/LO_data/wrf/$dstr/ >> /gscratch/macc/kmhewett/LO/driver/wrf_to_kopah.log
