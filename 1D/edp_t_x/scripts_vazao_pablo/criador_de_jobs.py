import argparse
import os
from time import time

# exemplo: python criador_de_jobs.py MIG-effedeec-21b5-5ad2-904d-f4d06708ac4d
parser = argparse.ArgumentParser(description='Executa o teste de corrida em uma GPU')
parser.add_argument('maquina', type=str, help='numeração da maquina (1.0, 1.1)')
parser.add_argument('tamanho_mig', type=str, help='tamanho do mig (ex: 1g.20gb. Precisa ser o tamanho exato)')
args = parser.parse_args()

maquina = args.maquina # maquina que vai executar os jobs, pode ser 1-0 ou 1-1
tamanho_mig = args.tamanho_mig # perfil do mig
mig_ou_gpu = 'mig'

num_exec = 168
devices = [ # id dos migs
'MIG-1863a8f0-4adf-5c21-b055-78502a027492',
'MIG-f12323e9-adaa-5033-8f30-912a1adbfa59'
]

benchmarks = ['bt.C','cg.C','ep.C','ft.C','is.C','lu.C','mg.C','sp.C']


for benchmark in benchmarks:
    inicio = time()
    for i in range(0,num_exec/len(devices)):
        
        with open('/home/pabloh/2025/scripts/mig', 'w+') as mig_script: # escreve o conteúdo do arquivo './mig' que é o que ta sendo executado dentro do roteiro
            mig_script.write(f'/home/pabloh/NPB-GPU/CUDA/bin/{benchmark}')

        roteiro = f'''
#!/bin/bash

time CUDA_VISIBLE_DEVICES={devices[0]} ./mig >> /home/pabloh/2025/saidas/compute-{maquina}/{tamanho_mig}/{benchmark.replace('.C','')}/{mig_ou_gpu}-{benchmark.replace('.C','')}-{devices[0]}-{i} &
pid1=$!
time CUDA_VISIBLE_DEVICES={devices[1]} ./mig >> /home/pabloh/2025/saidas/compute-{maquina}/{tamanho_mig}/{benchmark.replace('.C','')}/{mig_ou_gpu}-{benchmark.replace('.C','')}-{devices[1]}-{i} &
pid2=$!

wait $pid1
wait $pid2
        '''


        with open('/home/pabloh/2025/scripts/roteiro_secundario','w+') as roteiro_file: # escreve o roteiro
            roteiro_file.write(roteiro)

#	with open("/home/pabloh/2025/scripts/log.txt", "w+") as log:
#	    log.write(f'iniciado -> {i}')

        os.system('sh /home/pabloh/2025/scripts/roteiro_secundario')

#        while 'pabloh' in subprocess.getoutput('qstat | grep -i pabloh'):
#            sleep(0.5)
    fim = time()

    with open(f'/home/pabloh/2025/saidas/compute-{maquina}/{mig_ou_gpu}/tempo_de_fila_168/{len(devices)}_{benchmark.replace(".C","")}.txt', 'w') as tempo_file:
        tempo_file.write(f'{(fim-inicio):.2f}')


