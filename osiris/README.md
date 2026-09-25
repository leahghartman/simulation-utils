# OSIRIS

Everything you need to compile, configure, and submit OSIRIS runs. OSIRIS
is the fully-relativistic particle-in-cell (PIC) code the group uses for most
laser wakefield, plasma wakefield, and photon acceleration work.

**First time?** Read the sections in order. Compile OSIRIS (§2), run one of the
1D test decks (§3), then come back to §4 and §5 before you write your own deck.

← [Back to the main README](../README.md)

## Contents

1. [What's in this directory](#1-whats-in-this-directory)
2. [Compiling OSIRIS](#2-compiling-osiris)
3. [Submitting a job (`jobex.sh`)](#3-submitting-a-job-jobexsh)
4. [Input deck structure (general OSIRIS)](#4-input-deck-structure-general-osiris)
5. [Common input deck mistakes](#6-common-input-deck-mistakes)
6. [Where to go next](#7-where-to-go-next)

## What's in this directory

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

## Compiling OSIRIS

OSIRIS is written in Fortran (with some C). To build it you need:

- a Fortran and C compiler (GNU or Intel)
- MPI
- parallel HDF5, which OSIRIS uses for its output files

OSIRIS is compiled **separately for each dimension**, so to run a 1D deck you
need a 1D binary and to compile a 2D deck you need a 2D binary. The general
workflow for compiling is, from the top of the OSIRIS source tree:

```bash
./configure -d <dimensions> -s <system_config>
make
```

So, for example, if I wanted to compile OSIRIS with a 2D binary, I can run (from 
the top of the OSIRIS source tree): 

```

./configure -d 2 -s <system_config>
make
```

The executable that's created as a result ends up in the `bin/` directory, e.g.
`bin/osiris-2D.e`.

### On Great Lakes


### Local (macOS/Linux)

If you're attempting to install OSIRIS locally, I'm going to assume you *kind of*
know what you're doing, as doing this usually means you're involved in some kind
of code development and know how to properly compile code.

Install a compiler, MPI, and parallel HDF5. On macOS, Homebrew's `gcc`, `open-mpi`,
and `hdf5-mpi` work; on Linux, use your package manager's equivalents. I wouldn't
even try to do this on Windows unless you're familiar with the Windows Subsystem
for Linux (WSL). Then configure with a local system configuration file and `make` 
as above.

Local machines are good for code development and small 1D and 2D tests, but not
production runs. See the [Local Development Setup](../docs/clusters/local-setup.md) guide.

### Special Features: Q3D, QED, photon kinetics

The standard OSIRIS build doesn't include some features. You need the 
**development branch** of the code to run (just as an example):

- **Q3D:** quasi-3D (cylindrical modes) geometry
- **QED:** strong-field QED effects (photon emission, pair production)
- **Photon kinetics:** needed for the decks in `decks/*/photon_kinetics_tests/`

**Step 1: Get access.** Email **Alec** and ask for access to the OSIRIS
development repository. You may need to accept an invite to an organization on
GitHub.

**Step 2: Clone the branch you need.** Keep it in its own directory so you don't
mix it up with a standard build (granted, everything that's available in OSIRIS
4.0 should also be available in the development version, so you can just use
this as your default build instead).

```bash
git clone -b <branch-name> <dev-repo-url> osiris-<feature>
cd osiris-<feature>
```

**Step 4: Compile** the same way as a standard build (see above).

```bash
./configure -d <dimensions> -s <system_config>
make
```

**Step 5: Check** that you're running the binary you think you are. The
`bin/` directory of a dev branch contains executables with the same names as
a standard build, so use the full path in `jobex.sh`, e.g.
`~/codes/osiris-pkt/bin/osiris-2D.e`.

To pick up new changes on the branch later, run `git pull` and then `make` again.

## Submitting a job (`jobex.sh`)

`jobex.sh` is the shared Slurm template for OSIRIS jobs on Great Lakes. You can
submit a job via the `sbatch` command followed by the location of your batch
script:
 
```bash
sbatch jobex.sh
```
 
Edit these things before you submit:

| Slurm flag | What to set it to |
| :--- | :--- |
| `#SBATCH --account=` | Your group's Great Lakes allocation |
| `#SBATCH --ntasks=` | The **product** of `node_number` in the deck's `node_conf` section (e.g. `node_number(1:2) = 8, 4` → `--ntasks=32`). If they don't match, OSIRIS stops at startup. |
| `#SBATCH --time=` | Wall-clock limit. 2D PKT runs at fine resolution take much longer than the 1D equivalent, so budget accordingly. |

## 4. Input deck structure (general OSIRIS)


---

## 5. Common input deck mistakes


--- 

## 6. Where to go next

