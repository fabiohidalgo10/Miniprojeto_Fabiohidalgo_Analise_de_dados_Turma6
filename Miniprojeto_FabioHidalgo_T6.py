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

