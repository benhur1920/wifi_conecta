import matplotlib as pl
import plotly.express as px
import streamlit as st
from funcoes import df_bairro, df_zona, df_mapa

# Criando o gráfico de distribuicao por zona
def grafico_zona(df):
    df_agrupado = df.groupby('REGIÃO')[['BAIRRO']].count().reset_index()
    
    fig =  px.treemap(
        df_agrupado,
        path=['REGIÃO'],
        values='BAIRRO',
        color='BAIRRO',
        
    )
    fig.update_layout(
        title={
            'text': 'Quantidade de sinal de wifi por Zona',
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 22,
                'color': '#0b3d91'
            }
        }
    )
    return fig

# Criando o gráfico de distribuicao por bairro
def grafico_bairro(df):
    df_bairro = df.groupby('BAIRRO').size().reset_index(name='TOTAL')
    df_bairro = df_bairro.sort_values('TOTAL', ascending=False)

    fig1 =  px.bar(
        df_bairro,
        x='BAIRRO',
        y='TOTAL',
        
    )
    fig1.update_layout(
        title={
            'text': 'Quantidade de sinal de wifi por Bairro',
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 22,
                'color':  '#0b3d91'
            }
        }
    )
    return fig1


# Criando o gráfico de distribuicao por mapa
def grafico_mapa(df):
    
    fig3 =  px.scatter_mapbox(
        df,
        hover_name='BAIRRO',
        hover_data={
            'REGIÃO': True,
            'RPA': True,
            'ENDEREÇO': True  # ou outra coluna com o endereço completo
        },
        lat='LATITUDE',
        lon='LONGITUDE',
        zoom=11,
        height=500,
        color_discrete_sequence=['black']  # todos os pontos na cor preta
        
    )
    fig3.update_layout(
        title={
            'text': 'Pontos de WiFi na cidade do Recife',
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 22,
                'color':  '#0b3d91'
            }
            
        }
    )
    return fig3