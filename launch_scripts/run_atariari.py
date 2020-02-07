import subprocess
import sys
import argparse
import os
print(os.getcwd())
parser = argparse.ArgumentParser()
parser.add_argument("--unkillable", action='store_true', default=False)
parser.add_argument("--regime", type=str, default="stdim", choices=["stdim", "cswm"],
                    help="whether to use the encoder and dataloader from stdim or from cswm")
parser.add_argument("--base-cmd", type=str, default="sbatch", choices=["sbatch", "bash"])
parser.add_argument('--method', type=str, default='scn', help='Method to use for training representations (default: scn')
args = parser.parse_args()
base_cmd = args.base_cmd
if args.unkillable:
    file = "unkillable_mila_cluster.sl"
else:
    file = "mila_cluster.sl"
ss= "launch_scripts/" + file

# module = "scripts.run_probe"
run_args = [base_cmd, ss]
#run_args.extend(sys.argv[1:])

envs = ['asteroids',
'berzerk',
'bowling',
'boxing',
'breakout',
'demon_attack',
'freeway',
'frostbite',
'hero',
'montezuma_revenge',
'ms_pacman',
'pitfall',
'pong',
'private_eye',
'qbert',
'riverraid',
'seaquest',
'space_invaders',
'tennis',
'venture',
'video_pinball',
'yars_revenge']

envs = ['pong', 'space_invaders', 'ms_pacman']


suffix = "NoFrameskip-v4"
for i,env in enumerate(envs):

    names = env.split("_")
    name = "".join([s.capitalize() for s in names])
    sargs = run_args + ["--env-name"]

    sargs.append(name + suffix)

    sargs.extend(["--wandb-proj", "coors-production"])
    if args.regime == "stdim":
        sargs.extend(["--regime", "stdim", "--color",  "--lr",  "3e-4",  "--num-frames", "100000", "--batch-size", "128", "--epochs", "100"])
        if args.method == "stdim":
            sargs.extend(['--embedding-dim', '256'])
        else:
            sargs.extend(['--embedding-dim', '32', "--num-slots", "8"])

    elif args.regime == "cswm":
        sargs.extend(['--regime', 'cswm', "--color", '--num-episodes', '1000', '--embedding-dim', '4', '--action-dim', '6', '--num-slots', '3',
         '--copy-action', '--epochs', '200',"--noop-max", "0", "--num-frame-stack", "2", "--screen-size", "50", "50", '--frameskip', '4',
                      '--hidden-dim', '512', '--lr', '5e-4', '--batch-size', '1024'])
        if env in ["space_invaders", "pong"]:
            sargs.extend(["--num-slots", "3"])
            if env == "pong":
                sargs.extend([ "--max-episode-steps", "11", '--crop', '35', '190'])
                #"--crop", "35", "190", "--warmstart", "58",
            else:
                sargs.extend(["--max-episode-steps", "11", "--crop", '30', '200'])
                #"--crop", "30", "200", "--warmstart", "50",
        else:
            sargs.extend(["--num-slots", "5", "--max-episode-steps", "65"])


    sargs.extend(["--method", args.method])

    print(" ".join(sargs))
    subprocess.run(sargs)
