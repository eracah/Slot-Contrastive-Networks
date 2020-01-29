#!/bin/bash


#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH -c 6
#SBATXH -x rtx6
#SBATCH --time=16:00:00
#SBATCH -o /network/tmp1/racaheva/coors/slurm_stdout/slurm-%j.out  # Write the log on tmp1
#SBATCH -e /network/tmp1/racaheva/coors/slurm_stdout/slurm-%j.out
#SBATCH --partition=unkillable                      # Ask for unkillable job
# 1. Load your environment
# conda activate <env_name>

# 2. Copy your dataset on the compute node
#cp /network/data/<dataset> $SLURM_TMPDIR

# 3. Launch your job, tell it to save the model in $SLURM_TMPDIR
#    and look for the dataset into $SLURM_TMPDIR
python train.py $@ --run-dir $SLURM_TMPDIR --final-dir /network/tmp1/racaheva/coors/wandb
cp -r  $SLURM_TMPDIR/wandb/* /network/tmp1/racaheva/coors/wandb
for arg in "$@"
do
    if [ "$arg" != "--eval_args" ]
    then
      shift
    else
      shift
      echo $@
      break
    fi
done
python eval.py $@ --run-dir $SLURM_TMPDIR/eval_runs --train-run-dir $SLURM_TMPDIR/wandb
cp -r  $SLURM_TMPDIR/eval_runs/wandb/* /network/tmp1/racaheva/coors/wandb
