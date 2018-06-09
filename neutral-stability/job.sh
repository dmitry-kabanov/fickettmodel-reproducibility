#!/bin/bash -l
#SBATCH --partition=workq
#SBATCH --ntasks=256           # Number of MPI tasks.
#SBATCH --hint=nomultithread   # Avoid hyperthreading.
#SBATCH --time=00-10:00        # Time limit in DD-HH:MM format.
#SBATCH --job-name=neutral-stability
#SBATCH --output=%J.out        # File to which stdout will be written.
#SBATCH --error=%J.err         # File to which stderr will be written.
module load python/3.6.4

# Add solver's code to PYTHONPATH such that Python can find it.
export PYTHONPATH=code:

srun python run.py
echo 'Job completed'
