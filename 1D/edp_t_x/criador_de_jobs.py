import argparse
import os
from time import time
from parametros_maquina import *

parser = argparse.ArgumentParser(description='Executa o teste de corrida em uma GPU')
parser.add_argument('id_mig', type=str, help='id do mig que executarão os jobs')
parser.add_argument('device_index', type=int, help='index da lista devices para numerar os resultados')
args = parser.parse_args()

id_mig=args.id_mig
device_index=args.device_index

with open(f'/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/saidas/{tamanho_mig}_queue{device_index}', 'w') as roteiro_file:
        roteiro_file.write('')

for i in range(1,exec_per_mig+1):
    index_job=i+(exec_per_mig*device_index)
        
    add_mig=f'''
time CUDA_VISIBLE_DEVICES={id_mig} \
/home/thiago.esterci/.conda/envs/torch-numba-11/bin/python3 pinn_training.py \
-a __64__64__64__64__64__64 \
-b1 {beta1} \
-b2 {beta2}
'''
    with open(f'/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro_queue{device_index}.job', 'a') as roteiro_file:
        roteiro_file.write(add_mig)
        
#	with open("/home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/log.txt", "w+") as log:
#	    log.write(f'iniciado -> {i*index}')

#os.system('sh /home/ph4581/scripts_thiago/2D_imune_edema_pinn/1D/edp_t_x/jobs/roteiro_queue')

#while 'ph4581' in subprocess.getoutput('qstat | grep -i ph4581'):
#            sleep(0.5)