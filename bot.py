from binance.client import Client

api_key = ''
api_secret = ''
client = Client(api_key, api_secret)

import numpy as np
import pandas as pd

def calculate_rsi(data, period=14):
    """
    Verilen fiyat verisi üzerinde belirli bir periyotta RSI hesaplar.

    :param data: Hesaplanacak fiyat verilerini içeren bir liste veya numpy dizisi
    :param period: RSI'nın kullanacağı periyot (varsayılan değer: 14)
    :return: RSI veri serisi
    """
    if len(data) <= period:
        raise ValueError("Veri serisi periyoddan daha kısa olamaz.")

    delta = np.diff(data)
    gain = np.where(delta >= 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = np.mean(gain[:period])
    avg_loss = np.mean(loss[:period])

    rsi_values = [100 - (100 / (1 + avg_gain / avg_loss))]

    for i in range(period, len(data)):
        delta_gain = 0 if gain[i - 1] == 0 else gain[i - 1]
        delta_loss = 0 if loss[i - 1] == 0 else loss[i - 1]

        avg_gain = ((avg_gain * (period - 1)) + delta_gain) / period
        avg_loss = ((avg_loss * (period - 1)) + delta_loss) / period

        rsi = 100 - (100 / (1 + avg_gain / avg_loss))
        rsi_values.append(rsi)

    return rsi_values [-1:][0]


# Binance'den canlı BTC fiyatlarını al
def get_btc_prices(api_key, api_secret):
    """
    Binance'den canlı olarak BTC/USDT fiyat verilerini getirir.

    :param api_key: Binance API anahtarı
    :param api_secret: Binance API gizli anahtarı
    :return: BTC fiyatlarını içeren bir liste
    """
    client = Client(api_key, api_secret)
    klines = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_4HOUR)
    btc_prices = [float(kline[4]) for kline in klines]  # Kapanış fiyatlarını al
    return btc_prices 

# EMA hesapla
def calculate_ema(data, period):
    """
    Verilen veri serisi üzerinde belirli bir periyotta EMA hesaplar.

    :param data: Hesaplanacak fiyat verilerini içeren bir liste veya numpy dizisi
    :param period: EMA'nın kullanacağı periyot
    :return: EMA veri serisi
    """
    if len(data) < period:
        raise ValueError("Veri serisi periyoddan daha kısa olamaz.")

    # İlk EMA değerini basit hareketli ortalama ile başlat
    sma = np.mean(data[:period])
    multiplier = 2 / (period + 1)
    ema_values = [sma]

    # EMA değerlerini hesapla
    for i in range(period, len(data)):
        ema = (data[i] - ema_values[-1]) * multiplier + ema_values[-1]
        ema_values.append(ema)

    return ema_values [-1:][0]

# Binance'den BTC fiyatlarını al
btc_prices = get_btc_prices(api_key, api_secret)

# EMA periyodunu belirleyin
ema_period = 10

# EMA hesapla
btc_ema = calculate_ema(btc_prices, ema_period)

# RSI hesapla
btc_rsi = calculate_rsi(btc_prices)

print("BTC için EMA:", btc_ema)
print("BTC için RSI:", btc_rsi)


def klinesCoin(coinName:str, period:str, limit:int):
    """ Get data of a coin.
    
        **
    """

    kline = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_4HOUR)
    titles = ["open_time","open","high","low","close","volume","close_time","quote_asset_volume","number_of_trades","tbbsv","tbqav","ignore"]
    data = pd.DataFrame(kline,columns=titles,dtype=float)
    return data