import sf_library as sfl

sectores = [
    'XLK', 'XLF', 'XLV', 'XLP', 'XLY', 'XLE', 
    'XLI', 'XLC', 'XLB', 'XLU', 'XLRE'
]

regiones = ['EWJ', 'SPLG', 'EEM', 'IEUR', 'EWC']

tickers = sectores + regiones

sfl.descargar_tickers(tickers)
