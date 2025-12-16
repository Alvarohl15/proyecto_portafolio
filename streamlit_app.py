import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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
    optimize_BL_target,
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
ETF_Regionales=["SPLG", "EWC", "IEUR", "EEM", "EWJ"]

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

ETF_Sectoriales=["XLC", "XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU"]

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

###############Inicialización de pesos en 0##########
if "weights_arbitrary" not in st.session_state:
    st.session_state.weights_arbitrary = None

if "n_assets_arbitrary" not in st.session_state:
    st.session_state.n_assets_arbitrary = 11


# ===================== UNIVERSO =====================

st.subheader("Universo de inversión a analizar")

universo = st.selectbox(
    "Selecciona el universo de inversión que quieres analizar:",
    ["Regiones", "Sectores"],
    index=0,
)

if universo == "Regiones":
    st.session_state.n_assets_arbitrary=5
    tickers_universo = TICKERS_REGIONES
else:
    st.session_state.n_assets_arbitrary=11
    tickers_universo = TICKERS_SECTORES

df_universo, mu_universo, Sigma_universo, corr = obtener_momentos_desde_csv(tickers_universo)
returns_universo = df_universo.drop(columns="date")  # solo rendimientos

st.write("Tickers del universo seleccionado:", tickers_universo)

col_mu, col_sigma = st.columns(2)
with col_mu:
    st.markdown("**Rendimientos esperados μ (promedio):**")
    st.dataframe(mu_universo.to_frame("μ"))

with col_sigma:
    st.markdown("**Matriz de varianza–covarianza Σ:**")
    st.dataframe(Sigma_universo)

fig, ax = plt.subplots(figsize=(18, 16))

sns.heatmap(
    corr,
    annot=True,     
    fmt=".2f",      
    cmap="coolwarm",
    vmin=0,
    vmax=1,
    ax=ax           
)

st.markdown("**Matriz de Correlaciones")
st.pyplot(fig)

# ===================== TIPO DE ANÁLISIS =====================

tipo_portafolio = st.selectbox(
    "Por favor, seleccione el tipo de Análisis del Portafolio que desea usar:",
    ("Arbitrario", "Optimizado", "Black-Litterman"),
    index=None,
    placeholder="Seleccione método de análisis...",
)

# ===================== PORTAFOLIO ARBITRARIO =====================

if tipo_portafolio == "Arbitrario":

    st.subheader("Análisis de Portafolio Arbitrario")
    st.markdown("Define el peso (en %) de cada ETF del portafolio.")

    temp_weights = {}

    # Pesos regionales
    if universo == "Regiones":
        for i in range(1, st.session_state.n_assets_arbitrary + 1):
            temp_weights[f"Activo {i}"] = st.slider(
                f"Peso Activo {ETF_Regionales[i-1]}",
                min_value=0.0,
                max_value=1.0,
                value=0.0 if st.session_state.weights_arbitrary is None
                    else st.session_state.weights_arbitrary.get(f"Activo {i}", 0.0),
                step=0.01,
                key=f"slider_activo_{i}"
            )
    # Pesos sectoriales
    else:
         for i in range(1, st.session_state.n_assets_arbitrary + 1):
            temp_weights[f"Activo {i}"] = st.slider(
                f"Peso Activo {ETF_Sectoriales[i-1]}",
                min_value=0.0,
                max_value=1.0,
                value=0.0 if st.session_state.weights_arbitrary is None
                    else st.session_state.weights_arbitrary.get(f"Activo {i}", 0.0),
                step=0.01,
                key=f"slider_activo_{i}"
            )

    rf_arbitrario = st.number_input(
        "Tasa libre de riesgo (rf, por periodo) para el análisis del portafolio arbitrario",
        value=0.0,
        step=0.001,
        format="%.4f",
    )

    if st.button("Calcular Análisis del Portafolio Arbitrario"):
        tickers_all = TICKERS_REGIONES + TICKERS_SECTORES

        weights = {k: v / 100 for k, v in temp_weights.items()}
        st.session_state.weights_arbitrary = weights

        w = np.array(list(st.session_state.weights_arbitrary.values()))*100

        if not np.isclose(w.sum(), 1.0):
            st.warning(f"Los pesos suman {w.sum():.2f}. Se recomienda que la suma sea 1 (100%).")
        else:

            df_pesos=pd.DataFrame({"Ticker": tickers_universo, "Peso": w}).set_index("Ticker")

            metrics = compute_portfolio_metrics(returns_universo, w, rf=rf_arbitrario)

            v=pd.Series(metrics, name="Valor")
            v=v.round(6)

            st.markdown("## Distribución del Portafolio")
            st.scatter_chart(df_pesos)

            st.markdown("## 📊 Métricas del Portafolio Arbitrario")
            col1, col2, col3 = st.columns(3)

            col1.metric("Retorno Medio", v["Media"])
            col2.metric("Volatilidad", v["Volatilidad"])
            col3.metric("Sharpe Ratio", v["Sharpe"])

            st.markdown("### ⚙️ Riesgo Ajustado")
            col1, col2, col3 = st.columns(3)
            col1.metric("Sortino Ratio", v["Sortino"])
            col2.metric("α (Retorno – rf)", v["α (retorno - rf)"])
            col3.metric("Max Drawdown", v["Max Drawdown"])

            st.markdown("### 📐 Distribución y Riesgo Extremo")

            col1, col2, col3 = st.columns(3)

            col1.metric("Skewness", v["Skewness"])
            col2.metric("Kurtosis", v["Kurtosis"])
            col3.metric("VaR 95%", v["VaR 95%"])

            col1, col2, col3 = st.columns(3)
            col1.metric("CVaR 95%", v["CVaR 95%"])
            col2.metric("Beta vs Mercado", v["Beta vs mercado"])




