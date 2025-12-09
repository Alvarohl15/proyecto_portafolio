import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sf_library as sfl
from scipy.optimize import minimize

sectores = [
    'XLK',  # Tecnología
    'XLF',  # Finanzas
    'XLV',  # Salud
    'XLP',  # Consumo básico
    'XLY',  # Consumo discrecional
    'XLE',  # Energía
    'XLI',  # Industrial
    'XLC',  # Comunicaciones
    'XLB',  # Materiales
    'XLU',  # Servicios públicos
    'XLRE', # Bienes raíces
]

Regiones=[
    'EWJ',  # Japón
    'SPLG',  # Global
    'EEM',  # Mercados emergentes
    'IEUR',  # Europa
    'EWC',  # Canadá
]

tickers = sectores + Regiones

#Descargando la iforamación de los tickers
sfl.descargar_tickers(tickers)


#Matriz de correlación entre sectores

all_returns = []

for ticker in tickers:
    t = sfl.daily_return(ticker, data_dir="MarketData")
    t = t[['date', 'return']].rename(columns={'return': ticker})
    all_returns.append(t)

df = all_returns[0]
for t in all_returns[1:]:
    df = pd.merge(df, t, on='date', how='inner')

df = df.dropna().sort_values('date').reset_index(drop=True)
df = df[df['date']<'2019-01-01']
df

returns_only = df.drop(columns='date')
mtx_var_covar = returns_only.cov().values
mtx_correl = returns_only.corr().values

plt.figure(figsize=(18, 16))
sns.heatmap(
    mtx_correl,
    annot=True,        # imprime el valor de correlación en cada celda
    fmt=".2f",         # 2 decimales
    cmap="coolwarm",   
    vmin=0, vmax=1
)
plt.title("Matriz de Correlaciones de Tickers")
plt.tight_layout()
plt.show()
# ============================================
# FUNCIONES DE OPTIMIZACIÓN (MARKOWITZ)
# ============================================

def _check_inputs(mu, Sigma):
    """
    Convierte mu y Sigma a numpy y valida dimensiones.
    mu: iterable de medias (por ejemplo, mu_universo de pandas)
    Sigma: matriz varianza-covarianza (DataFrame o array)
    """
    mu = np.asarray(mu).reshape(-1)
    Sigma = np.asarray(Sigma)
    n = mu.shape[0]

    if Sigma.shape != (n, n):
        raise ValueError("Dimensiones incompatibles entre mu y Sigma.")

    return mu, Sigma, n


def port_return(w, mu):
    """
    Rendimiento esperado del portafolio: w' mu
    """
    return float(np.dot(w, mu))


def port_vol(w, Sigma):
    """
    Volatilidad del portafolio: sqrt(w' Σ w)
    """
    return float(np.sqrt(w @ Sigma @ w))


def optimize_min_variance(mu, Sigma, short=False):
    """
    Portafolio de MÍNIMA VARIANZA:
        min  w' Σ w
        s.a. sum(w) = 1
             (y w >= 0 si short = False)
    """
    mu, Sigma, n = _check_inputs(mu, Sigma)

    def obj(w):
        return w @ Sigma @ w

    cons = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]

    bounds = None if short else [(0.0, 1.0)] * n
    w0 = np.ones(n) / n

    res = minimize(obj, w0, method="SLSQP", bounds=bounds, constraints=cons)

    return res.x, res


def optimize_max_sharpe(mu, Sigma, rf=0.0, short=False):
    """
    Portafolio de MÁXIMO SHARPE:
        max (w' mu - rf) / sqrt(w' Σ w)
        s.a. sum(w) = 1
             (y w >= 0 si short = False)
    """
    mu, Sigma, n = _check_inputs(mu, Sigma)

    def neg_sharpe(w):
        r = port_return(w, mu)
        v = port_vol(w, Sigma)
        if v == 0:
            return 1e6
        return -(r - rf) / v   # negativo porque minimizamos

    cons = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]
    bounds = None if short else [(0.0, 1.0)] * n
    w0 = np.ones(n) / n

    res = minimize(neg_sharpe, w0, method="SLSQP", bounds=bounds, constraints=cons)

    return res.x, res


def optimize_markowitz_target(mu, Sigma, r_target, short=False):
    """
    Portafolio de Markowitz con RENDIMIENTO OBJETIVO:
        min  w' Σ w
        s.a. sum(w) = 1
             w' mu = r_target
             (y w >= 0 si short = False)
    """
    mu, Sigma, n = _check_inputs(mu, Sigma)

    def obj(w):
        return w @ Sigma @ w

    cons = [
        {"type": "eq", "fun": lambda w: np.sum(w) - 1.0},
        {"type": "eq", "fun": lambda w: np.dot(w, mu) - r_target},
    ]

    bounds = None if short else [(0.0, 1.0)] * n
    w0 = np.ones(n) / n

    res = minimize(obj, w0, method="SLSQP", bounds=bounds, constraints=cons)

    return res.x, res
