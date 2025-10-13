import pandas as pd
import glob
import re
import os

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

def processar_arquivos_tempo(pasta='.', padrao='*.txt'):
    """
    Processa todos os arquivos de texto na pasta e extrai os tempos reais
    """
    dados = []
    path="saidas/"
    #dispositivo='3g/40gb'
    with os.scandir(path) as dispositivos:
        print(dispositivos)
        for dispositivo in dispositivos:
            print(dispositivo)
        # Encontra todos os arquivos que correspondem ao padrão
            caminhos_arquivos = glob.glob(os.path.join(path+dispositivo.name, padrao))
            print(path+dispositivo.name)
    
            for caminho_arquivo in caminhos_arquivos:
                try:
                    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                        conteudo = arquivo.read()
                    
                    tempo_segundos = extrair_tempo_real(conteudo)
                    nome_arquivo = os.path.basename(caminho_arquivo)
                    
                    if tempo_segundos is not None:
                        # Converte para minutos para facilitar leitura
                        tempo_minutos = tempo_segundos / 60
                        
                        dados.append({
                            'Arquivo': nome_arquivo,
                            'Dispositivo' : dispositivo,
                            'Tempo_Real_Segundos': tempo_segundos,
                            'Tempo_Real_Formatado': f"{int(tempo_segundos // 60)}m{tempo_segundos % 60:.3f}s"
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
    
    # Ordena por tempo (do menor para o maior)
    #df = df.sort_values('Arquivo')
    
    # Adiciona uma coluna de ranking
    df['Tempo'] = range(1, len(df) + 1)
    
    # Reorganiza as colunas
    colunas = ['Arquivo', 'Tempo','Dispositivo','Tempo_Real_Segundos', 'Tempo_Real_Formatado']
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
        print(f"\nEstatísticas:")
        print(f"Total de arquivos processados: {len(df_tempos)}")
        #print(f"Tempo médio: {df_tempos['Tempo_Real_Minutos'].mean():.2f} minutos")
        #print(f"Tempo mínimo: {df_tempos['Tempo_Real_Minutos'].min():.2f} minutos")
        #print(f"Tempo máximo: {df_tempos['Tempo_Real_Minutos'].max():.2f} minutos")
        
        # Salva em CSV (opcional)
        #df_tempos.to_csv('tempos_processados.csv', index=False)
        #print(f"\nDados salvos em 'tempos_processados.csv'")