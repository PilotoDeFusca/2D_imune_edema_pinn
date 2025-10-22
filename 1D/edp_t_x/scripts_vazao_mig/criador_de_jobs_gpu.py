import argparse
import os
from time import time
from parametros_maquina import *

# exemplo: python criador_de_jobs.py MIG-effedeec-21b5-5ad2-904d-f4d06708ac4d
parser = argparse.ArgumentParser(description='Executa o teste de corrida em uma GPU')
parser.add_argument('maquina', type=str, help='numeração da maquina (1.0, 1.1)')
parser.add_argument('gpu_id', type=str, help='id da gpu que vai usar')
args = parser.parse_args()

maquina = maquina

device = gpu_id


inicio = time()
for i in range(1,numero_testes_vazao+1):
        
    #with open('/home/pabloh/2025/scripts/mig', 'w+') as mig_script: # escreve o conteúdo do arquivo './mig' que é o que ta sendo executado dentro do roteiro
    #    mig_script.write(f'/home/pabloh/NPB-GPU/CUDA/bin/{benchmark}')

    roteiro = f'''
#!/bin/bash

time CUDA_VISIBLE_DEVICES={device} ./mig >> /home/pabloh/2025/saidas/compute-{maquina}/gpu/{benchmark.replace('.C','')}/gpu-{benchmark.replace('.C','')}-{device}-{i}-0 &
time CUDA_VISIBLE_DEVICES={device} ./mig >> /home/pabloh/2025/saidas/compute-{maquina}/gpu/{benchmark.replace('.C','')}/gpu-{benchmark.replace('.C','')}-{device}-{i}-1 &
time CUDA_VISIBLE_DEVICES={device} ./mig >> /home/pabloh/2025/saidas/compute-{maquina}/gpu/{benchmark.replace('.C','')}/gpu-{benchmark.replace('.C','')}-{device}-{i}-2 &
time CUDA_VISIBLE_DEVICES={device} ./mig >> /home/pabloh/2025/saidas/compute-{maquina}/gpu/{benchmark.replace('.C','')}/gpu-{benchmark.replace('.C','')}-{device}-{i}-3 &
time CUDA_VISIBLE_DEVICES={device} ./mig >> /home/pabloh/2025/saidas/compute-{maquina}/gpu/{benchmark.replace('.C','')}/gpu-{benchmark.replace('.C','')}-{device}-{i}-4 &
time CUDA_VISIBLE_DEVICES={device} ./mig >> /home/pabloh/2025/saidas/compute-{maquina}/gpu/{benchmark.replace('.C','')}/gpu-{benchmark.replace('.C','')}-{device}-{i}-5 &
time CUDA_VISIBLE_DEVICES={device} ./mig >> /home/pabloh/2025/saidas/compute-{maquina}/gpu/{benchmark.replace('.C','')}/gpu-{benchmark.replace('.C','')}-{device}-{i}-6 &
pid1=$!

wait $pid1
        '''


    with open('/home/pabloh/2025/scripts/roteiro_secundario','w+') as roteiro_file: # escreve o roteiro
            roteiro_file.write(roteiro)

#	with open("/home/pabloh/2025/scripts/log.txt", "w+") as log:
#	    log.write(f'iniciado -> {i}')

    os.system('sh /home/pabloh/2025/scripts/roteiro_secundario')

#        while 'pabloh' in subprocess.getoutput('qstat | grep -i pabloh'):
#            sleep(0.5)
fim = time()

with open(f'/home/pabloh/2025/saidas/compute-{maquina}/gpu/tempo_de_fila_100xGPU_{benchmark.replace(".C","")}.txt', 'w') as tempo_file:
        tempo_file.write(f'real {(fim-inicio):.2f}')


