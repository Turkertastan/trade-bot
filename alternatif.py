import math
import numpy as np
import pandas as pd
from binance.client import Client

api_key = ''
api_secret = ''
client = Client(api_key, api_secret)

def klinesCoin(coinName: str, period: str, limit: int):
    kline = client.get_klines(symbol=coinName, interval=period, limit=limit)
    titles = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume",
              "number_of_trades", "tbbsv", "tbqav", "ignore"]
    data = pd.DataFrame(kline, columns=titles, dtype=float)
    return data

def calculate_rsi(data, period=14):
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

    return rsi_values[-1]

def calculate_ema(data, period):
    if len(data) < period:
        raise ValueError("Veri serisi periyoddan daha kısa olamaz.")

    sma = np.mean(data[:period])
    multiplier = 2 / (period + 1)
    ema_values = [sma]

    for i in range(period, len(data)):
        ema = (data[i] - ema_values[-1]) * multiplier + ema_values[-1]
        ema_values.append(ema)

    return ema_values[-1]

def destek_direnc(coinName: str, period: str, limit: int):
    coin = klinesCoin(coinName, period, limit)
    close = coin["close"]
    direncList = []
    destekList = []

    for x in close:
        aroundPrice = math.isclose(x, close[len(close)-1], abs_tol=(close[len(close)-1] * 10) / 100)
        if aroundPrice:
            if x > close[len(close)-1]:
                direncList.append(x)
            else:
                destekList.append(x)

    direnc = sum(direncList) / len(direncList) if direncList else 0
    destek = sum(destekList) / len(destekList) if destekList else 0

    return direnc, destek

def find_optimal_coins(api_key, api_secret):
    coinName = 'GASUSDT'  # XRP-USDT çifti için
    coin_data = klinesCoin(coinName, "15m", 200)
    close_prices = coin_data["close"].astype(float)

    ema = calculate_ema(close_prices, 10)
    rsi = calculate_rsi(close_prices, 14)
    direnc, destek = destek_direnc(coinName, "15m", 200)

    print("-----XRP-USDT İÇİN ANALİZ-----")
    print(f"EMA: {ema}")
    print(f"RSI: {rsi}")
    print(f"Direnc: {direnc}  Destek: {destek}\n")

    if close_prices.iloc[-1] > (ema * 1.02) and 30 <= rsi <= 35 and close_prices.iloc[-1] > (direnc * 1.015):
        print("En iyi ihtimal: Uzun pozisyon") 
    elif close_prices.iloc[-1] < (ema * 0.98) and close_prices.iloc[-1] < (destek * 0.985):
        print("En iyi ihtimal: Kısa pozisyon") 
    else:
        print("En iyi ihtimal: Bekleme")

if __name__ == "__main__":
    find_optimal_coins(api_key, api_secret)
