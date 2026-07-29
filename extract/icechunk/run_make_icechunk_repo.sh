#!/bin/bash

## run using a command of the form
## sbatch ./run_make_icechunk_repo.sh &

## Group
#SBATCH -A macc
## Node type
#SBATCH -p cpu-g2

## Resources
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
## Each slice (32 cores) has 256G, so 8GB per core.
#SBATCH --mem=8G
#SBATCH --time=24:00:00

# Do not return until the job is finished (use with & on the command line)
#SBATCH --wait

# activate our conda environment
source /gscratch/macc/parker/miniconda3/etc/profile.d/conda.sh
conda activate loenv

# paths
dir0='/gscratch/macc/parker'
dir1=${dir0}'/LO/extract/icechunk'

# Run the worker
python3 ${dir1}/make_icechunk_repo.py > ${dir1}/run_make_repo.log