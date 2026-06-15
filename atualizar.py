import pandas as pd

try:
    # 1. Carregar os dados (ajustado para os nomes exatos dos seus arquivos)
    df_discos = pd.read_csv('Tabela_Discos.csv')
    df_sessoes = pd.read_csv('Tabela_Sessoes.csv')

    # Limpeza preventiva: remove espaços em branco nos nomes das colunas e nos dados
    df_discos.columns = df_discos.columns.str.strip()
    df_sessoes.columns = df_sessoes.columns.str.strip()
    df_discos['DISCO'] = df_discos['DISCO'].str.strip()
    df_sessoes['DISCO'] = df_sessoes['DISCO'].str.strip()

    detalhes_discos = []

    for disco in df_discos['DISCO']:
        # Filtra as sessões para o disco atual (Ex: BKG-0061 tem 4 sessões [2])
        sessoes = df_sessoes[df_sessoes['DISCO'] == disco]
        
        if not sessoes.empty:
            # Concatena COD_SESSAO, TAMANHO e STATUS_NASA (Ex: RD2406,200,RELEASE [2])
            lista = []
            for _, s in sessoes.iterrows():
                lista.append(f"{s['COD_SESSAO']},{s['TAMANHO_SESSAO_GB']},{s['STATUS_NASA']}")
            
            sessoes_detalhadas = "; ".join(lista)
            # Soma o uso total (Ex: UVLBI+86 somará 6700 GB [2])
            uso_total = sessoes['TAMANHO_SESSAO_GB'].sum()
            
            # Define STATUS_NASA como BLOCK se houver qualquer 'HOLD' (Ex: USN-0041 [2])
            status_nasa = 'BLOCK' if any(sessoes['STATUS_NASA'] == 'HOLD') else 'FREE'
        else:
            sessoes_detalhadas = "-"
            uso_total = 0
            status_nasa = 'VAZIO'
            
        detalhes_discos.append({
            'DISCO': disco,
            'SESSÕES_DETALHADAS': sessoes_detalhadas,
            'USO_TOTAL': uso_total, # Vírgula adicionada aqui
            'STATUS_NASA': status_nasa
        })

    # 2. Criar o DataFrame final e mesclar com a capacidade e status físico [1]
    df_processado = pd.DataFrame(detalhes_discos)
    tabela_mestra = pd.merge(
        df_discos[['DISCO', 'CAPACIDADE_TOTAL_GB', 'STATUS_FISICO']], 
        df_processado, 
        on='DISCO'
    )

    # 3. Salvar o arquivo (A linha que gera o CSV)
    tabela_mestra.to_csv('Tabela_Mestra.csv', index=False)
    print("Sucesso: O arquivo 'Tabela_Mestra.csv' foi gerado no seu diretório.")

except FileNotFoundError:
    print("Erro: Verifique se os arquivos 'Tabela_Discos.csv' e 'Tabela_Sessoes.csv' estão na mesma pasta do script.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")