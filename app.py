import streamlit as st
import pandas as pd
import math
from pathlib import Path

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

    left, right = st.columns(2, vertical_alignment="bottom")
    with left:
        
        st.write("SPLG: ETF que sigue el índice S&P 500.")
        st.write("EWC: ETF que sigue el índice de acciones canadienses.")
        st.write("IEUR: ETF que sigue el índice de acciones europeas.")    
        st.write("EEM: ETF que sigue el índice de acciones de mercados emergentes.")
        st.write("EWJ: ETF que sigue el índice de acciones japonesas.")
    
    with right:
        W_SPLG = st.number_input(
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
        )

        W_EWC = st.number_input(
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
        )

    W_IEUR = st.number_input(
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    W_EEM = st.number_input(
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    W_EWJ = st.number_input(
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )
    
    st.subheader("ETFs Sectoriales")

    '''
    XLC: ETF que sigue el índice de comunicaciones.
    '''
    W_XLC = st.number_input(
        "Peso asignado a ETF XLC:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    '''
    XLY: ETF que sigue el índice de consumo discrecional.
    '''
    W_XLY = st.number_input(
        "Peso asignado a ETF V:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    '''
    XLP: ETF que sigue el índice de consumo básico.
    '''
    W_XLP = st.number_input(
        "Peso asignado a ETF XLP:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    '''
    XLE: ETF que sigue el índice de energía.
    '''
    W_XLE = st.number_input(
        "Peso asignado a ETF XLE:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    '''
    XLF: ETF que sigue el índice financiero.
    '''
    W_XLF = st.number_input(
        "Peso asignado a ETF XLF:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    '''
    XLV: ETF que sigue el índice de salud.
    '''
    W_XLV = st.number_input(
        "Peso asignado a ETF XLV:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    '''
    XLI: ETF que sigue el índice industrial.
    '''
    W_XLI = st.number_input(
        "Peso asignado a ETF XLI:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    '''
    XLB: ETF que sigue el índice de materiales.
    '''
    W_XLB = st.number_input(
        "Peso asignado a ETF XLB:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    '''
    XLRE: ETF que sigue el índice inmobiliario.
    '''
    W_XLRE = st.number_input(
        "Peso asignado a ETF XLRE:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    '''
    XLK: ETF que sigue el índice tecnológico.
    '''
    W_XLK = st.number_input(
        "Peso asignado a ETF XLK:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    '''
    XLU: ETF que sigue el índice de servicios públicos.
    '''
    W_XLU = st.number_input(
        "Peso asignado a ETF XLU:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )



########################## Análisis de Portafolio Arbitrario ##########################
if tipo_portafolio == "Arbitrario":
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
