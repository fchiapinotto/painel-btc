import requests
import pandas as pd

def fetch_and_process_candles(timeframe: str) -> pd.DataFrame:
    resp = requests.get("https://api.bitget.com/api/.../candles", params={"period": timeframe})
    data = resp.json().get("data", [])
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[['timestamp','open','high','low','close','volume']]
    df.sort_values('timestamp', inplace=True)
    return df
