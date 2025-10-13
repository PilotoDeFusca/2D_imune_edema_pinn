import os
import glob
import re
import pandas as pd

def extrair_tempo_real(conteudo):
    """
    Extrai o tempo real do conteúdo do arquivo
    Retorna em segundos
    """
    # Procura pela linha que começa com "real"
    padrao = r'real\s+(\d+)m([\d.]+)s'
    match = re.search(padrao, conteudo)
    
    if match:
        minutos = int(match.group(1))
        segundos = float(match.group(2))
        return minutos * 60 + segundos
    else:
        return None

def processar_arquivos_tempo():
    dados=[]
    for dispositivo in os.scandir('saidas'):
            print(dispositivo.name)
            path='saidas/'+dispositivo.name
        # Encontra todos os arquivos que correspondem ao padrão
            caminhos_arquivos = glob.glob(os.path.join(path, "*.txt"))
            #print(path)
            #print(caminhos_arquivos)
            for index,caminho_arquivo in enumerate(caminhos_arquivos):
                try:
                    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                        conteudo = arquivo.read()
                        #print(conteudo)
                    
                        tempo_segundos = extrair_tempo_real(conteudo)
                        nome_arquivo = os.path.basename(caminho_arquivo)
                    
                        if tempo_segundos is not None:
                        
                            dados.append({
                            'Arquivo': nome_arquivo,
                            'Tempo': (index%10)+1,
                            'Dispositivo' : dispositivo.name,
                            'Tempo_Segundos': tempo_segundos,
                            'Tempo_Formatado': f"{int(tempo_segundos // 60)}m{tempo_segundos % 60:.3f}s"

                        })
                        else:
                            print(f"Aviso: Não foi possível extrair tempo real do arquivo {nome_arquivo}")
                        
                except Exception as e:
                    print(f"Erro ao processar {caminho_arquivo}: {e}")
    return dados

def criar_dataframe(dados):
    """
    Cria um DataFrame pandas com os dados processados
    """
    if not dados:
        print("Nenhum dado foi processado.")
        return None
    
    df = pd.DataFrame(dados)
    
    # Reorganiza as colunas
    colunas = ['Arquivo', 'Tempo','Dispositivo','Tempo_Segundos', 'Tempo_Formatado']
    df = df[colunas]
    
    return df

# Exemplo de uso
if __name__ == "__main__":
    # Processa os arquivos na pasta atual
    dados_processados = processar_arquivos_tempo()
    
    # Cria o DataFrame
    df_tempos = criar_dataframe(dados_processados)
    
    if df_tempos is not None:
        # Exibe a tabela
        print("Tabela de Tempos Reais:")
        print("=" * 80)
        print(df_tempos.to_string(index=False))
        print("\n" + "=" * 80)
        
        # Estatísticas básicas
        print(f"Total de arquivos processados: {len(df_tempos)}")

        
        # Salva em CSV (opcional)
        #df_tempos.to_csv('tempos_processados.csv', index=False)
        #print(f"\nDados salvos em 'tempos_processados.csv'")