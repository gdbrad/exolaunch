#!/bin/bash
# template for computing distillation basis with chroma 

#SBATCH --nodes=2 
#SBATCH --ntasks-per-node=4 
#SBATCH --partition=dc-gpu
#SBATCH --gpu-bind=none
#SBATCH --account=exotichadrons
#SBATCH -t 400
#SBATCH --gres=gpu:4
#SBATCH -o /p/scratch/exotichadrons/exolauncher/res/eigs770.out

CODE_DIR=/p/scratch/exotichadrons/pederiva/chroma-distillation
source $CODE_DIR/install-scripts/machines/env-new-jureca-gpu.sh
chroma=$CODE_DIR/install/chroma/bin/chroma

export OPENBLAS_NUM_THREADS=4
export OMP_NUM_THREADS=4
export CUDA_VISIBLE_DEVICES=0,1,2,3

BASE_DIR=/p/scratch/exotichadrons/exolauncher/res
log=$BASE_DIR/log/eigs/eigs_770.log
in=$BASE_DIR/xml/eigs/eigs_770.ini.xml
out=$BASE_DIR/out/eigs/eigs_770.out.xml

output="$BASE_DIR/eigs.out"
export OPTS=" -geom 1 2 2 2"
echo "START  "$(date "+%Y-%m-%dT%H:%M")
srun -n 8 -c 16 $chroma $OPTS -i $in -o $out -l $log > $output 2>&1
echo "FINISH JOB "$(date "+%Y-%m-%dT%H:%M")
echo "you should move this to metaq dir!" 