# ===================== PORTAFOLIO OPTIMIZADO =====================

if tipo_portafolio == "Optimizado":
    st.subheader("Análisis de Portafolio Optimizado")
    '''
    Seleccione el método deseado y ajuste los parámetros según sus preferencias para obtener recomendaciones personalizadas.
    '''
    metodo_optimizado = st.selectbox(
        "Por favor, seleccione el método de optimización:",
        ("Mínima Varianza", "Máximo Sharpe", "Markowitz"),
        index=None,
        placeholder="Seleccione método de optimización...",
    )

    # Solo mostramos inputs y botón si ya eligió un método
    if metodo_optimizado is not None:
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
            mu_vals = mu_universo.values*252 #anualizado
            Sigma_vals = Sigma_universo.values*252 #anualizado

            if metodo_optimizado == "Mínima Varianza":
                w_opt, res = optimize_min_variance(mu_vals, Sigma_vals, short=False)
            elif metodo_optimizado == "Máximo Sharpe":
                w_opt, res = optimize_max_sharpe(mu_vals, Sigma_vals, rf=rf, short=False)
            else:
                w_opt, res = optimize_markowitz_target(mu_vals, Sigma_vals, r_target, short=False)

            metrics_opt = compute_portfolio_metrics(returns_universo, w_opt, rf=rf)

            st.markdown("### Pesos óptimos del portafolio")
            df_pesos=pd.DataFrame({"Ticker": tickers_universo, "Peso": w_opt}).set_index("Ticker")
            st.dataframe(
                df_pesos
            )
            
            st.scatter_chart(df_pesos)

            v=pd.Series(metrics_opt, name="Valor")
            v=v.round(6)

            st.markdown("## 📊 Métricas del Portafolio Optimizado")
            col1, col2, col3 = st.columns(3)

            col1.metric("Retorno Medio", v["Media"])
            col2.metric("Volatilidad", v["Volatilidad"])
            col3.metric("Sharpe Ratio", v["Sharpe"])

            st.markdown("### ⚙️ Riesgo Ajustado")
            col1, col2, col3 = st.columns(3)
            col1.metric("Sortino Ratio", v["Sortino"])
            col2.metric("α (Retorno – rf)", v["α (retorno - rf)"])
            col3.metric("Max Drawdown", v["Max Drawdown"])

            st.markdown("### 📐 Distribución y Riesgo Extremo")

            col1, col2, col3 = st.columns(3)

            col1.metric("Skewness", v["Skewness"])
            col2.metric("Kurtosis", v["Kurtosis"])
            col3.metric("VaR 95%", v["VaR 95%"])

            col1, col2, col3 = st.columns(3)
            col1.metric("CVaR 95%", v["CVaR 95%"])
            col2.metric("Beta vs Mercado", v["Beta vs mercado"])



# ===================== PORTAFOLIO Black Litterman =====================

