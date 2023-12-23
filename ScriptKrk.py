import krakenex
import pandas as pd
import matplotlib.pyplot as plt

# Clase principal para el análisis del par de monedas
class AnalizadorMonedas:
    def __init__(self, par_moneda):
        self.par_moneda = par_moneda
        self.datos = None

    # Descargar datos del par de monedas usando la API de Kraken
    def descargar_datos(self):
        k = krakenex.API()
        response = k.query_public('OHLC', {'pair': self.par_moneda, 'interval': 60})
        if response['error']:
            raise ValueError(f"Error al descargar datos para {self.par_moneda}: {response['error']}")
        self.datos = pd.DataFrame(response['result'][self.par_moneda], columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
        self.datos['time'] = pd.to_datetime(self.datos['time'], unit='s')
        # Convertir columnas a flotantes
        for col in ['open', 'high', 'low', 'close', 'vwap', 'volume']:
            self.datos[col] = self.datos[col].astype(float)

    # Calcular el oscilador estocástico
    def calcular_estocastico(self, k_period=14, d_period=3):
        df = self.datos
        df['low_k'] = df['low'].rolling(window=k_period).min()
        df['high_k'] = df['high'].rolling(window=k_period).max()
        df['%K'] = (df['close'] - df['low_k']) / (df['high_k'] - df['low_k']) * 100
        df['%D'] = df['%K'].rolling(window=d_period).mean()

    # Graficar las cotizaciones
    def graficar_cotizaciones(self):
        plt.figure(figsize=(10,6))
        plt.plot(self.datos['time'], self.datos['close'])
        plt.title(f'Cotizaciones para {self.par_moneda}')
        plt.xlabel('Tiempo')
        plt.ylabel('Precio de cierre')
        plt.show()

    # Graficar el oscilador estocástico junto con las cotizaciones
    def graficar_estocastico(self):
        df = self.datos
        plt.figure(figsize=(10,6))
        plt.subplot(2, 1, 1)
        plt.plot(df['time'], df['close'])
        plt.title(f'Estocástico y Cotizaciones para {self.par_moneda}')
        plt.ylabel('Precio de cierre')

        plt.subplot(2, 1, 2)
        plt.plot(df['time'], df['%K'], label='%K')
        plt.plot(df['time'], df['%D'], label='%D')
        plt.ylabel('Estocástico')
        plt.legend()
        plt.show()

    # Método para ejecutar todo el proceso
    def procesar(self):
        try:
            self.descargar_datos()
            self.calcular_estocastico()
            self.graficar_cotizaciones()
            self.graficar_estocastico()
        except Exception as e:
            print(f"Error durante el procesamiento: {e}")

# Función para obtener y mostrar la lista de pares de monedas disponibles
def obtener_pares_disponibles():
    k = krakenex.API()
    response = k.query_public('AssetPairs')
    pares_disponibles = list(response['result'].keys())
    return pares_disponibles

# Bucle para solicitar al usuario que ingrese un par de monedas válido
while True:
    par_moneda_usuario = input("Ingrese el par de monedas a analizar (ejemplo: XBTEUR): ")
    pares_disponibles = obtener_pares_disponibles()

    if par_moneda_usuario in pares_disponibles:
        analizador = AnalizadorMonedas(par_moneda_usuario)
        analizador.procesar()
        break
    else:
        print(f"El par de monedas '{par_moneda_usuario}' no está disponible. Pares disponibles:")
        print(" / ".join(pares_disponibles))
