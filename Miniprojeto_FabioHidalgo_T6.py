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
# =============================================================================
# SPRINT 2/3 - LIMPEZA DOS DADOS (3 etapas mínimas exigidas)
# =============================================================================

#("3. LIMPEZA DA BASE")

df_limpo = df.copy()

# --- Limpeza 1: remover colunas totalmente vazias -----------------------
# Escolha: REMOVER (não faz sentido imputar uma coluna sem nenhum dado;
# ela é apenas resíduo dos ";" finais de cada linha do CSV original).
df_limpo = df_limpo.drop(columns=colunas_vazias)
print(f"[OK] Removidas {len(colunas_vazias)} colunas 100% vazias: {colunas_vazias}")

# --- Limpeza 2: tratar categoria ausente ("#N/D") ------------------------
# Escolha: IMPUTAR (não remover), pois o item comprado continua sendo uma
# informação válida de venda; perder a linha jogaria fora vendas reais.
# Regra de negócio se/senão: se a categoria for "#N/D", vira "Sem Categoria".
if "PR_CAT" in df_limpo.columns:
    df_limpo["PR_CAT"] = df_limpo["PR_CAT"].apply(
        lambda cat: "Sem Categoria" if cat == "#N/D" else cat
    )
print("[OK] Categorias '#N/D' substituídas por 'Sem Categoria' "
      f"({qtd_nd} registros afetados).")

# --- Limpeza 3: remover duplicatas relevantes ----------------------------
# Escolha: REMOVER. Uma linha duplicada em TODAS as colunas (mesma compra,
# mesmo cliente, mesmo produto, mesma data) representa o mesmo item sendo
# contado duas vezes, o que distorce contagens e estatísticas de vendas.
qtd_antes = len(df_limpo)
df_limpo = df_limpo.drop_duplicates()
qtd_depois = len(df_limpo)
print(f"[OK] Duplicatas removidas: {qtd_antes - qtd_depois} "
      f"(de {qtd_antes} para {qtd_depois} linhas).")

# --- Ajuste de tipos: converter DATA (string) para datetime --------------
df_limpo["DATA"] = pd.to_datetime(df_limpo["DATA"], format="%d/%m/%Y")
print("[OK] Coluna DATA convertida de texto (string) para datetime.")

print("\nTipos de dados após a limpeza:")
print(df_limpo.dtypes)
# =============================================================================
# 4. REGRA DE NEGÓCIO: CO_ID identifica a COMPRA, não a linha
# =============================================================================
# Cada linha da base é um ITEM comprado. Várias linhas com o mesmo CO_ID
# formam UMA compra (carrinho). Validamos essa regra e usamos CO_ID para
# agrupar itens de uma mesma compra quando necessário.

#("4. VALIDAÇÃO DO IDENTIFICADOR DE COMPRA (CO_ID)")

itens_por_compra = df_limpo.groupby("CO_ID").size()
print(f"Total de compras (CO_ID distintos): {df_limpo['CO_ID'].nunique()}")
print(f"Total de itens (linhas) na base limpa: {len(df_limpo)}")
print(f"Média de itens por compra: {itens_por_compra.mean():.2f}")
print(f"Compra com mais itens: CO_ID {itens_por_compra.idxmax()} "
      f"({itens_por_compra.max()} itens)")
print(f"Compra com menos itens: CO_ID {itens_por_compra.idxmin()} "
      f"({itens_por_compra.min()} itens)")
# =============================================================================
# 5. ESTATÍSTICA DESCRITIVA - Número de filhos do cliente (CL_FHL)
# =============================================================================

#("5. ESTATÍSTICA DESCRITIVA - Número de filhos do cliente (CL_FHL)")

# Como cada cliente aparece várias vezes (uma vez por item comprado),
# calculamos as estatísticas sobre clientes ÚNICOS, para não inflar os
# resultados com a repetição do mesmo cliente em várias linhas.
clientes_unicos = df_limpo.drop_duplicates(subset="CL_ID")
filhos = clientes_unicos["CL_FHL"]

estat_filhos = {
    "contagem": filhos.count(),
    "média": filhos.mean(),
    "mediana": filhos.median(),
    "desvio_padrão": filhos.std(),
    "moda": filhos.mode().iloc[0],
    "mínimo": filhos.min(),
    "máximo": filhos.max(),
    "quartil_25%": filhos.quantile(0.25),
    "quartil_50%": filhos.quantile(0.50),
    "quartil_75%": filhos.quantile(0.75),
}
for nome, valor in estat_filhos.items():
    print(f"{nome:15s}: {valor:.2f}" if isinstance(valor, float) else f"{nome:15s}: {valor}")
# =============================================================================
# 6. PADRÕES DE AGRUPAMENTO (2 combinações, groupby / pivot_table)
# =============================================================================

#("6. AGRUPAMENTO 1 - Vendas (itens) por gênero e categoria de produto")

agrup_genero_categoria = df_limpo.pivot_table(
    index="CL_GENERO",
    columns="PR_CAT",
    values="PR_ID",
    aggfunc="count",
    fill_value=0,
)
print(agrup_genero_categoria)

#("6. AGRUPAMENTO 2 - Vendas (itens) por mês e segmento de cliente (CL_SEG)")

df_limpo["ANO_MES"] = df_limpo["DATA"].dt.to_period("M")
agrup_mes_segmento = df_limpo.groupby(["ANO_MES", "CL_SEG"]).size().unstack(fill_value=0)
print(agrup_mes_segmento)

#("6. AGRUPAMENTO 3 (extra) - Top 10 produtos mais vendidos por categoria")

top_produtos = (
    df_limpo.groupby(["PR_CAT", "PR_NOME"])
    .size()
    .reset_index(name="qtd_itens")
    .sort_values("qtd_itens", ascending=False)
    .head(10)
)
print(top_produtos.to_string(index=False))
# =============================================================================
# 7. CONCLUSÕES / INSIGHTS
# =============================================================================

#("7. CONCLUSÕES E INSIGHTS")

categoria_top = df_limpo["PR_CAT"].value_counts().idxmax()
genero_top = df_limpo["CL_GENERO"].value_counts().idxmax()
mes_top = df_limpo.groupby("ANO_MES").size().idxmax()

conclusoes = [
    f"1. A base contém {df_limpo['CO_ID'].nunique()} compras distintas, totalizando "
    f"{len(df_limpo)} itens vendidos após a limpeza (foram removidas "
    f"{qtd_antes - qtd_depois} linhas duplicadas).",

    f"2. A categoria de produto mais vendida é '{categoria_top}', concentrando a "
    "maior parte do volume de itens da base.",

    f"3. O gênero '{genero_top}' concentra a maior parte das compras registradas, "
    "o que pode orientar campanhas e sortimento de produtos.",

    f"4. O mês com maior volume de vendas foi {mes_top}, indicando possível "
    "sazonalidade no comportamento de compra.",

    f"5. Em média, os clientes têm {estat_filhos['média']:.1f} filhos (mediana "
    f"{estat_filhos['mediana']:.0f}), com desvio padrão de "
    f"{estat_filhos['desvio_padrão']:.2f}, mostrando um perfil familiar "
    "relativamente homogêneo na base de clientes.",

    f"6. Ainda restam {qtd_nd} itens que tinham categoria original ausente "
    "('Sem Categoria' após o tratamento) - vale investigar a origem desses "
    "registros no sistema de origem para evitar o problema em cargas futuras.",
]
for c in conclusoes:
    print(c)
