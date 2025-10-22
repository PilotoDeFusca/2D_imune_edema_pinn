v_gpu = [
    "MIG-7fce5663-3a1e-514f-a938-af77e5766e80"
    ]

#ver se mig esta funcionando

numero_nucleos="16"

tempo_execução="10:00:00"

n_hd_layers = [6]

n_neurons = [2**6]

beta1 =0.6

beta2 =0.99

iter=10

#3.40
devices = [ 
 'MIG-1863a8f0-4adf-5c21-b055-78502a027492',
 'MIG-f12323e9-adaa-5033-8f30-912a1adbfa59'
]

#devices = ['MIG-7fce5663-3a1e-514f-a938-af77e5766e80'] 4.40

gpu_id = "GPU-fd7e14c3-91ce-6c4b-e736-393c0d0537ef" # ID da gpu completa

maquina = '1-0' # maquina que vai executar os jobs, pode ser 1-0 ou 1-1
tamanho_mig = '3g-40gb' # perfil do mig

numero_testes_vazao=4
exec_per_mig=numero_testes_vazao//len(devices)