if tipo_portafolio == "Black-Litterman":
    
    if universo == "Regiones":
        assets=["SPLG", "EWC", "IEUR", "EEM", "EWJ"]
    else:
        assets = ["XLC", "XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU"]
    
    n_assets=len(assets)

    st.subheader("Análisis de Portafolio bajo Black Litterman")

    st.markdown("""En esta sección puedes definir **vistas absolutas o relativas**, junto con tu **nivel de confianza**.""")
    
    rf = st.number_input(
        "Tasa libre de riesgo (rf, por periodo)",
        value=0.0,
        step=0.001,
        format="%.4f",
    )

    r_target_bl = st.number_input(
        "Rendimiento objetivo (misma base temporal que μ)",
        value=float(mu_universo.mean()),
        step=0.001,
        format="%.4f",
    )

    
    if universo == "Regiones":
        # Número de vistas
        k = st.number_input(
            "Número de vistas",
            min_value=1,
            max_value=4,
            value=1,
            step=1
        )
    else:
        # Número de vistas
        k = st.number_input(
            "Número de vistas",
            min_value=1,
            max_value=10,
            value=1,
            step=1
        )

    P = np.zeros((k, n_assets))
    Q = np.zeros(k)
    Omega = np.zeros((k, k))

    # Definición de vistas
    st.markdown("## Definición de vistas")

    for i in range(k):
        st.markdown(f"### Vista {i + 1}")

        col1, col2, col3 = st.columns(3)

        with col1:
            view_type = st.selectbox(
                "Tipo de vista",
                ["Absoluta", "Relativa"],
                key=f"type_{i}"
            )

        with col2:
            asset_1 = st.selectbox(
                "Activo principal",
                assets,
                key=f"a1_{i}"
            )

        with col3:
            confidence = st.slider(
                "Confianza en la vista (%)",
                min_value=1,
                max_value=100,
                value=50,
                key=f"conf_{i}"
            )

        if view_type == "Relativa":
            asset_2 = st.selectbox(
                "Activo de comparación",
                assets,
                key=f"a2_{i}"
            )

        expected_return = st.number_input(
            "Retorno esperado de la vista (ej. 0.03 = 3%)",
            value=0.02,
            step=0.005,
            format="%.4f",
            key=f"q_{i}"
        )

        # Construcción de P y Q
        idx_1 = assets.index(asset_1)
        P[i, idx_1] = 1

        if view_type == "Relativa":
            idx_2 = assets.index(asset_2)
            P[i, idx_2] = -1

        Q[i] = expected_return

        # Incertidumbre Ω
        # (menor confianza → mayor varianza)
        Omega[i, i] = (1 - confidence / 100) ** 2

    # Resultados
    st.markdown("## Matrices Resultantes")

    df_P = pd.DataFrame(P, columns=assets)
    df_Q = pd.DataFrame(Q, columns=["Q"])
    df_Omega = pd.DataFrame(Omega)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Matriz P")
        st.dataframe(df_P)

    with col2:
        st.markdown("### Vector Q")
        st.dataframe(df_Q)

    with col3:
        st.markdown("### Matriz Ω")
        st.dataframe(df_Omega)

    if st.button("Calcular Análisis del Portafolio bajo Black-Litterman"):
            mu_vals = mu_universo.values*252 #anualizado
            Sigma_vals = Sigma_universo.values*252 #anualizado

            w_opt, res = optimize_BL_target(mu_vals, Sigma_vals, r_target_bl, df_P, df_Q, df_Omega, short=False)
            metrics_opt = compute_portfolio_metrics(returns_universo, w_opt, rf=rf)
            
            st.markdown("### Pesos óptimos del portafolio")
            df_pesos=pd.DataFrame({"Ticker": tickers_universo, "Peso": w_opt}).set_index("Ticker")
            st.dataframe(
                df_pesos
            )
            st.scatter_chart(df_pesos)

            v=pd.Series(metrics_opt, name="Valor")
            v=v.round(6)

            st.markdown("## 📊 Métricas del Portafolio Optimizado")
            col1, col2, col3 = st.columns(3)

            col1.metric("Retorno Medio", v["Media"])
            col2.metric("Volatilidad", v["Volatilidad"])
            col3.metric("Sharpe Ratio", v["Sharpe"])

            st.markdown("### ⚙️ Riesgo Ajustado")
            col1, col2, col3 = st.columns(3)
            col1.metric("Sortino Ratio", v["Sortino"])
            col2.metric("α (Retorno – rf)", v["α (retorno - rf)"])
            col3.metric("Max Drawdown", v["Max Drawdown"])

            st.markdown("### 📐 Distribución y Riesgo Extremo")

            col1, col2, col3 = st.columns(3)

            col1.metric("Skewness", v["Skewness"])
            col2.metric("Kurtosis", v["Kurtosis"])
            col3.metric("VaR 95%", v["VaR 95%"])

            col1, col2, col3 = st.columns(3)
            col1.metric("CVaR 95%", v["CVaR 95%"])
            col2.metric("Beta vs Mercado", v["Beta vs mercado"])

            
