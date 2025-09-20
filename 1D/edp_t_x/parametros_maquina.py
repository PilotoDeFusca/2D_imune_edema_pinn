gpu_id="GPU-49723f5b-3680-6d21-0357-4b7bf88ad0e7"

v_gpu = [
    "MIG-7fce5663-3a1e-514f-a938-af77e5766e80"
    ]

#ver se mig esta funcionando

numero_nucleos_gpu="128"

numero_nucleos_mig="128"

tempo_execução_mig="04:00:00"
tempo_execução_gpu="04:00:00"

n_hd_layers = [6]

betas1 =[0.6,0.9]

betas2 =[0.99,0.9999]

iter=4

# id dos migs
devices = [ 
 'MIG-1863a8f0-4adf-5c21-b055-78502a027492',
 'MIG-f12323e9-adaa-5033-8f30-912a1adbfa59',
]

gpu_id = "GPU-fd7e14c3-91ce-6c4b-e736-393c0d0537ef" # ID da gpu completa

maquina = '1-0' # maquina que vai executar os jobs, pode ser 1-0 ou 1-1
tamanho_mig = '3g-40gb' # perfil do mig