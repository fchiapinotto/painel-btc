import pandas as pd
import ta

def compute_all_indicators(df: pd.DataFrame) -> dict:
    rsi = ta.momentum.RSIIndicator(df['close'], window=14).rsi().iloc[-1]
    macd = ta.trend.MACD(df['close']).macd_diff().iloc[-1]
    bb_width = ta.volatility.BollingerBands(df['close']).bollinger_pband().iloc[-1]
    adx = ta.trend.ADXIndicator(df['high'], df['low'], df['close']).adx().iloc[-1]
    return {'rsi': rsi, 'macd': macd, 'bb_width': bb_width, 'adx': adx}

def extract_supports_resistances(df: pd.DataFrame, window: int = 20) -> dict:
    sup = df['low'].rolling(window).min().iloc[-1]
    res = df['high'].rolling(window).max().iloc[-1]
    return {'support': sup, 'resistance': res}
