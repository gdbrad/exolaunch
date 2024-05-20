'''
Script to execute jobs on cluster using generated shell scripts contained in /res
Inspired by https://github.com/eromero-vlc/chroma-scripts-cori/blob/master/ensembles.sh
'''

import os 
import subprocess
import shlex 
import argparse
import os 
import yaml 
from pydantic import BaseModel,Field
#coding: utf-8
from typing import Dict,Any,Optional,Annotated
from decimal import Decimal
import re 

FDIR = os.path.dirname(os.path.realpath(__file__))
INFILES = os.path.abspath(os.path.join(FDIR, "ens_files"))
CONFS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cfgs'))
cfg_files = os.listdir(CONFS_PATH)


class RunJobs(BaseModel):
    '''
    spawn METAQ instances running chroma jobs on cluster
    '''
    # eigs must be run first then pass checks! 
    #---------------------#
    run_eigs: bool 
    run_perams: bool
    run_mesons: bool
    run_baryons: bool
    run_exotract: bool
    #--------------------#

    user: str
    beta: Annotated[Decimal, Field(default=None,ge=0, decimal_places=3)] | None
    ms: Annotated[Decimal,  Field(default=None,ge=0, decimal_places=3)] | None
    mud: Annotated[Decimal,  Field(default=None,ge=0, decimal_places=3)] | None
    NL: int
    NT: int 
    P: int 
    cfg_i: int  #0001
    cfg_f: int #0400

    max_moms_per_job: int
    machine: str

# def _filenames_to_terminal():

def lauch_eigs():
    '''
    walk through eigs_chroma subdirectory and spawn jobs
    manage directory structure, file naming, storage options 
    instantiates a METAQ instance then actively monitors. 
    TODO should be a babysitter type script that is monitoring this python file and subprocs therein
    '''
    def _eigs_filename():

        for cfg_file in cfg_files:
            cfg_id = int(cfg_file.split('_')[-1].split('.')[0])
        eig_file=




parser = argparse.ArgumentParser()
parser.add_argument('input_yml', default='')

parser.add_argument('cfg_f', type=int)
parser.add_argument('cfg_step', type=int, nargs='?', default=8, help='default: %(default)s')
parser.add_argument('--email', default='', help='default: %(default)s')
parser.add_argument('--eig_dir', default='/res/eigs', help='default: %(default)s')
parser.add_argument('--gconfbase', default='../cfgs', help='default: %(default)s')
parser.add_argument('--exe', default='/chroma', help='default: %(default)s')
parser.add_argument('--jobname', default='sWC_A2p1_Mpi270_L24T96', help='default: %(default)s')
parser.add_argument('--rundir', default='/p/scratch/exotichadrons/grant/perambulators/sWC_A2p1_Mpi270_L24T96/${flavor}/cnfg', help='default: %(default)s')
# parser.add_argument('--start_METAQ',default='y')? put eigs into metaq priority 
# if eigs work is done, 
    
options = parser.parse_args()

conf_start=1
conf_step=1
conf_end=10

# setting up eigs env
for i in range(conf_start,conf_step,conf_end):
  print(f"{i}")
  print('starting config f"{i}"')
  eigs=f"chroma_eigs_{i}.sh"
  subprocess.call(shlex.split(f"chroma_eigs_{i}.sh"))

# check that eigenvectors have been generated and stored in $SCRATCH , TEMP, WHATEVER
# if true, then create a sym link to metaq priority where the eigs live, perform rest of measurements , spawn chroma jobs in tandem 
# DO YOU WANT STORE EIGS ON DISK OR DELETE OR MOVE SOMEWHERE ELSE 

def check_eigs():
    

   return

# if eigs passed above checks and are on disk:
    # set up perams.sh, meson.sh, baryon.sh 
     
# 

def main():
    with open(os.path.join(INFILES, 'a065m300.yml')) as f:
        dataMap = yaml.safe_load(f)
    expected_keys = RunJobs.model_fields.keys()
    runjobs = {k: v for k, v in dataMap.items() if k in expected_keys}
    print(runjobs)

    # distillation basis/eigensystem creation 
    if runjobs['run_eigs']:
        print('eigendoit!')
        runpath= os.cwd/tag/cfg_{cfg}
        os.makedirs(runpath,exist_ok=True)
        # now grab the shell scripts and start doing work...
        print('starting config f"{i}"')
        eigs=f"chroma_eigs_{i}.sh"
        subprocess.call(shlex.split(f"chroma_eigs_{i}.sh"))

    
        output=f"{runjobs['runpath']}"/eigs.out
        if os.stat(output).st_size != 0:
            print('CHROMA ran successfully ')

        if options.transfer_back:

        if options.delete:
             


            
                
            
            
            
            
            
        




