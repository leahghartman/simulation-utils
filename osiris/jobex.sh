#!/bin/bash

###############################################################################
# jobex.sh: SLURM submission script for OSIRIS on Great Lakes.
#
# Usage:
#   1. Copy this file (to keep the template clean): `cp jobex.sh my_job.sh`
#   2. Replace everything in <angled brackets> below.
#   3. Submit:  `sbatch my_job.sh`
#
#   The script loads the modules OSIRIS needs itself, so you don't have to 
#   every time you login to the cluster.
#
#   See osiris/README section 3 for more detail.
###############################################################################

# --- SLURM SETTINGS: CHANGE FOR EVERY RUN ------------------------------------

# Name shown in squeue and in notification emails
#SBATCH --job-name <name-of-your-job>

# Number of compute nodes
#SBATCH --nodes=1

# MPI ranks per node (Great Lakes standard nodes have 36 cores).
# nodes x tasks-per-node must equal the total set by node_number in the deck.
#SBATCH --tasks-per-node=36

# Wall-clock limit (HH:MM:SS); your job will be killed when it runs out
#SBATCH --time 1:00:00

# Slurm account the compute time is billed to
#SBATCH --account=<name-of-account>

# Where job notifications are sent
#SBATCH --mail-user=<your-uniqname>@umich.edu

# --- SLURM SETTINGS: USUALLY LEAVE THESE ALONE -------------------------------

# Memory per MPI rank
#SBATCH --mem-per-cpu=1g

# Partition to run on; "standard" is the normal CPU partition. There is also
# "standard-oc" (specifically for software that can only be use on campus), 
# "largemem" (large memory), "gpu", "spgpu", and "debug".
#SBATCH --partition=standard

# Copy your shell environment (loaded modules, variables) into the job
#SBATCH --export=ALL

# Which events trigger an email (when job ends, begins, and if it fails)
#SBATCH --mail-type=BEGIN,END,FAIL


###############################################################################
# EDIT BELOW HERE
###############################################################################

# Which OSIRIS executable to use: 1D, 2D, or 3D. Must match your input deck.
export DIMS=1D

# Path to your input deck.
export INPUTFILE=<path-to-input-file>

# OPTIONAL: label added to the output folder name. Can be blank; no spaces.
export RUNTITLE=<name-of-your-job>

# Your OSIRIS build directory (the one that contains e.g. bin/osiris-2D.e).
export ROOT_DIR=<path-to-osiris-installation>

# Where run folders are created and data from your run is stored. Use /scratch,
# not /home. Must already exist.
export DATA_DIR=<where-to-store-your-data>


###############################################################################
# NOTHING TO EDIT BELOW THIS LINE
###############################################################################

# Load the same modules OSIRIS was compiled with. Start from a clean slate so
# nothing loaded in the terminal leaks into your job.
module purge
module load intel/2022.1.2
module load openmpi/4.1.6
module load libaec/1.1.7
module load phdf5/1.12.1
module load fftw/3.3.10

# Executable name and a unique output folder name, e.g. os4.0_1D_myrun_12345678
export EXEC=osiris-${DIMS}.e
export DIR_NAME=os4.0_${DIMS}_${RUNTITLE}_${SLURM_JOB_ID}

# Create the run directory and copy in the executable and deck.
# OSIRIS reads its input from a file called os
mkdir ${DATA_DIR}/${DIR_NAME}
cp -f ${ROOT_DIR}/bin/${EXEC} ${DATA_DIR}/${DIR_NAME}
cp -f ${INPUTFILE} ${DATA_DIR}/${DIR_NAME}/os-stdin

# Move into the run folder, so all output is written here.
cd ${DATA_DIR}/${DIR_NAME}

# Run OSIRIS on all allocated MPI ranks.
mpirun ${EXEC}
