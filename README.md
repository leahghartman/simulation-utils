# Simulation Software Utilities

A collection of input decks, Slurm submission scripts, and analysis workflows
for plasma simulation codes used in Alec Thomas's research group at the
University of Michigan.

**New to the group?** Start with [New here? Start here](#new-here-start-here) below.

## Contents
 
- [New here? Start here](#new-here-start-here)
- [Find what you need](#find-what-you-need)
- [Simulation codes](#simulation-codes)
- [Computing and HPC guides](#computing-and-hpc-guides)
- [Repository layout](#repository-layout)
- [Getting help and contributing](#getting-help-and-contributing)

## New here? Start here

Work through the following steps in order. Most people can get through the 
first three in an afternoon.

1. **Get cluster access and learn the basics.** Read the [Great Lakes HPC Guide](docs/clusters/great-lakes.md).
   It covers modules, Slurm queues, and where to keep files (`/scratch` vs `/home`).
2. **Run a small test simulation.** Pick the code you'd like to use below and 
   follow its guide. Start with a small 1D or 2D run before trying anything large.
3. **Setup your analysis environment.** Follow the [Python Analysis Environment](docs/analysis/python-env.md)
   to create a Conda environment and set up Open OnDemand.
4. **Look at your output.** Open one of the notebooks in [`analysis/`](./analysis) and point
   it at your run's output directory.

## Find what you need

| I want to... | Go to |
| :--- | :--- |
| Run OSIRIS | [OSIRIS Guide](./osiris/README.md) |
| Run HiPACE++ | [HiPACE++ Guide](./hipace/README.md) |
| Submit a job on Great Lakes | [Great Lakes HPC Guide](docs/clusters/great-lakes.md) |
| Compile or test on my laptop | [Local Development Setup](docs/clusters/local-setup.md) |
| Plot or analyze simulation output | [`analysis/`](./analysis) and the [Python Analysis Environment](docs/analysis/python-env.md) |
| Find an example input deck | The `osiris/` or `hipace/` folder for your code |

## Simulation codes

| Code | What it does | Guide | Submission script |
| :--- | :--- | :--- | :--- |
| **OSIRIS**   | Fully relativistic PIC (1D/2D/3D) | [OSIRIS Guide](./osiris/README.md) | [`osiris/jobex.sh`](./osiris/jobex.sh) |
| **HiPACE++** | Quasi-static 3D PIC | [HiPACE++ Guide](./hipace/README.md) | [`hipace/jobex.sh`](./hipace/jobex.sh) |

Not sure which code to use? OSIRIS is the general-purpose choice we usually
default to in our group for most laser-plasma problems, but if you are unsure, 
you can always ask Alec or another graduate student in the group. We're happy
to help! :)

## Computing and HPC guides

Read these before submitting large runs.

| Guide | Covers |
| :--- | :--- |
| [Great Lakes HPC Guide](docs/clusters/great-lakes.md) | System modules, Slurm queue options, storage quotas (`/scratch` vs `/home`) |
| [Local Development Setup](docs/clusters/local-setup.md) | Compiling and testing light 1D/2D runs on your own machine |
| [Python Analysis Environment](docs/analysis/python-env.md) | Conda environments, HDF5 reader libraries, Open OnDemand setup |

---

## Repository layout

```
.
├── osiris/      # OSIRIS input decks, cluster configs, and jobex.sh
├── hipace/      # HiPACE++ input decks, cluster configs, and jobex.sh
├── analysis/    # Jupyter notebooks and Python scripts for post-processing
└── docs/        # Lab documentation, HPC best practices, onboarding
    ├── clusters/
    └── analysis/
```
 
Each code folder is self-contained: all of the information you need to run that
code is contained in it.

## Getting help and contributing

- **Stuck?** You're welcome to contact Alec, myself, or any other graduate student
  in the group if you struggle with any of the information presented here. Just
  describeto us the problem you ran into and the error you're getting!
- **Found something outdated?** Pull requests are welcome, especially fixes to
  the guides.
- **Adding new code?** Copy the structure of `osiris/`: a `README.md`, a `jobex.sh`,
  and an example input deck.






