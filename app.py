# %%

import numpy as np
import pandas as pd
import streamlit as st
import warnings
import locale

warnings.filterwarnings('ignore')
locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')

st.title("Insghts sobre de medicamentos no Brasil")

# %%

st.markdown("## Sobre a base de dados:")

st.markdown("""
    Os dados sobre medicamentos estaão divididos em duas bases diferentes. Ambas as bases contém quase todas as
    informações sobre os medicamentos mas diferem quando uma base possui os valores de PMC (Preço Máximo de Venda
    ao Consumidor) e a outra base possui ps valores de PMVG (Preço Máximo de Venda ao Governo).
    
    O primeiro passo para realizar o tratamento destes dados é unir ambas estas bases para facilitar qualquer análise.
""")

# %%


def currency(value: float, round_to: int = 2):
    return "R$ " + f'{round(value, round_to):n}'


def thousands(value: float, round_to: int = 0):
    return f'{round(value, round_to):n}'


# %%

df_consumidor = pd.read_csv('TA_PRECO_MEDICAMENTO.CSV', sep=';', encoding='ISO-8859-1')
df_governo = pd.read_csv('TA_PRECO_MEDICAMENTO_GOV.CSV', sep=';', encoding='ISO-8859-1')

# %%

# Limpar Dataframes

df_consumidor = df_consumidor[[
    'SUBSTÂNCIA', 'CNPJ', 'LABORATÓRIO', 'PRODUTO', 'PF Sem Impostos', 'PF 0%', 'PF 12%', 'PF 17%',
    'PF 17% ALC', 'PF 17,5%', 'PF 17,5% ALC', 'PF 18%', 'PF 18% ALC',
    'PF 20%', 'PMC 0%', 'PMC 12%', 'PMC 17%', 'PMC 17% ALC', 'PMC 17,5%',
    'PMC 17,5% ALC', 'PMC 18%', 'PMC 18% ALC', 'PMC 20%'
]]

df_governo = df_governo.rename(columns={'PRINCÍPIO ATIVO': 'SUBSTÂNCIA'})
df_governo = df_governo[[
    'SUBSTÂNCIA', 'CNPJ', 'LABORATÓRIO', 'PRODUTO', 'PF Sem Impostos', 'PF 0%', 'PF 12%', 'PF 17%',
    'PF 17% ALC', 'PF 17,5%', 'PF 17,5% ALC', 'PF 18%', 'PF 18% ALC',
    'PF 20%', 'PMVG Sem Impostos', 'PMVG 0%', 'PMVG 12%', 'PMVG 17%',
    'PMVG 17% ALC', 'PMVG 17,5%', 'PMVG 17,5% ALC', 'PMVG 18%',
    'PMVG 18% ALC', 'PMVG 20%'
]]

# %%

# Juntar Dataframes

df = df_consumidor.merge(df_governo, how='inner', on=[
    'SUBSTÂNCIA', 'CNPJ', 'LABORATÓRIO', 'PRODUTO', 'PF Sem Impostos',
    'PF 0%', 'PF 12%', 'PF 17%', 'PF 17% ALC', 'PF 17,5%', 'PF 17,5% ALC',
    'PF 18%', 'PF 18% ALC', 'PF 20%'
])

del df_consumidor
del df_governo

# %%

# limpeza de dados

df_count_1 = df.shape[0]

df = df.dropna()

df_count_2 = df.shape[0]

df = df.drop_duplicates([
    'SUBSTÂNCIA', 'CNPJ', 'LABORATÓRIO', 'PRODUTO', 'PF Sem Impostos',
    'PF 0%', 'PF 12%', 'PF 17%', 'PF 17% ALC', 'PF 17,5%', 'PF 17,5% ALC',
    'PF 18%', 'PF 18% ALC', 'PF 20%'
]).reset_index(drop=True)

# df.to_csv('./medicamentos-v2.csv')
# df.info()

df_count_3 = df.shape[0]

st.markdown("#### Contagem de produtos:")
col1, col2, col3 = st.columns(3)

