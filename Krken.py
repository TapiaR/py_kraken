import krakenex
import pandas as pd

# Crear una instancia del cliente Kraken
k = krakenex.API()

# Obtener datos de un par específico, por ejemplo, ETH/EUR
response = k.query_public('OHLC', {'pair': 'ETHEUR'})
df = pd.DataFrame(response['result']['XETHZEUR'], columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])

df['close'] = pd.to_numeric(df['close'], errors='coerce')
df['high'] = pd.to_numeric(df['high'], errors='coerce')
df['low'] = pd.to_numeric(df['low'], errors='coerce')

#print(df.dtypes)

import matplotlib.pyplot as plt
import datetime

# Convertir el tiempo de Unix a datetime
df['time'] = pd.to_datetime(df['time'], unit='s')

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(df['time'], df['close'].astype(float))
plt.title('ETH/EUR Price Over Time')
plt.xlabel('Time')
plt.ylabel('Price (EUR)')
plt.show()


def stochastic_oscillator(df, k_period=14):
    low_min = df['low'].rolling(window=k_period).min()
    high_max = df['high'].rolling(window=k_period).max()

    df['%K'] = 100 * ((df['close'] - low_min) / (high_max - low_min))
    df['%D'] = df['%K'].rolling(window=3).mean()
    return df

df = stochastic_oscillator(df)

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(df['time'], df['%K'], label='%K')
plt.plot(df['time'], df['%D'], label='%D')
plt.title('Stochastic Oscillator')
plt.xlabel('Time')
plt.ylabel('Stochastic Value')
plt.legend()
plt.show()


class CryptoData:
    def __init__(self, pair):
        self.pair = pair
        self.df = None

    def fetch_data(self):
        # Implementar la lógica para descargar datos
        pass

    def calculate_stochastic(self):
        # Implementar el cálculo del oscilador estocástico
        pass

    def plot_data(self):
        # Implementar la lógica para graficar los datos
        pass


