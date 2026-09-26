# OSIRIS

Everything you need to compile, configure, and submit OSIRIS runs. OSIRIS
is the fully-relativistic particle-in-cell (PIC) code the group uses for most
laser wakefield, plasma wakefield, and photon acceleration work.

**First time?** Read the sections in order. Compile OSIRIS (§1), run one of the
1D test decks (§2), then come back to §3 and §4 before you try to write your 
own deck.

1. [Compiling OSIRIS](#1-compiling-osiris)
2. [Submitting a job (`jobex.sh`)](#2-submitting-a-job-jobexsh)
3. [Input deck structure (general OSIRIS)](#3-input-deck-structure-general-osiris)
4. [Useful resources](#4-where-to-go-next)

The following is a map of this directory:

```
.
├── decks      <-- example input decks for 1D, 2D, 3D, and Quasi-3D
│   ├── 1D
│   ├── 2D
│   ├── 3D
│   └── Q3D
├── jobex.sh   <-- example batch script
└── README.md  <-- you are here
```

---

## (1) Compiling OSIRIS

OSIRIS is written in Fortran (with some C). To build it you need:

- MPI
- a Fortran and C compiler (GNU or Intel)
- optionally (but we will use it), parallel HDF5, which OSIRIS uses for its 
  output files

OSIRIS is compiled **separately for each dimension**, so to run a 1D deck you
need a 1D binary and to run a 2D deck you need a 2D binary. The general
workflow for compiling is, from the top of the OSIRIS source tree:

```bash
./configure -d <dimensions> -s <system_config>
make
```

So, for example, if I wanted to compile OSIRIS with a 2D binary, I can run (from 
the top of the OSIRIS source tree): 

```bash
./configure -d 2 -s <system_config>
make
```

The executable that's created as a result ends up in the `bin/` directory, e.g.
`bin/osiris-2D.e`.

### On Great Lakes

[Great Lakes](https://documentation.its.umich.edu/arc-hpc/greatlakes/user-guide)
is U-M's shared computing cluster. If you haven't used one before, here's a 
brief explanation of how they work:

- You **log in** to a **login node**. This is a shared machine for editing files,
  compiling code, and submitting jobs.
- Your simulations run on **compute nodes** by submitting jobs to Slurm, the 
  scheduler that shares the machine between users.
- **Never run OSIRIS directly on a login node.** Compiling there is fine, but
  running large simulations is not.

#### Before you start (one time only)

1. **Request a Great Lakes login.** Use the [ARC login request portal](https://caen.engin.umich.edu/rc/getting-started/)
   to do this (scroll down to find the request link on that page).
2. **Ask Alec to add you to the group's Slurm account.** That account name goes
   in `--account` in `jobex.sh`, and your scratch folder is named after it.

#### Step 1: Log in

From a terminal, run:

```bash
ssh <uniqname>@greatlakes.arc-ts.umich.edu
```

You need to be **on campus or connected to the UM-VPN**. You'll be asked for your
password then an Okta confirmation. Once you're in, the prompt shows a login 
node name, like `[uniqname@gl-login1 ~]$`.

#### Step 2: Know where files go
 
| Location | Use it for | Watch out for |
| :--- | :--- | :--- |
| `~` (your home folder) | OSIRIS source, builds, scripts, input decks | 80 GB quota |
| `/scratch/<account>_root/<account>/<uniqname>` | Simulation output | Files **not accessed for 60 days are deleted** |

Simulation output can easily fill up your home directory, so make sure to send 
all of your data to scratch (`DATA_DIR` in `jobex.sh`). Copy anything you want to 
keep, such as figures or processed data, somewhere permanent.

#### Step 3: Load modules

Software on Great Lakes isn't available until you *load* it with the `module`
command. Some useful commands:

```bash
module list            # what's loaded right now
module avail           # what's available to load
module spider hdf5     # search for a package and see how to load it
module purge           # unload everything
```

To compile OSIRIS, we need to load the following set of modules:

```bash
module load intel/2022.1.2
module load openmpi/4.1.6
module load libaec/1.1.7
module load phdf5/1.12.1
module load fftw/3.3.10
```

These are the Intel compiler, MPI, parallel HDF5 (with `libaec`, a compression
library it depends on), and FFTW.

#### Step 4: Download and compile OSIRIS

```bash
mkdir -p ~/software && cd ~/software
git clone https://github.com/osiris-code/osiris.git
cd osiris

# The following configures OSIRIS for 1D. If you want two dimensions, for example,
# after running `make` below, you can also run `make 2d`.
./configure -s greatlakes.intel -d 1

# The following will take a few minutes; just make sure there are no errors,
# but there will be a lot of output.
make
```

This builds the public version of OSIRIS. For specialized code such as
Q3D, QED, or photon kinetics, see [Special features](#special-features-q3d-qed-photon-kinetics) below.

#### Step 5: Point `jobex.sh` at your build
 
Copy `jobex.sh` to your location of choice in your home directory on Great Lakes. 
Inside the file, set `ROOT_DIR` in your copy of `jobex.sh` to the folder you just built in,
e.g. `ROOT_DIR=$HOME/software/osiris`. Now you're ready for §2 (and can likely
skip the following subsections unless you explicitly need them)!

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
- **Photon kinetics:** photon kinetic (PKT) modeling of laser pulses in plasma

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

---

## (2) Submitting a job (`jobex.sh`)

`jobex.sh` is the shared Slurm template for OSIRIS jobs on Great Lakes. Every 
setting is commented in the script itself. You can submit a job via the `sbatch` 
command followed by the location of the batch script. So, if you copied the
script to your home directory, to submit a job you'd run:
 
```bash
sbatch ~/jobex.sh
```

The script loads the modules OSIRIS needs itself, so you don't need to set 
anything up in your terminal first.

### Slurm settings (`#SBATCH` lines)

Change these for every run:

| Flag | What it does |
| :--- | :--- |
| `--job-name` | Name shown in `squeue` and in notification emails |
| `--nodes` | Number of compute nodes |
| `--tasks-per-node` | MPI ranks per node (standard nodes have 36 cores) |
| `--time` | Wall-clock limit (`HH:MM:SS`); the job is killed when it runs out |
| `--account` | Slurm account the compute time is billed to |
| `--mail-user` | Your email, for job start/end/failure notifications |

You can usually leave these alone, but don't be afraid to change them if you
need/want to:

| Flag | What it does |
| :--- | :--- |
| `--mem-per-cpu` | Memory per MPI rank |
| `--partition` | Queue to run in; `standard` is the normal CPU partition |
| `--export` | `ALL` copies your environment variables into the job |
| `--mail-type` | Which events trigger an email |

**Matching `node_number`:** the total number of MPI ranks,
`--nodes` × `--tasks-per-node`, must equal the number set by `node_number`
in the deck's `node_conf` section. In 1D, that's just the value of
`node_number`: a deck with `node_number(1:1) = 4` needs `--nodes=1` and
`--tasks-per-node=4`. In 2D and 3D, it's the **product** of the values: a 2D
deck with `node_number(1:2) = 8, 9` splits the box into 8 × 9 = 72 pieces,
so it needs `--nodes=2` and `--tasks-per-node=36`. If the totals don't
match, OSIRIS stops at startup.
 
**`--time`:** run time grows quickly with dimension and resolution. A 2D run
can take much longer than the 1D version of the same problem, so budget
accordingly. Don't be the person who submits jobs with an insane wall time
simply because you're too lazy to estimate how long your job will take.

### Run settings (below "EDIT BELOW HERE")
 
| Variable | What to set it to |
| :--- | :--- |
| `DIMS` | `1D`, `2D`, or `3D`. Selects `osiris-<DIMS>.e`, so it must match your deck |
| `INPUTFILE` | Path to your input deck |
| `RUNTITLE` | Optional label for the output folder name (no spaces) |
| `ROOT_DIR` | Your OSIRIS build directory, the one containing `bin/` |
| `DATA_DIR` | Where run folders are created. Use `/scratch`, and create it first |

### What happens when the job runs

1. The script clears any loaded modules and loads the ones OSIRIS was compiled
   with.
2. It creates a run directory, `DATA_DIR/os4.0_<DIMS>_<RUNTITLE>_<jobID>/`.
3. It copies the executable and your deck into that directory. The deck is
   renamed `os-stdin`, because that's the file OSIRIS reads its input from.
4. It runs OSIRIS with `mpirun`, so all the output from the code ends up in the
   run folder.

---

## (3) Input deck structure

An OSIRIS input deck is a text file made up of **sections** in the form 
`section_name{ key = value, }`. The sections must appear in a fixed order. Below
is a stripped-down 1D example showing that order. You can start with one of the
decks in `decks/` instead of writing one from scratch.

```fortran
simulation { }                                   ! global options
 
node_conf {                                      ! parallel decomposition
  node_number(1:1) = 4,                          ! MPI ranks per direction -> must match jobex.sh
  if_periodic(1:1) = .false.,
}
 
grid       { nx_p(1:1) = 2000, }                 ! number of cells
time_step  { dt = 0.0099, ndump = 100, }         ! time step; base dump interval
space      { xmin(1:1) = 0.0, xmax(1:1) = 20.0, }! box size
time       { tmin = 0.0, tmax = 100.0, }         ! simulation length
 
el_mag_fld { }                                   ! field solver options
emf_bound  { type(1:2,1) = "open", "open", }     ! field boundaries
diag_emf   { ndump_fac = 1, reports = "e1", "e2", }
 
particles  { num_species = 1, }                  ! how many species follow
 
! --- repeat this block once per species, in order ---
species      { name = "electrons", num_par_x(1:1) = 8, rqm = -1.0, }
profile      { ... }                             ! density profile
spe_bound    { type(1:2,1) = "open", "open", }
diag_species { ndump_fac = 1, reports = "charge", }
 
! --- optional: lasers, current smoothing, etc. ---
zpulse { ... }
```

**Units.** OSIRIS uses normalized units. Lengths are in $c/\omega_p$, times in
$1/\omega_p$, densities in $n_0$, and fields in $m_e c\,\omega_p / e$. Some
laser decks normalize to the laser frequency $\omega_0$ instead, so check the
comments at the top of the deck.

**Output.** Everything goes into `MS/`: fields in `MS/FLD/`, phase spaces in
`MS/PHA/`, and raw particle data in `MS/RAW/`, all as HDF5. The notebooks/python
scripts in [`../analysis/`](../analysis) read these files.

If you need more information on the input file format or the possible sections
you can use in these input files, please see the 
[official OSIRIS reference guide](https://osiris-code.github.io/osiris/reference/).

---

## (4) Useful resources

- **Analyze your output:** [`../analysis/`](../analysis) and the
  [Python Analysis Environment](../docs/analysis/python-env.md) guide
- **Official OSIRIS documentation:** full reference for every input deck
  section and parameter: <https://osiris-code.github.io/>
- **Cluster details:** [Great Lakes HPC Guide](../docs/clusters/great-lakes.md)