col1.metric("Antes da Limpeza", thousands(df_count_1))
col2.metric("Após Limpeza de Nulos", thousands(df_count_2), delta=thousands(df_count_2 - df_count_1))
col3.metric("Após Limpeza de Duplicatas", thousands(df_count_3), delta=thousands(df_count_3 - df_count_2))

st.markdown("""
    O segundo passo é realizar o filtro de impurezas nestas bases. As principais ações de filtragem escolhidas foram:
    remover linhas que não estavam 100% preenchidas e então remover linhas duplicadas que significaram quase 1/5
    da base.
""")

st.markdown("---------------------------")

st.markdown("##### Resumo:")

col1, col2 = st.columns(2)

# Qtd. Laboratórios Diferentes
unique_labs = df['LABORATÓRIO'].nunique()
col1.metric("Qtd. Laboratórios Diferentes", "%s laboratórios" % thousands(unique_labs))

# Qtd. Produtos Diferentes
unique_products = df['PRODUTO'].nunique()
col2.metric("Qtd. Produtos Diferentes", "%s produtos" % thousands(unique_products))


# %%

for column in [
    'PF Sem Impostos', 'PF 0%', 'PF 12%', 'PF 17%', 'PF 17% ALC',
    'PF 17,5%', 'PF 17,5% ALC', 'PF 18%', 'PF 18% ALC', 'PF 20%',
    'PMC 0%', 'PMC 12%', 'PMC 17%', 'PMC 17% ALC', 'PMC 17,5%',
    'PMC 17,5% ALC', 'PMC 18%', 'PMC 18% ALC', 'PMC 20%',
    'PMVG Sem Impostos', 'PMVG 0%', 'PMVG 12%', 'PMVG 17%', 'PMVG 17% ALC',
    'PMVG 17,5%', 'PMVG 17,5% ALC', 'PMVG 18%', 'PMVG 18% ALC', 'PMVG 20%'
]:
    df[column] = df[column].astype(str)
    df[column] = df[column].str.replace(',', '.')
    df[column] = df[column].astype(np.float32)

# %%

df['PF MED'] = df[[
    'PF Sem Impostos', 'PF 0%', 'PF 12%', 'PF 17%', 'PF 17% ALC',
    'PF 17,5%', 'PF 17,5% ALC', 'PF 18%', 'PF 18% ALC', 'PF 20%'
]].mean(axis=1)

df['PMC MED'] = df[[
    'PMC 0%', 'PMC 12%', 'PMC 17%', 'PMC 17% ALC', 'PMC 17,5%',
    'PMC 17,5% ALC', 'PMC 18%', 'PMC 18% ALC', 'PMC 20%',
]].mean(axis=1)

df['PMVG MED'] = df[[
    'PMVG Sem Impostos', 'PMVG 0%', 'PMVG 12%', 'PMVG 17%', 'PMVG 17% ALC',
    'PMVG 17,5%', 'PMVG 17,5% ALC', 'PMVG 18%', 'PMVG 18% ALC', 'PMVG 20%'
]].mean(axis=1)

# df.to_csv('./medicamentos-v3.csv')

# %%

st.markdown("------------------")

pf_mean = df['PF MED'].mean()
pmc_mean = df['PMC MED'].mean()
pmvg_mean = df['PMVG MED'].mean()

st.markdown("#### Medianas: ")
col1, col2, col3 = st.columns(3)

col1.metric("PF | Preço de Fábrica", currency(pf_mean))
col2.metric("PMC | Preço ao Consumidor", currency(pmc_mean), delta=f'{round(((pmc_mean - pf_mean) / pf_mean) * 100):n} %')
col3.metric("PMVG | Preço ao Governo", currency(pmvg_mean), delta=f'{round(((pmvg_mean - pf_mean) / pf_mean) * 100):n} %')

st.markdown("""
    Terceiro passo: Encontrar as medianas de cada valor (PF, PMC e PMVG) e gerar insigts com hipóteses de causas e
    consequências dos dados.
""")

# %%

st.markdown("------------------")

# Diferença mediana entre Preço de Consumidor e Preço para governo
st.markdown("##### Diferença mediana entre Preço de Consumidor e Preço ao governo:")

