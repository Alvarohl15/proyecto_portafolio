import streamlit as st
import pandas as pd
import numpy as np

from sf_library import (
    TICKERS_REGIONES,
    TICKERS_SECTORES,
    obtener_momentos_desde_csv,
    compute_portfolio_metrics,
)

from optimization import (
    optimize_min_variance,
    optimize_max_sharpe,
    optimize_markowitz_target,
)

# ===================== CONFIGURACIÓN DE LA APP =====================

st.set_page_config(
    page_title='SF-Portafolio de Inversión',
    page_icon=':earth_americas:',
)

st.header('Análisis Cuantitativo - Portafolio de Inversión')
'''
Bienvenido a esta aplicación de análisis y optimización de portafolios. Aquí podrás explorar estrategias
de inversión por regiones y sectores, consultar métricas clave como rendimiento y riesgo, 
y comparar distintos tipos de portafolios: arbitrarios y optimizados (Mínima Varianza, Máximo Sharpe y Markowitz).

La plataforma ofrece tablas con parámetros ajustables y guías claras en cada sección,
para que puedas evaluar tus decisiones de inversión de forma sencilla y eficiente.
'''

# ===================== TABLAS DE ETFs =====================

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

# ===================== UNIVERSO =====================

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

# ===================== TIPO DE ANÁLISIS =====================

tipo_portafolio = st.selectbox(
    "Por favor, seleccione el tipo de Análisis del Portafolio que desea usar:",
    ("Arbitrario", "Optimizado"),
    index=None,
    placeholder="Seleccione método de análisis...",
)

# ===================== SIDEBAR (INFO) =====================

with st.sidebar:
    st.header("Definición de Pesos de los Activos")
    st.subheader("ETFs Regionales")

    left, right = st.columns([2, 1], vertical_alignment='center')
    with left:
        st.write("SPLG")
        st.write("EWC")
        st.write("IEUR")
        st.write("EEM")
        st.write("EWJ")

    with right:
        st.write("Pesos definidos en la sección de análisis.")

    st.subheader("ETFs Sectoriales")

    left_S, right_S = st.columns([2, 1], vertical_alignment='center')
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

    with right_S:
        st.write("Pesos definidos en la sección de análisis.")

# ===================== PORTAFOLIO ARBITRARIO =====================

if tipo_portafolio == "Arbitrario":

    st.subheader("Análisis de Portafolio Arbitrario")
    st.markdown("Define el peso (en %) de cada ETF del portafolio.")

    # Pesos regionales
    regionales = st.columns(5)
    with regionales[0]:
        st.number_input("SPLG", 0.0, 100.0, 0.0, 0.1, key="W_SPLG")
    with regionales[1]:
        st.number_input("EWC", 0.0, 100.0, 0.0, 0.1, key="W_EWC")
    with regionales[2]:
        st.number_input("IEUR", 0.0, 100.0, 0.0, 0.1, key="W_IEUR")
    with regionales[3]:
        st.number_input("EEM", 0.0, 100.0, 0.0, 0.1, key="W_EEM")
    with regionales[4]:
        st.number_input("EWJ", 0.0, 100.0, 0.0, 0.1, key="W_EWJ")

    # Pesos sectoriales
    sectoriales_1 = st.columns(5)
    with sectoriales_1[0]:
        st.number_input("XLC", 0.0, 100.0, 0.0, 0.1, key="W_XLC")
    with sectoriales_1[1]:
        st.number_input("XLY", 0.0, 100.0, 0.0, 0.1, key="W_XLY")
    with sectoriales_1[2]:
        st.number_input("XLP", 0.0, 100.0, 0.0, 0.1, key="W_XLP")
    with sectoriales_1[3]:
        st.number_input("XLE", 0.0, 100.0, 0.0, 0.1, key="W_XLE")
    with sectoriales_1[4]:
        st.number_input("XLF", 0.0, 100.0, 0.0, 0.1, key="W_XLF")

    sectoriales_2 = st.columns(5)
    with sectoriales_2[0]:
        st.number_input("XLV", 0.0, 100.0, 0.0, 0.1, key="W_XLV")
    with sectoriales_2[1]:
        st.number_input("XLI", 0.0, 100.0, 0.0, 0.1, key="W_XLI")
    with sectoriales_2[2]:
        st.number_input("XLB", 0.0, 100.0, 0.0, 0.1, key="W_XLB")
    with sectoriales_2[3]:
        st.number_input("XLRE", 0.0, 100.0, 0.0, 0.1, key="W_XLRE")
    with sectoriales_2[4]:
        st.number_input("XLK", 0.0, 100.0, 0.0, 0.1, key="W_XLK")

    regionales_3 = st.columns(5)
    with regionales_3[0]:
        st.number_input("XLU", 0.0, 100.0, 0.0, 0.1, key="W_XLU")

    rf_arbitrario = st.number_input(
        "Tasa libre de riesgo (rf, por periodo) para el análisis del portafolio arbitrario",
        value=0.0,
        step=0.001,
        format="%.4f",
    )

    if st.button("Calcular Análisis del Portafolio Arbitrario"):
        tickers_all = TICKERS_REGIONES + TICKERS_SECTORES

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

        w = np.array(pesos_pct, dtype=float) / 100.0

        if not np.isclose(w.sum(), 1.0):
            st.warning(f"Los pesos suman {w.sum():.2f}. Se recomienda que la suma sea 1 (100%).")

        df_all, _, _ = obtener_momentos_desde_csv(tickers_all)
        returns_all = df_all.drop(columns="date")

        metrics = compute_portfolio_metrics(returns_all, w, rf=rf_arbitrario)

        st.subheader("Métricas del portafolio arbitrario")
        st.table(pd.Series(metrics, name="Valor"))

# ===================== PORTAFOLIO OPTIMIZADO =====================

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
