from pydantic import BaseModel
from typing import List
import numpy as np

class Meson(BaseModel):
    '''Meson dataclass matching that of input yaml files 
    Output -> xml file 
    DISTILLATION BASIS GENERATION SHOULD ALWAYS BE RUN FIRST IN THE CHAIN!
    '''
    # universal imports for a given ensemble 
    num_vecs: int 
    NL: int
    NT: int
    Frequency: int
    t_start: int 

    # t_source_list: list HARDCODED RIGHT NOW 0-64
    meson_nvec: int
    meson_zphases: list
    mom2_min: int 
    mom2_max : int
    momentum_list: List[str] = [
    f"{x} {y} {z}" for x, y, z in [
        (0, 0, 0), (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0), (0, 0, 1),
        (0, 0, -1), (2, 0, 0), (-2, 0, 0),
        (0, 2, 0), (0, -2, 0), (0, 0, 2),
        (0, 0, -2), (3, 0, 0), (-3, 0, 0),
        (0, 3, 0), (0, -3, 0), (0, 0, 3),
        (0, 0, -3)
    ]
]
    displacement_list: List[str] = ['', '1', '2', '3', '1 1', '2 2', '3 3', '1 2', '1 3', '2 1', '2 3', '3 1', '3 2']

    Nt_forward: int
    Nt_backward: int 
    decay_dir: int 
    num_tries: int 
    max_rhs: int 
    phase: list 
    #link smearing options 
    LinkSmearingType: str
    link_smear_fact: float
    link_smear_num: int
    no_smear_dir: int

    # meson_path: str
    cfg_path: str
    colorvec_file: str = 'res/eigs-64.sdb'
    # colorvec_out : str
    
t_source_list = np.array(range(64))