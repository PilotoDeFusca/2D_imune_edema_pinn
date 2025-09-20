import os
import subprocess
from time import sleep
from parametros_maquina import *

#Pegar os ids da gpu e mig do txt
#with open(f'../id_mig/id_mig_{maquina}.txt') as f:
#    linhas = [line.rstrip() for line in f]

#tamanho_mig = linhas[0]
#gpu_id = linhas[1]
#devices = linhas[2:]


def check(): # Serve pra ver se o job ainda ta rodando
    result = subprocess.run("qstat | grep ph4581", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        return True
    return False


for beta1 in betas1:
    for beta2 in betas2:
        for i in range(1,iter+1):

# cria as pastas caso não existam. Essa sequencia ficou meio ruim, mas da pra usar sem problema
            try:
                os.system(f'mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/compute-{maquina}/{tamanho_mig}/{beta1}_{beta2} -p')
                os.system(f'mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/compute-{maquina}/gpu/{beta1}_{beta2} -p')
            except:
                pass

            roteiro = f'''
#!/bin/bash
#----------------------------------------------------------
# Job name
#PBS -N race_tester_ph

# Name of stdout output file
#PBS -o /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/saidas_out
#PBS -e /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/saidas_err
# Total number of nodes and MPI tasks/node requested
#PBS -l nodes=compute-{maquina}:ppn={numero_nucleos_mig}

# Run time (hh:mm:ss) - 04 hs
#PBS -l walltime={tempo_execução_mig}
#----------------------------------------------------------

# Change to submission directory
cd $PBS_O_WORKDIR

cat $PBS_NODEFILE

# Launch MPI-based executable
time CUDA_VISIBLE_DEVICES={devices[0]} \
/home/thiago.esterci/.conda/envs/torch-numba-11/bin/python3 pinn_training.py \
-a __64__64__64__64__64__64 \
-b1 {beta1} \
-b2 {beta2} >>\
/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/\
compute-{maquina}/{tamanho_mig}/{beta1}_{beta2}/{i}

'''     
            with open('/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro', 'w') as roteiro_file: # escreve o roteiro
                    roteiro_file.write(roteiro)

                # envia o job no roteiro
            os.system('qsub /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro')


                # confere se o job ainda ta rodando
            while check():
                sleep(60)
