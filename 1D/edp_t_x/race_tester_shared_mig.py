import os
import subprocess
from time import sleep
from parametros_maquina import *

for i in range(1,iter+1):

# cria as pastas caso não existam. Essa sequencia ficou meio ruim, mas da pra usar sem problema
    try:
        os.system(f'mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/lixeira/{tamanho_mig}_shared -p')
        os.system(f'mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/{tamanho_mig}_shared -p')
        os.system('mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs -p')
    except:
        pass

    roteiro = f'''
#!/bin/bash
#----------------------------------------------------------
# Job name
#PBS -N race_tester_mig{i}

# Name of stdout output file
#PBS -o /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/lixeira/{tamanho_mig}_shared/saida{i}.o
#PBS -e /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/{tamanho_mig}_shared/tempo{i}.txt
# Total number of nodes and MPI tasks/node requested
#PBS -l nodes=compute-{maquina}:ppn={numero_nucleos}

# Run time (hh:mm:ss) - 2h
#PBS -l walltime={tempo_execução}
#----------------------------------------------------------

# Change to submission directory
cd $PBS_O_WORKDIR

cat $PBS_NODEFILE

# Launch MPI-based executable
'''
    with open(f'/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro{i}.job', 'w') as roteiro_file: # escreve o roteiro
                    roteiro_file.write(roteiro)
    
    add_wait='\nwait'
    for index, mig in enumerate(devices):
        add_mig=f'''
time CUDA_VISIBLE_DEVICES={mig} \
/home/thiago.esterci/.conda/envs/torch-numba-11/bin/python3 pinn_training.py \
-a __64__64__64__64__64__64 \
-b1 {beta1} \
-b2 {beta2} &

pid{index}=$!
'''

        with open(f'/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro{i}.job', 'a') as roteiro_file:
              roteiro_file.write(add_mig)
        
        add_wait+=f' $pid{index}'
    with open(f'/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro{i}.job', 'a') as roteiro_file:
        roteiro_file.write(add_wait)

    # envia o job no roteiro
    os.system(f'qsub /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro{i}.job')
