import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='SF-Portafolio de Inversión',
    page_icon=':earth_americas:',
)


st.header('Análisis Cauntitativo - Portafolio de Inversión')
'''
Aqui va una intrducción de la funcionalidad de la pagina
'''

tipo_portafolio = st.selectbox(
    "Por favor, seleccione el tipo de Análisis del Portafolio que desea usar:",
    ("Arbitrario", "Optimizado", "Black-Litterman"),
    index=None,
    placeholder="Seleccione metodo de análisis...",
)

if tipo_portafolio == "Arbitrario":
    st.subheader("Análisis de Portafolio Arbitrario")
    '''
    Por favor, defina el peso de cada uno de los activos que componen el portafolio.
    '''
    W_SPLG = st.number_input(
        "Peso asignado a ETF SPLG:",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.1,
    )

    weight_matrix_regionales = pd.DataFrame(
    {
        "ETF Regionales": ["SPLG", "EWC", "IEUR", "EEM", "EWJ"],
        "Weight": [W_SPLG, 78, 4, 0, 0]
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
