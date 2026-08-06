# Simulation Software Utilities

A collection of input decks, Slurm submission scripts, and analysis workflows
for plasma simulation codes used throughout my PhD research and in our group.

---

## Overview of Simulation Codes

| Code | Type | Submission Template | Documentation |
| :--- | :--- | :--- | :--- |
| **OSIRIS** | Relativistic PIC (1D/2D/3D) | [`osiris/jobex.sh`](./osiris/jobex.sh) | [OSIRIS Guide](./osiris/README.md) |
| **HiPACE++** | Quasi-static 3D PIC | [`hipace/submit_hipace.sh`](./hipace/submit_hipace.sh) | [HiPACE++ Guide](./hipace/README.md) |

---

## Shared Computing and HPC Guides

Before submitting large runs, here are some setup guides for various machines:

* **[Great Lakes HPC Guide](docs/clusters/great-lakes.md)** – System modules, Slurm queue options, and storage quotas (`/scratch` vs `/home`).
* **[Local Development Setup](docs/clusters/local-setup.md)** – Compiling and testing light 1D/2D runs on local machines.
* **[Python Analysis Environment](docs/analysis/python-env.md)** – Conda environments, HDF5 reader libraries, and Open OnDemand setup.

---

## Repository Layout

* **`osiris/` & `hipace/`** – Self-contained directories with input decks, cluster 
configurations, and the primary batch submission script for each code.
* **`analysis/`** – Post-processing tools, interactive Jupyter notebooks, and 
automated Python scripts for analyzing simulation output.
* **`docs/`** – Shared lab documentation, HPC best practices, and onboarding 
instructions.







