import streamlit as st
import pandas as pd
import math
from pathlib import Path
import numpy as np
from sf_library import TICKERS_REGIONES, TICKERS_SECTORES, obtener_momentos_desde_csv, compute_portfolio_metrics
from optimization import (
    optimize_min_variance,
    optimize_max_sharpe,
    optimize_markowitz_target,
    port_return,
    port_vol,
)

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

st.subheader("ETFs Regionales Disponibles")
st.table({
    "ETFs Regionales": ["SPLG", "EWC", "IEUR", "EEM", "EWJ"],
    "Descripción": [
        "ETF que sigue el índice S&P 500.",
        "ETF que sigue el índice de acciones canadienses.",
        "ETF que sigue el índice de acciones europeas.",
        "ETF que sigue el índice de acciones de mercados emergentes.",
        "ETF que sigue el índice de acciones japonesas."
    ]
})

st.subheader("ETFs Sectoriales Disponibles")
st.table({
    "ETFs Sectoriales": ["XLC", "XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU"],
    "Descripción": [
        "ETF que sigue el índice de comunicaciones.",
        "ETF que sigue el índice de consumo discrecional.",
        "ETF que sigue el índice de consumo básico.",
        "ETF que sigue el índice de energía.",
        "ETF que sigue el índice financiero.",
        "ETF que sigue el índice de salud.",
        "ETF que sigue el índice industrial.",
        "ETF que sigue el índice de materiales.",
        "ETF que sigue el índice inmobiliario.",
        "ETF que sigue el índice tecnológico.",
        "ETF que sigue el índice de servicios públicos."
    ]
})
# elección de universo y cálculo de μ y Σ
st.subheader("Universo de inversión a analizar")

universo = st.selectbox(
    "Selecciona el universo de inversión que quieres analizar:",
    ["Regiones", "Sectores"],
    index=0,
)

if universo == "Regiones":
    tickers_universo = TICKERS_REGIONES
else:
    tickers_universo = TICKERS_SECTORES

df_universo, mu_universo, Sigma_universo = obtener_momentos_desde_csv(tickers_universo)
returns_universo = df_universo.drop(columns="date")  # solo rendimientos

st.write("Tickers del universo seleccionado:", tickers_universo)

col_mu, col_sigma = st.columns(2)
with col_mu:
    st.markdown("**Rendimientos esperados μ (promedio):**")
    st.dataframe(mu_universo.to_frame("μ"))

with col_sigma:
    st.markdown("**Matriz de varianza–covarianza Σ:**")
    st.dataframe(Sigma_universo)
# Elección del analisis del portafolio
tipo_portafolio = st.selectbox(
    "Por favor, seleccione el tipo de Análisis del Portafolio que desea usar:",
    ("Arbitrario", "Optimizado", "Black-Litterman"),
    index=None,
    placeholder="Seleccione metodo de análisis...",
)
# actualizar el flag según la selección
arbitrario = (tipo_portafolio == "Arbitrario")

