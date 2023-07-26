#!/bin/bash
#SBATCH -C cpu
#SBATCH -q regular
#SBATCH -J Optimization
#SBATCH --mail-user=bens.roy@gmail.com
#SBATCH --mail-type=NONE
#SBATCH -t 12:00:00
#SBATCH --image=balewski/ubu20-neuron8:v5




shifter python3 Na16HMM_Tau.py