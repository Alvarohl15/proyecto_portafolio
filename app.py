import streamlit as st
import pandas as pd
import math
from pathlib import Path

#booleano para definir si es portafolio arbitrario
arbitrario=False

#Etiquetas para pesos de los ETFs
W_EEM=0.0
W_EWC=0.0
W_IEUR=0.0
W_SPLG=0.0
W_EWJ=0.0
W_XLC=0.0
W_XLY=0.0
W_XLP=0.0
W_XLE=0.0
W_XLF=0.0
W_XLV=0.0
W_XLI=0.0
W_XLB=0.0
W_XLRE=0.0
W_XLK=0.0
W_XLU=0.0


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='SF-Portafolio de Inversión',
    page_icon=':earth_americas:',
)

# Introcucción a la página
st.header('Análisis Cauntitativo - Portafolio de Inversión')
'''
Bienvenido a esta aplicación de análisis y optimización de portafolios. Aquí podrás explorar estrategias
de inversión por regiones y sectores, consultar métricas clave como rendimiento, riesgo; 
y comparar distintos tipos de portafolios: arbitrarios, optimizados (M ́ınima Varianza, Ma ́ximo Sharpe y Markowitz) y basados en Black-Litterman.

La plataforma ofrece gráficos interactivos, parámetros ajustables y guías claras en cada sección,
 para que puedas evaluar tus decisiones de inversión de forma sencilla y eficiente.
 '''

# Elección del analisis del portafolio
tipo_portafolio = st.selectbox(
    "Por favor, seleccione el tipo de Análisis del Portafolio que desea usar:",
    ("Arbitrario", "Optimizado", "Black-Litterman"),
    index=None,
    placeholder="Seleccione metodo de análisis...",
)

#Barra lateral para mostrar y definir los pesos de los ETFs
with st.sidebar:
    st.header("Definición de Pesos de los Activos")
    st.subheader("ETFs Regionales")

    left, right = st.columns([2,1],vertical_alignment='center')
    with left:
        st.write("SPLG: ETF que sigue el índice S&P 500.")
        st.write("EWC: ETF que sigue el índice de acciones canadienses.")
        st.write("IEUR: ETF que sigue el índice de acciones europeas.")    
        st.write("EEM: ETF que sigue el índice de acciones de mercados emergentes.")
        st.write("EWJ: ETF que sigue el índice de acciones japonesas.")
    
    if arbitrario:
        #######Input de pesos para portafolio arbitrario########
        with right:
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_SPLG",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_EWC",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_IEUR",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_EEM",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_EWJ",
            )
    else:
        #########etiquetas para peso de portafolio optimizado y black-litterman######
        with right:
            st.write(W_SPLG)
            st.write(W_EWC)        
            st.write(W_IEUR)
            st.write(W_EEM)
            st.write(W_EWJ)

    st.subheader("ETFs Sectoriales")

    with left:
        st.write("XLC: ETF que sigue el índice de comunicaciones.")
        st.write("XLY: ETF que sigue el índice de consumo discrecional.")
        st.write("XLP: ETF que sigue el índice de consumo básico.")    
        st.write("XLE: ETF que sigue el índice de energía.")
        st.write("XLF: ETF que sigue el índice financiero.")
        st.write("XLV: ETF que sigue el índice de salud.")
        st.write("XLI: ETF que sigue el índice industrial.")
        st.write("XLB: ETF que sigue el índice de materiales.")
        st.write("XLRE: ETF que sigue el índice inmobiliario.")
        st.write("XLK: ETF que sigue el índice tecnológico.")
        st.write("XLU: ETF que sigue el índice de servicios públicos.")
    
    if arbitrario:
        #######Input de pesos para portafolio arbitrario########
        with right:
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_XLC",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_XLY",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_XLP",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_XLE",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_XLF",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_XLV",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_XLI",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_XLB",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_XLRE",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_XLK",
            )
            st.number_input(
                "Peso asignado",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="W_XLU",
            )
    else:
        #########etiquetas para peso de portafolio optimizado y black-litterman######
        with right:
            st.write(W_XLC)
            st.write(W_XLY)        
            st.write(W_XLP)
            st.write(W_XLE)
            st.write(W_XLF)
            st.write(W_XLV)
            st.write(W_XLI)
            st.write(W_XLB)
            st.write(W_XLRE)
            st.write(W_XLK)
            st.write(W_XLU)


########################## Análisis de Portafolio Arbitrario ##########################
if tipo_portafolio == "Arbitrario":
    arbitrario=True
    st.subheader("Análisis de Portafolio Arbitrario")
    '''
    Por favor, defina el peso de cada uno de los activos que componen el portafolio.
    '''

    weight_matrix_regionales = pd.DataFrame(
    {
        "ETF Regionales": ["SPLG", "EWC", "IEUR", "EEM", "EWJ"],
        "Weight": [0, 78, 4, 0, 0]
    },
    index=["ETF Regionales", "Weight"],
    )

    weight_matrix_sectores = pd.DataFrame(
    {
        "ETF Sectoriales": ["XLC", "XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU"],
        "Weight": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    index=["ETF Sectoriales", "Weight"],
    )

    st.table(weight_matrix_regionales)
else:
    Arbitrario=False