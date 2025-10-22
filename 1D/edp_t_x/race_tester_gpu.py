import os
import subprocess
from time import sleep
from parametros_maquina import *

for i in range(1,iter+1):

# cria as pastas caso não existam
    try:
        os.system(f'mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/lixeira/gpu -p')
        os.system(f'mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/gpu -p')
        os.system('mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs -p')
    except:
        pass

    roteiro = f'''
#!/bin/bash
#----------------------------------------------------------
# Job name
#PBS -N race_tester_gpu{i}

# Name of stdout output file
#PBS -o /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/lixeira/gpu/saida{i}.o
#PBS -e /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/gpu/tempo{i}.txt
# Total number of nodes and MPI tasks/node requested
#PBS -l nodes=compute-1-1:ppn=128

# Run time (hh:mm:ss) - 2h
#PBS -l walltime=02:00:00
#----------------------------------------------------------

# Change to submission directory
cd $PBS_O_WORKDIR

cat $PBS_NODEFILE

# Launch MPI-based executable
time CUDA_VISIBLE_DEVICES=GPU-fd7e14c3-91ce-6c4b-e736-393c0d0537ef \
/home/thiago.esterci/.conda/envs/torch-numba-11/bin/python3 pinn_training.py \
-a __64__64__64__64__64__64 \
-b1 {beta1} \
-b2 {beta2}
'''     
    # escreve o roteiro
    with open(f'/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro{i}.job', 'w') as roteiro_file:
        roteiro_file.write(roteiro)

    # envia o job no roteiro
    os.system(f'qsub /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro{i}.job')