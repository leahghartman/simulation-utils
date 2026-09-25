"""
simutils.readers.osiris
-------------------------
HDF5 readers for OSIRIS simulation data (grid fields, particle datasets,)
"""

from pathlib import Path
from typing import Dict, Tuple, Union, Optional, List
import h5py
import numpy as np


def osiris_load_dataset(
    dump: int,
    data_type: str,
    dataset_name: str,
    sub_path: str,
    path: Union[str, Path] = "./",
    ms_dir: str = "MS",
    h5_key: Optional[str] = None,
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """
    A generic and safe reader for OSIRIS grid-based HDF5 outputs.

    Parameters:
        dump: Simulation dump index number.
        data_type: OSIRIS directory type under MS (e.g., 'FLD', 'DENSITY', 'RAW').
        dataset_name: Name of dataset inside HDF5 file (e.g., 'e1', 'charge-electrons').
        sub_path: Subfolder path relative to data_type (e.g., 'e1' or 'electrons/charge').
        path: Root path to simulation run directory.
        ms_dir: Main output directory name (defaults to 'MS').
        h5_key: Key of the dataset INSIDE the HDF5 file. If none, auto-detects the
                top-level key.

    Returns:
        tuple: (data_array, axes_dict)
    """
    base_path = Path(path) / ms_dir / data_type / sub_path
    filename = f"{dataset_name}-%.6d.h5" % dump
    file_path = base_path / filename

    if not file_path.exists():
        raise FileNotFoundError(f"OSIRIS output file not found: {file_path}")

    with h5py.File(file_path, "r") as h5f:
        if h5_key is not None:
            key = h5_key
        elif dataset_name in h5f:
            key = dataset_name
        else:
            candidates = [k for k in h5f.keys() if k not in ("AXIS", "SIMULATION")]
            if len(candidates) != 1:
                raise KeyError(
                    f"Could not auto-detect dataset key in {file_path}; "
                    f"top-level keys are {list(h5f.keys())}. Pass h5_key= explicitly."
                )
            key = candidates[0]
 
        data = h5f[key][()]
 
        nx_from_sim = None
        if "SIMULATION" in h5f and "NX" in h5f["SIMULATION"].attrs:
            nx_from_sim = h5f["SIMULATION"].attrs["NX"]
 
        axes = {}
        if "AXIS" in h5f:
            axis_group = h5f["AXIS"]
            for idx, axis_key in enumerate(sorted(axis_group.keys())):
                ax_bounds = axis_group[axis_key][()]
                if nx_from_sim is not None and idx < len(nx_from_sim):
                    num_pts = int(nx_from_sim[idx])
                elif idx < data.ndim:
                    num_pts = data.shape[idx]
                else:
                    num_pts = ax_bounds.shape[0]
                axes[f"x{idx + 1}"] = np.linspace(ax_bounds[0], ax_bounds[1], num_pts)
 
        return data, axes

def osiris_load_density(
    dump: int,
    species: str = "plasma",
    path: Union[str, Path] = "./",
    ms_dir: str = "MS",
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """
    Loads charge density data and spatial grid axes for a given species.

    Returns:
        tuple: (data_array, axes_dict)
    """
    return osiris_load_dataset(
        dump=dump,
        data_type="DENSITY",
        dataset_name=f"charge-{species}",
        sub_path=f"{species}/charge",
        path=path,
        ms_dir=ms_dir,
        h5_key="charge",
    )


def osiris_load_efield(
    dump: int,
    component: str = "1",
    path: Union[str, Path] = "./",
    ms_dir: str = "MS",
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """
    Loads electric field component (e1, e2, or e3) and spatial grid axes.

    Returns:
        tuple: (data_array, axes_dict)
    """
    field_name = f"e{component}"
    return osiris_load_dataset(
        dump=dump,
        data_type="FLD",
        dataset_name=field_name,
        sub_path=field_name,
        path=path,
        ms_dir=ms_dir,
        h5_key=field_name,
    )


def osiris_load_bfield(
    dump: int,
    component: str = "1",
    path: Union[str, Path] = "./",
    ms_dir: str = "MS",
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """
    Loads magnetic field component (b1, b2, or b3) and spatial grid axes.

    Returns:
        tuple: (data_array, axes_dict)
    """
    field_name = f"b{component}"
    return osiris_load_dataset(
        dump=dump,
        data_type="FLD",
        dataset_name=field_name,
        sub_path=field_name,
        path=path,
        ms_dir=ms_dir,
        h5_key=field_name,
    )


def osiris_load_raw_particles(
    dump: int,
    species: str = "plasma",
    quantities: Optional[List[str]] = None,
    path: Union[str, Path] = "./",
    ms_dir: str = "MS",
) -> Dict[str, np.ndarray]:
    """
    Loads raw macroparticle quantities for a given species.

    Returns:
        dict: Mapping of quantity names ('x1', 'p1', 'q', etc.) to 1D arrays.
    """
    if quantities is None:
        quantities = ["x1", "x2", "p1", "p2", "p3", "q"]

    base_path = Path(path) / ms_dir / "RAW" / species
    filename = f"RAW-{species}-%.6d.h5" % dump
    file_path = base_path / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Particle raw data file not found: {file_path}")

    particle_data = {}
    with h5py.File(file_path, "r") as h5f:
        for qty in quantities:
            if qty in h5f:
                particle_data[qty] = h5f[qty][()]

    return particle_data
