#!/bin/bash

#“#SBATCH” directives that convey submission options:

#SBATCH --job-name <name-of-your-job>
#SBATCH --nodes=1
#SBATCH --tasks-per-node=36
#SBATCH --mem-per-cpu=1g
#SBATCH --time 3:00:00
#SBATCH --account=<name-of-account>
#SBATCH --export=ALL
#SBATCH --partition=standard

#SBATCH --mail-user=<your-uniqname>@umich.edu
#SBATCH --mail-type=BEGIN,END,FAIL

#############################################################################################
# EDIT BELOW HERE
#############################################################################################

# select code version here (1D, 2D etc.)
export DIMS=1D
export INPUTFILE=<path-to-input-file>

## OPTIONAL - CAN BE BLANK, no space
export RUNTITLE=<name-of-your-job>

export ROOT_DIR=<path-to-osiris-installation>
export DATA_DIR=<where-to-store-your-data>


#############################################################################################

export EXEC=osiris-${DIMS}.e
export DIR_NAME=os4.0_${DIMS}_${RUNTITLE}_${SLURM_JOB_ID}

mkdir ${DATA_DIR}/${DIR_NAME}
cp -f ${ROOT_DIR}/bin/${EXEC} ${DATA_DIR}/${DIR_NAME}
cp -f ${INPUTFILE} ${DATA_DIR}/${DIR_NAME}/os-stdin

# Create root directory
cd ${DATA_DIR}/${DIR_NAME}

# Run code
mpirun ${EXEC}