insight_01 = df['PMC MED'].sub(df['PMVG MED'], axis=0).mean()

col1, col2 = st.columns(2)
col1.metric("PMVG - PMC | Mediano", currency(insight_01))

# O governo paga em média x% a menos em medicamentos em relação ao consumidor
insight_02 = (insight_01 / pmc_mean) * 100
col2.metric("Portentagem da Diferença em Relação ao PMC", f'{round(insight_02):n} %')

st.markdown("""
    Encontrando a diferença mediana entre o PMVG (Preço Máximo de Venda ao Governo) e PMC (Preço máximo de venda ao
    consumidor). Esta diferênça de valores indica o nível de economia do setor público ao comercializar diretamente 
    com laboratórios   
""")

# %%

st.markdown("------------------")
st.markdown("##### Margem de lucro ao vender para consumidores")

insight_03 = df['PMC MED'].sub(df['PF MED'], axis=0).mean()
st.metric("PMC - PF | Mediano", currency(insight_03))

st.markdown("""
    Ao encontrar a mediana da subtração de PF (Preço de Fábrica) e PMC (Preço Máximo de Venda ao Consumidor),
    encontramos o intervalo mínimo que farmácias podem competir por preços ao vender seus produtos. Levando em
    consideração de que tanto PF quanto PMC são valores de teto, é possível que laboratórios e farmácias realizem
    negócios com valores abeixo deste teto.
""")


# %%

# st.markdown("------------------")

# Margem de perda ao vender ao governo
# insight_04 = df['PMVG MED'].sub(df['PF MED'], axis=0).mean()
# st.metric("Margem de perda ao vender ao governo", currency(insight_04))

# %%

st.markdown("------------------")
st.markdown("### Laboratório com Maior Número de Medicamentos")

st.markdown("""
    Quarto passo: Insights sobre a empresa com maior número de medicamentos encontrada.
""")

# Laboratório com maior número de medicamentos
count_products_by_lab = df.groupby("LABORATÓRIO", group_keys=False).size()
lab = count_products_by_lab.reset_index().sort_values(0, ascending=False).iloc[0]

insight_05 = lab["LABORATÓRIO"]
insight_06 = lab[0]

col1, col2 = st.columns(2)
col1.metric("Laboratório", insight_05)
col2.metric("Qtd. Medicamentos", "%s medicamentos" % thousands(insight_06))

# %%

st.markdown("------------------")

lab_products = df.loc[df["LABORATÓRIO"] == insight_05]

col1, col2 = st.columns(2)

# Quantidade de Produtos distintos no laboratório
lab_unique_products_count = lab_products['PRODUTO'].nunique()
col1.metric("Qtd. Produtos Distintos", "%s produtos" % thousands(lab_unique_products_count))

# Quantidade de combinações de substâncias no laboratórios
col2.metric("Qtd. Variantes por Produto", "%s variantes" % thousands(insight_06 / lab_unique_products_count, 2))

# %%

st.markdown("------------------")

col1, col2, col3 = st.columns(3)

# PF médio do laboratório
lab_pf_mean = lab_products['PF MED'].mean()
col1.metric("PF Mediano", currency(lab_pf_mean))

# PMC médio do laboratório
lab_pmc_mean = lab_products['PMC MED'].mean()
col2.metric("PMC Mediano", currency(lab_pmc_mean))

# PMVG médio do laboratório
lab_pmvg_mean = lab_products['PMVG MED'].mean()
col3.metric("PMVG Mediano", currency(lab_pmvg_mean))

st.markdown("""
    Aqui, podemos ver que o laboratório EMS S/A possuí uma grande quantidade de produtos, e diferentes variantes do
    mesmo produto. Isso permite que o laboratório possa comercializar diferentes produtos com diferentes preços para
    obter maior lucro. Com o PF mediano sendo de R$128, vemos que o preço comercializado com o governo ou diretamente
    com o consumidor não difere da mediana geral de todos os laboratórios. A diferença do PMC da EMS S/A se mantém em
    39% e o PMGV também se mantém com uma queda de -22%
""")

