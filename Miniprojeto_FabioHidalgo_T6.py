import pandas as pd
import numpy as np

# =============================================================================
# SPRINT 1 - IMPORTAÇÃO DOS DADOS
# =============================================================================
# A base foi baixada do Kaggle (link no README) e está no diretório do projeto.
# O separador do CSV é ";" (padrão brasileiro), por isso é preciso informar
# esse parâmetro para o pandas não juntar todas as colunas em uma só.


df = pd.read_csv('Base_Varejo.csv', sep=';', encoding='utf-8')


print(f"Número de registros (linhas): {df.shape[0]}")
print(f"Número de colunas: {df.shape[1]}")
print("\nColunas e tipos de dados originais:")
print(df.dtypes)
print("\nAmostra dos dados:")
print(df.head())


# =============================================================================
# SPRINT 2/3 - VERIFICAÇÃO DE QUALIDADE (antes de limpar)
# =============================================================================


# 2.1 Colunas totalmente vazias (o CSV tem ";" sobrando no final de cada linha,
# o que o pandas interpreta como colunas extras "Unnamed: 10..13", 100% nulas)
colunas_vazias = [c for c in df.columns if df[c].isnull().all()]
print(f"Colunas 100% vazias encontradas (sujeira de exportação do CSV): {colunas_vazias}")

# 2.2 Valores nulos por coluna
print("\nValores nulos por coluna:")
print(df.isnull().sum())

# 2.3 Linhas duplicadas (registro idêntico em todas as colunas)
qtd_duplicadas = df.duplicated().sum()
print(f"\nLinhas totalmente duplicadas: {qtd_duplicadas}")

# 2.4 Inconsistências de categoria: na base Varejo, categoria ausente vem
# como a string "#N/D" em vez de nulo tradicional -> precisa ser tratado.
qtd_nd = (df["PR_CAT"] == "#N/D").sum()
print(f"\nRegistros com categoria ausente ('#N/D'): {qtd_nd}")
print("Distribuição de categorias (PR_CAT):")
print(df["PR_CAT"].value_counts())

# 2.5 Inconsistências de data: DATA está como texto (string), não como data.
# Verificamos se existe alguma data que não segue o padrão dd/mm/aaaa.
datas_teste = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")
qtd_datas_invalidas = datas_teste.isnull().sum()
print(f"\nDatas em formato inválido (não convertidas): {qtd_datas_invalidas}")
print(f"Período coberto pela base: {datas_teste.min().date()} até {datas_teste.max().date()}")
