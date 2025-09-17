import os
import subprocess
from time import sleep

chunk_size=25
maquina='1-1'
number_jobs=1

def check(): # Serve pra ver se o job ainda ta rodando
    result = subprocess.run("qstat | grep ph4581", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        return True
    return False

#Pegar os ids da gpu e mig do txt
with open(f'../id_mig/id_mig_{maquina}.txt') as f:
    linhas = [line.rstrip() for line in f]

tamanho_mig = linhas[0]
gpu_id = linhas[1]
devices = linhas[2:]


# devices = [ # id dos migs
# 'MIG-365f9ce1-c091-57a7-8ef3-4cbb45dcca47',
# 'MIG-40144944-d4a9-585d-978e-1ace55172139',
# 'MIG-0ebc0c9f-adc4-59a6-af10-200d49046bb5',
# 'MIG-effedeec-21b5-5ad2-904d-f4d06708ac4d'
# ]

#gpu_id = "GPU-fd7e14c3-91ce-6c4b-e736-393c0d0537ef" # ID da gpu completa

#maquina = '1-1' # maquina que vai executar os jobs, pode ser 1-0 ou 1-1
#tamanho_mig = '1g-20gb' # perfil do mig

# cria as pastas caso não existam. Essa sequencia ficou meio ruim, mas da pra usar sem problema
try:
    os.system(f'mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/compute-{maquina}/{tamanho_mig} -p')
    os.system(f'mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/compute-{maquina}/gpu -p')
except:
    pass

for i in range(1,number_jobs):
    roteiro = f'''
#!/bin/bash
#----------------------------------------------------------
# Job name
#PBS -N test

# Name of stdout output file
#PBS -o /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/saidas_out
#PBS -e /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/saidas_err
# Total number of nodes and MPI tasks/node requested
#PBS -l nodes=compute-{maquina}:ppn=4

# Run time (hh:mm:ss) - 20 min
#PBS -l walltime= 00:20:00
#----------------------------------------------------------

# Change to submission directory
cd $PBS_O_WORKDIR

cat $PBS_NODEFILE

# Launch MPI-based executable
time CUDA_VISIBLE_DEVICES={devices[0]} ## >> /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/compute-{maquina}/{tamanho_mig}/mig-{devices[0]}-{chunk_size} &

pid1=$!

time CUDA_VISIBLE_DEVICES={devices[1]} ## >> /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/compute-{maquina}/{tamanho_mig}/mig-{devices[1]}-{chunk_size} &

pid2=$!

time CUDA_VISIBLE_DEVICES={devices[2]} ## >> /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/compute-{maquina}/{tamanho_mig}/mig-{devices[2]}-{chunk_size} &

pid3=$!

time CUDA_VISIBLE_DEVICES={devices[3]} ## >> /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/compute-{maquina}/{tamanho_mig}/mig-{devices[3]}-{chunk_size} &

pid4=$!

wait $pid1 $pid2 $pid3 $pid4

'''
        
        # No script original (me refiro à primeira execução desse script), havia linhas antes de `sleep 60` que executavam, sequencialmente na GPU inteira,
        # o mesmo número de jobs que estão sendo executados em paralelo nos migs (exemplo: 4 migs, 1 job pra cada mig e 4 pra GPU completa)
         
    with open('/home/ph4581/scripts2025_pedroh/scripts/roteiro', 'w') as roteiro_file: # escreve o roteiro
            roteiro_file.write(roteiro)

        # envia o job no roteiro
    os.system('qsub home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/roteiro')


        # confere se o job ainda ta rodando
    while check():
           sleep(60)
