"""
photon_init.py
--------------
Generates phase-space photon macroparticle distributions from OSIRIS zpulse 
definitions.
"""

from typing import Dict, Tuple
import numpy as np
from scipy.constants import c, hbar, e, m_e, epsilon_0

def zpulse_to_photon_dist(
    a0: float,
    omega0_omega_p0: float,
    w0_
)
