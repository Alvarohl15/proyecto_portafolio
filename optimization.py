import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sf_library as sfl

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