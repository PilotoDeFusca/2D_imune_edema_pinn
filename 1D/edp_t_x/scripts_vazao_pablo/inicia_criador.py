import os

tamanho_mig = '3g.40gb'
maquina = '1-0' # maquina que vai executar os jobs, pode ser 1-0 ou 1-1
gpu_id = 'GPU-8c36d9dd-4315-583f-c95d-c0e7575f3433'

benchmarks = ['bt.C','cg.C','ep.C','ft.C','is.C','lu.C','mg.C','sp.C']

for benchmark in benchmarks: # cria as pastas caso não existam. Essa sequencia ficou meio ruim, mas da pra usar sem problema
    try:
        os.system(f'mkdir /home/pabloh/2025/saidas/compute-{maquina}/{tamanho_mig}/{benchmark.replace(".C","")}/ -p')
        os.system(f'mkdir /home/pabloh/2025/saidas/compute-{maquina}/gpu/{benchmark.replace(".C","")}/ -p')
    except:
        pass


roteiro = f'''
#!/bin/bash
#----------------------------------------------------------
# Job name
#PBS -N mig_test_1.0

# Name of stdout output file
#PBS -o /home/pabloh/2025/saidas/lixeira/out/
#PBS -e /home/pabloh/2025/saidas/lixeira/err/
# Total number of nodes and MPI tasks/node requested
#PBS -l nodes=compute-{maquina}:ppn=128

# Run time (hh:mm:ss) - 1.5 hours
#PBS -l walltime=06:30:00
#----------------------------------------------------------

# Change to submission directory
cd $PBS_O_WORKDIR

cat $PBS_NODEFILE

# Launch MPI-based executable
python3 /home/pabloh/2025/scripts/criador_de_jobs.py {maquina} {tamanho_mig}
pid=$!
wait pid
'''

with open('roteiro','w+') as roteiro_file: # escreve o roteiro
    roteiro_file.write(roteiro)

os.system('qsub roteiro')
print('iniciado')
