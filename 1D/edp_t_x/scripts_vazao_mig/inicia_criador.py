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
#PBS -o /home/pabloh/2025/saidas/lixeira/out/
#PBS -e /home/pabloh/2025/saidas/lixeira/err/
# Total number of nodes and MPI tasks/node requested
#PBS -l nodes=compute-{maquina}:ppn={numero_nucleos}

# Run time (hh:mm:ss) - 12 hours
#PBS -l walltime=12:00:00
#----------------------------------------------------------

# Change to submission directory
cd $PBS_O_WORKDIR

cat $PBS_NODEFILE

# Launch MPI-based executable
python3 /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/criador_de_jobs.py {maquina} {tamanho_mig}
pid=$!
wait pid
'''

with open('roteiro','w+') as roteiro_file: # escreve o roteiro
    roteiro_file.write(roteiro)

#os.system('qsub roteiro')
print('iniciado')
