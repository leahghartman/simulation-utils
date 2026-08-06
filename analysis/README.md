# Data Analysis and Post-Processing Package

This directory contains `sim_analysis`, a portable Python package for loading,
processing, and visualizing output data (HDF5/openPMD) from the simulation codes
I frequently use (OSIRIS, HiPACE++, etc.).

It is designed to be installed once in your Python environment so you can run 
analysis scripts or Jupyter notebooks from **any directory** on your machine
or HPC cluster.

---

## Quick Setup (2-Step Installation)

Before using the analysis tools or notebooks, install `sim_analysis` into your
active Conda environment in **editable mode** (`-e`).

### 1. Activate your environment and install
```
```bash
# Navigate to this directory
cd analysis

# Activate your analysis Conda environment
conda activate osiris-analysis

# Install in editable mode
pip install -e .
