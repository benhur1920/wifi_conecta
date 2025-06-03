import streamlit as st
from dataset import df
from funcoes import limpar_dados




st.markdown(
    "<h1 style='color: #0b3d91;'>Wifi Conecta Recife</h1>",
    unsafe_allow_html=True
)


st.markdown("<hr style='border:2px solid #1f77b4;'>",
    unsafe_allow_html=True)


# Corrige tipos e remove NaNs
df['REGIÃO'] = df['REGIÃO'].astype(str)
df['BAIRRO'] = df['BAIRRO'].astype(str)

# Seleção de colunas
with st.expander('Clique para selecionar as colunas  que deseja para download do seu arquivo .csv na seta'):
    colunas = st.multiselect(
        'Selecione as Colunas',
        options=list(df.columns),
        default=list(df.columns)
    )

st.sidebar.title('Filtros')

# Filtros hierárquicos
zonas_selecionadas = st.sidebar.multiselect(
    "Selecione a Zona",
    options=sorted(df['REGIÃO'].unique())
)

# Bairros filtrados conforme zona (se houver)
if zonas_selecionadas:
    df_temp = df[df['REGIÃO'].isin(zonas_selecionadas)]
else:
    df_temp = df

bairros_selecionados = st.sidebar.multiselect(
    "Selecione o Bairro",
    options=sorted(df_temp['BAIRRO'].unique())
)

# Se bairro for selecionado, atualizar zonas também
if bairros_selecionados:
    df_temp = df[df['BAIRRO'].isin(bairros_selecionados)]
    zonas_validas = sorted(df_temp['REGIÃO'].unique())
    zonas_selecionadas = [z for z in zonas_selecionadas if z in zonas_validas] if zonas_selecionadas else zonas_validas

# Aplica os filtros no DataFrame
filtro_dados = df.copy()

if zonas_selecionadas:
    filtro_dados = filtro_dados[filtro_dados['REGIÃO'].isin(zonas_selecionadas)]

if bairros_selecionados:
    filtro_dados = filtro_dados[filtro_dados['BAIRRO'].isin(bairros_selecionados)]

# Aplica seleção de colunas
filtro_dados = filtro_dados[colunas]

# Mostra os dados
st.dataframe(filtro_dados)

# Conta a quantidade de linhas selecionados e que serão gravadas no arquivo csv
contagem = filtro_dados['REGIÃO'].value_counts()
# Botão de download
csv = filtro_dados.to_csv(index=False).encode('utf-8')

# Exibição lado a lado no Streamlit
col1, col2,  = st.columns(2)
        
with col1:    
    st.download_button(
            label="📥 Baixar dados filtrados",
            data=csv,
            file_name='wifi_conecta_recife_filtrado.csv',
            mime='text/csv'
    )
with col2:
    st.metric(label="Total de registros filtrados", value=int(contagem.sum()))