#!/bin/bash -l
#SBATCH --partition=workq      # Default queue with time limit 1 day.
#SBATCH --ntasks=251           # Number of MPI tasks.
#SBATCH --hint=nomultithread   # Avoid hyperthreading.
#SBATCH --time=00-24:00        # Time limit in DD-HH:MM format.
#SBATCH --job-name=bif0160
#SBATCH --output=%J.out        # File to which stdout will be written.
#SBATCH --error=%J.err         # File to which stderr will be written.
#SBATCH --mail-type=ALL,TIME_LIMIT
#SBATCH --mail-user=dmitry.kabanov@kaust.edu.sa
module load python/3.6.4

# Add solver's code to PYTHONPATH such that Python can find it.
export PYTHONPATH=code:$PYTHONPATH

# Set Matplotlib's backend to Agg to avoid errors on compute nodes without X.
export MPLBACKEND=Agg

srun python run.py 160
