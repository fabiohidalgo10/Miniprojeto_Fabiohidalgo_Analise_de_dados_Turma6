# Análise Exploratória de Dados - Base Varejo

Mini-Projeto Avaliativo - Módulo 1 - Semana 07 - Análise de Dados com Python [T6]
Turma: **Analise_de_Dados_T6**

## 📖 Sobre a análise realizada

Este projeto aplica uma **Análise Exploratória de Dados (AED)** sobre uma base
real de compras de varejo (`Base_Varejo.csv`), contendo registros de itens
comprados por clientes (data, cliente, produto, categoria e características
sociodemográficas). O script (`Miniprojeto_FabioHidalgo_T6.py`) percorre as
seguintes etapas:

1. **Carga e inspeção inicial** — leitura do CSV com `pandas`, verificação do
   número de registros, colunas e tipos de dados.

2. **Diagnóstico de qualidade dos dados** — identificação de:
   - 4 colunas totalmente vazias (resíduo de `;` no final de cada linha do CSV);
   - 96.553 linhas duplicadas;
   - 3.650 itens com categoria de produto ausente (representada pela string `"#N/D"`);
   - a coluna `DATA` armazenada como texto em vez de data.

3. **Limpeza dos dados**, com justificativa para cada decisão:
   - remoção das colunas vazias;
   - substituição de `"#N/D"` por `"Sem Categoria"` (imputação, via `if/else`), preservando o item vendido em vez de descartar a linha;
   - remoção das linhas duplicadas, que inflavam artificialmente as contagens de vendas;
   - conversão da coluna `DATA` para o tipo `datetime`.

4. **Validação de regra de negócio** — confirmação de que cada linha da base
   representa um **item** comprado, e que `CO_ID` identifica a **compra**
   (podendo agrupar vários itens de um mesmo carrinho).

5. **Estatística descritiva** da coluna **número de filhos do cliente**
   (`CL_FHL`): contagem, média, mediana, desvio padrão, moda, mínimo, máximo
   e quartis — calculada sobre clientes únicos, para não repetir o mesmo
   cliente em cada item que ele comprou.

6. **Padrões de agrupamento** (`groupby` / `pivot_table`):
   - itens vendidos por **gênero × categoria de produto**;
   - itens vendidos por **mês × segmento de cliente**;
   - top 10 produtos mais vendidos por categoria (agrupamento extra).

7. **Conclusões** — bloco com os principais insights obtidos (categoria mais
   vendida, gênero predominante, sazonalidade mensal, perfil familiar dos
   clientes e problemas remanescentes na base).

8. **Exportação** da base tratada para `df_limpo.csv`, pronta para alimentar
   uma etapa seguinte de análise ou um dashboard de BI.

Base de dados original (Kaggle):
https://www.kaggle.com/datasets/namespaiva/base-varejo/data

## 🛠️ Tecnologias utilizadas

- **Python 3** — linguagem principal do projeto
- **pandas** — leitura do CSV, limpeza, transformação, estatísticas descritivas e agrupamentos (`groupby`, `pivot_table`)
- **NumPy** — suporte a operações numéricas
- **CSV** (`Base_Varejo.csv`) — formato da base de dados de origem
- **VSCode** ou **Google Colab** — ambientes de execução do script

## ▶️ Como executar o projeto

### Pré-requisitos
- Python 3.9 ou superior
- Biblioteca `pandas` instalada:
  ```
  pip install pandas
  ```

### Opção 1 — VSCode / terminal
1. Coloque o arquivo `Base_Varejo.csv` na mesma pasta do script.
2. Abra o terminal na pasta do projeto.
3. Execute:
   ```
   python Miniprojeto_FabioHidalgo_T6.py
   ```
4. O relatório completo (diagnóstico, limpeza, estatísticas, agrupamentos e
   conclusões) é impresso no terminal, e o arquivo `df_limpo.csv` é gerado
   automaticamente na mesma pasta ao final da execução.

### Opção 2 — Google Colab
1. Faça upload de `Base_Varejo.csv` e de `Miniprojeto_FabioHidalgo_T6.py` para o
   ambiente do Colab (ou cole o conteúdo do `.py` em uma célula).
2. Rode todas as células.

## 🗂️ Estrutura do repositório

```
├── Base_Varejo.csv                  # base original (bruta)
├── Miniprojeto_FabioHidalgo_T6.py      # script da AED (comentado por bloco)
├── df_limpo.csv                     # base já limpa, gerada pelo script
└── README.md                        # este arquivo
```
