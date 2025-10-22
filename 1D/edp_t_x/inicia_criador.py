import os
from parametros_maquina import *



try:
    os.system(f'mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/lixeira/{tamanho_mig}_queue -p')
    os.system(f'mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/{tamanho_mig}_queue -p')
    os.system('mkdir /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs -p')
except:
    pass


roteiro = f'''
#!/bin/bash
#----------------------------------------------------------
# Job name
#PBS -N race_tester_queue_mig

# Name of stdout output file
#PBS -o /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/lixeira/{tamanho_mig}_queue/saida.o
#PBS -e /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/{tamanho_mig}_queue/tempo.txt
# Total number of nodes and MPI tasks/node requested
#PBS -l nodes=compute-{maquina}:ppn={numero_nucleos}

# Run time (hh:mm:ss) -
#PBS -l walltime={tempo_execução}
#----------------------------------------------------------

# Change to submission directory
cd $PBS_O_WORKDIR

cat $PBS_NODEFILE

# Launch MPI-based executable

START_TIME=$(date +%s%3N)
'''

with open(f'/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro_create_queue.job','w+') as roteiro_file: # escreve o roteiro
    roteiro_file.write(roteiro)

add_wait='\nwait'
for index, mig in enumerate(devices):
        
        add_mig=f'''
time CUDA_VISIBLE_DEVICES={mig} \
python3 criador_de_jobs.py {devices[index]} {index} &

pid{index}=$!
'''
        with open(f'/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro_create_queue.job', 'a') as roteiro_file:
              roteiro_file.write(add_mig)
        
        add_wait+=f' $pid{index}'
with open(f'/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro_create_queue.job', 'a') as roteiro_file:
    roteiro_file.write(add_wait)

add_end_time=f'''

END_TIME=$(date +%s%3N)

# Calcular duração total
DURATION=$((END_TIME - START_TIME))

echo $DURATION >> /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/{tamanho_mig}_queue/tempo_queue.txt
'''

with open(f'/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro_create_queue.job', 'a') as roteiro_file:
    roteiro_file.write(add_end_time)

os.system('qsub jobs/roteiro_create_queue.job')
print('iniciado')
