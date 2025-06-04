import streamlit as st
import matplotlib as pl
import plotly.express as px
from dataset import df
from funcoes import df_zona, totalWifi, limpar_dados
from graficos import grafico_zona, grafico_bairro, grafico_mapa
from streamlit_extras.metric_cards import style_metric_cards


# Usar todo espaço disponivel na tela
st.set_page_config(layout="wide")

# Título da pagina
st.markdown(
    "<h1 style='color: #0b3d91;'>Wifi Conecta Recife</h1>",
    unsafe_allow_html=True
)

# Limpando o dataframe
df = limpar_dados(df)

# Abertura do sidebar com título
st.sidebar.markdown(
    "<h1 style='color: #0b3d91;'>Filtros</h1>",  # azul escuro
    unsafe_allow_html=True
)

# Cópia do DataFrame original para fazer os filtros sem mecher nele
df_filtrado = df.copy()

# Filtro de ZONA (ordenado alfabeticamente)
zonas_disponiveis = sorted(df_filtrado['REGIÃO'].dropna().unique())
filtro_zona = st.sidebar.multiselect(
    'Selecione a Zona',
    zonas_disponiveis
)
if filtro_zona:
    df_filtrado = df_filtrado[df_filtrado['REGIÃO'].isin(filtro_zona)]

# Filtro de BAIRRO com base nas zonas selecionadas (também ordenado)
bairros_disponiveis = sorted(df_filtrado['BAIRRO'].dropna().unique())
filtro_bairro = st.sidebar.multiselect(
    'Selecione o Bairro',
    bairros_disponiveis
)
if filtro_bairro:
    df_filtrado = df_filtrado[df_filtrado['BAIRRO'].isin(filtro_bairro)]


# gerar os graficos a partir do df filtrado
figura_zona = grafico_zona(df_filtrado)
figura_bairro = grafico_bairro(df_filtrado)
fig_mapa = grafico_mapa(df_filtrado)

# Criar as abas para navegacao do projeto

aba1, aba2 = st.tabs(['📄 Conecta wifi', '📊 Dashboards'])

with aba1:
    col1, col2 = st.columns([1,2])  # proporção da largura das colunas

    with col1:
        st.image("images/wifi.png", width=400)  # define o tamanho da imagem em pixels

    with col2:
        st.markdown(
        f"""
        <div style="text-align: center;  color: #0b3d91;">
        <h1>Rede de internet gratuita em Recife</h1>
            <p style="font-size: 15px;">
            A Prefeitura do Recife leva internet gratuita para todas as regiões da cidade, são <b>{totalWifi} </b> pontos de acesso distribuídos  pelos seus  bairros para que você possa usar seus dispositivos sem custo algum. Uma política inclusiva que conecta todos os cidadãos, oferecendo oportunidades iguais de acesso à internet.
            </p>
            <p style="font-size: 15px; margin: 10px">
            Visualize os dashboards e se informe dos locais com o sinal de wifi para ter acesso a um mundo de oportunidades !!!!!
            </p>
        </div>
        """, unsafe_allow_html=True
    )

with aba2:
    # cálculo do total de pontos
    contagem = df_filtrado['REGIÃO'].value_counts()
    contagem_fixa = df['REGIÃO'].value_counts()
    # Zona com mais pontos
    zona_mais_freq = contagem_fixa.idxmax()
    quantidade_mais = contagem_fixa.max()

    # Zona com menos pontos
    zona_menos_freq = contagem_fixa.idxmin()
    quantidade_menos = contagem_fixa.min()

    # Exibição lado a lado no Streamlit
    col1, col2, col3, col4 = st.columns(4, gap="small",border=True,vertical_alignment='center')
    
    with col1:
        
        st.metric(label="Total de pontos de Wifi", value=f"{int(contagem.sum())}")
        #st.metric(
            #label="Regiões selecionadas", value=int(contagem.sum()),delta=f"{int(contagem.sum())} pontos",border=True)

    with col2:
        st.metric(
            label=f"Zona {zona_mais_freq} com mais pontos",
            value=int(quantidade_mais)
        )

    with col3:
        st.metric(
            label=f"Zona {zona_menos_freq} com menos pontos",
            value=int(quantidade_menos)
        )
    with col4:
        st.image('images/amico.png', width=200, use_container_width=True )

    
    
    st.markdown("<hr style='border:2px solid #0b3d91;'>",
    unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # CSS para margem (pode deixar só uma vez, não precisa repetir)
    st.markdown("""
        <style>
            .grafico-com-margem {
                margin-top: 80px;
            }
        </style>
    """, unsafe_allow_html=True)

    with col1:
        st.plotly_chart(figura_zona, use_container_width=True)
    with col2:
        st.plotly_chart(figura_bairro, use_container_width=True)

    st.markdown("<hr style='border:2px solid #0b3d91;'>", unsafe_allow_html=True)

    fig_mapa.update_layout(mapbox_style="open-street-map")
    fig_mapa.update_layout(margin={"r":0, "t":30, "l":0, "b":0})

    # Aplica a margem com a div
    st.markdown('<div class="grafico-com-margem">', unsafe_allow_html=True)
    st.plotly_chart(fig_mapa, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