#Barra lateral para mostrar y definir los pesos de los ETFs
with st.sidebar:
    st.header("Definición de Pesos de los Activos")
    st.subheader("ETFs Regionales")

    left, right = st.columns([2,1],vertical_alignment='center')
    with left:
        st.write("SPLG")
        st.write("EWC")
        st.write("IEUR")    
        st.write("EEM")
        st.write("EWJ")
    
    #########etiquetas para peso de portafolio optimizado y black-litterman######
    with right:
        st.write(W_SPLG)
        st.write(W_EWC)        
        st.write(W_IEUR)
        st.write(W_EEM)
        st.write(W_EWJ)

    st.subheader("ETFs Sectoriales")

    left_S, right_S = st.columns([2,1],vertical_alignment='center')
    with left_S:
        st.write("XLC")
        st.write("XLY")
        st.write("XLP")    
        st.write("XLE")
        st.write("XLF")
        st.write("XLV")
        st.write("XLI")
        st.write("XLB")
        st.write("XLRE")
        st.write("XLK")
        st.write("XLU")
    
    if arbitrario:
        #######Input de pesos para portafolio arbitrario########
        with right_S:
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
        with right_S:
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

    #######Input de pesos para portafolio arbitrario########
    st.subheader("Análisis de Portafolio Arbitrario")
    '''
    Por favor, defina el peso de cada uno de los ETF´s Regionales que componen el portafolio.
    '''
    regionales=st.columns(5)
    with regionales[0]:
        st.number_input(
            "SPLG",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_SPLG",
        )
    with regionales[1]:
        st.number_input(
            "EWC",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_EWC",
        )
    with regionales[2]:
        st.number_input(
            "IEUR",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_IEUR",
        )
    with regionales[3]:
        st.number_input(
            "EEM",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_EEM",
        )
    with regionales[4]:
        st.number_input(
            "EWJ",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_EWJ",
        )
    '''
    Por favor, defina el peso de cada uno de los ETF´s Sectoriales que componen el portafolio.
    '''
    sectoriales_1=st.columns(5)
    with sectoriales_1[0]:
        st.number_input(
            "XLC",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_XLC",
        )
    with sectoriales_1[1]:
        st.number_input(
            "XLY",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_XLY",
        )
    with sectoriales_1[2]:
        st.number_input(
            "XLP",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_XLP",
        )
    with sectoriales_1[3]:
        st.number_input(
            "XLE",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_XLE",
        )
    with sectoriales_1[4]:
        st.number_input(
            "XLF",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_XLF",
        )
    
    sectoriales_2=st.columns(5)
    with sectoriales_2[0]:
        st.number_input(
            "XLV",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_XLV",
        )
    with sectoriales_2[1]:
        st.number_input(
            "XLI",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_XLI",
        )
    with sectoriales_2[2]:
        st.number_input(
            "XLB",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_XLB",
        )
    with sectoriales_2[3]:
        st.number_input(
            "XLRE",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_XLRE",
        )
    with sectoriales_2[4]:
        st.number_input(
            "XLK",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_XLK",
        )
    regionales_3=st.columns(5)
    with regionales_3[0]:
        st.number_input(
            "XLU",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key="W_XLU",
        )
        rf_arbitrario = st.number_input(
        "Tasa libre de riesgo (rf, por periodo) para el análisis del portafolio arbitrario",
        value=0.0,
        step=0.001,
        format="%.4f",
    )

    if st.button("Calcular Analisis del Portafolio Arbitrario", horizontal_alignment='right'):
        # Orden de los tickers (regiones + sectores)
        tickers_all = TICKERS_REGIONES + TICKERS_SECTORES

        # Leemos los pesos desde st.session_state (en %)
        pesos_pct = [
            st.session_state["W_SPLG"],
            st.session_state["W_EWC"],
            st.session_state["W_IEUR"],
            st.session_state["W_EEM"],
            st.session_state["W_EWJ"],
            st.session_state["W_XLC"],
            st.session_state["W_XLY"],
            st.session_state["W_XLP"],
            st.session_state["W_XLE"],
            st.session_state["W_XLF"],
            st.session_state["W_XLV"],
            st.session_state["W_XLI"],
            st.session_state["W_XLB"],
            st.session_state["W_XLRE"],
            st.session_state["W_XLK"],
            st.session_state["W_XLU"],
        ]

        w = np.array(pesos_pct) / 100.0

        if not np.isclose(w.sum(), 1.0):
            st.warning(f"Los pesos suman {w.sum():.2f}. Se recomienda que la suma sea 1 (100%).")

        # Rendimientos históricos de todos los tickers
        df_all, _, _ = obtener_momentos_desde_csv(tickers_all)
        returns_all = df_all.drop(columns="date")

        metrics = compute_portfolio_metrics(returns_all, w, rf=rf_arbitrario)

        st.subheader("Métricas del portafolio arbitrario")
        st.table(pd.Series(metrics, name="Valor"))
    st.button("Calcular Analisis del Portafolio Arbitrario",horizontal_alignment='right')




########################## Análisis de Portafolio Optiizado ##########################
if tipo_portafolio == "Optimizado":
    st.subheader("Análisis de Portafolio Optimizado")
    '''
    Seleccione el método deseado y ajuste los parámetros según sus preferencias para obtener recomendaciones personalizadas.
    '''
    metodo_optimizado = st.selectbox(
        "Por favor, seleccione el método de optimización:",
        ("Mínima Varianza", "Máximo Sharpe", "Markowitz"),
        index=0,
    )

    rf = st.number_input(
        "Tasa libre de riesgo (rf, por periodo)",
        value=0.0,
        step=0.001,
        format="%.4f",
    )

    r_target = None
    if metodo_optimizado == "Markowitz":
        r_target = st.number_input(
            "Rendimiento objetivo (misma base temporal que μ)",
            value=float(mu_universo.mean()),
            step=0.001,
            format="%.4f",
        )

    if st.button("Calcular Análisis del Portafolio Optimizado"):
        mu_vals = mu_universo.values
        Sigma_vals = Sigma_universo.values

        if metodo_optimizado == "Mínima Varianza":
            w_opt, res = optimize_min_variance(mu_vals, Sigma_vals, short=False)
        elif metodo_optimizado == "Máximo Sharpe":
            w_opt, res = optimize_max_sharpe(mu_vals, Sigma_vals, rf=rf, short=False)
        else:
            w_opt, res = optimize_markowitz_target(mu_vals, Sigma_vals, r_target, short=False)

        
        metrics_opt = compute_portfolio_metrics(returns_universo, w_opt, rf=rf)

        st.markdown("### Pesos óptimos del portafolio")
        st.dataframe(
            pd.DataFrame({"Ticker": tickers_universo, "Peso": w_opt}).set_index("Ticker")
        )

        st.markdown("### Métricas del portafolio optimizado")
        st.table(pd.Series(metrics_opt, name="Valor"))

        st.markdown("### Métricas del portafolio optimizado")
        st.write(f"**Rendimiento esperado:** {ret_opt:.4%}")
        st.write(f"**Volatilidad:** {vol_opt:.4%}")
        st.write(f"**Sharpe (rf = {rf:.4%}):** {sharpe_opt:.4f}")

if tipo_portafolio == "Black-Litterman":
    st.subheader("Proceso en desarrollo, próximamente disponible.")
    
