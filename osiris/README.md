# OSIRIS

This directory contains everything needed to compile, configure, and submit
runs of **OSIRIS**, the relativistic particle-in-cell (PIC) code used for most
of the group's laser wakefield/plasma wakefield and photon acceleration
work.

---
## Table of Contents
1. [What's in this directory](#1-whats-in-this-directory)
2. [Compiling OSIRIS](#2-compiling-osiris)
3. [Submitting a run (`jobex.sh`)](#3-submitting-a-run-jobexsh)
4. [Input deck structure (general OSIRIS)](#4-input-deck-structure-general-osiris)
5. [Common input deck mistakes](#6-common-input-deck-mistakes)
6. [Where to go next](#7-where-to-go-next)
---


## 1. What's in this directory

```
.
├── decks
│   ├── 1D
│   │   └── photon_kinetics_tests
│   └── 2D
│       └── photon_kinetics_tests
├── jobex.sh                        <-- Slurm submission template
├── profile.osiris
└── README.md                       <-- you are here
```


---

## 2. Compiling OSIRIS

OSIRIS is compiled from Fortran 


### On Great Lakes


### Local (macOS/Linux)


---

## 3. Submitting a Run

`jobex.sh` is the shared Slurm template for OSIRIS jobs on Great Lakes.
 
```bash
sbatch jobex.sh <path/to/input_deck>
```
 
Key things to edit before submitting:
- `#SBATCH --account=` — your allocation
- `#SBATCH --ntasks=` — must match the parallel decomposition (`node_number`)
  set in the input deck's `node_conf` section, or OSIRIS will error out on
  startup
- `#SBATCH --time=` — wall-clock; PKT 2D runs with fine resolution can take
  much longer than the 1D equivalent, budget accordingly

> **TODO (Leah):** paste in the actual `jobex.sh` contents here (or link
> directly) with inline `#` comments explaining each Slurm flag, so the next
> student doesn't have to reverse-engineer it.


---

## 4. Input deck structure (general OSIRIS)


---

## 5. Common input deck mistakes


--- 

## 6. Where to go next

