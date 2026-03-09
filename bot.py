from binance.client import Client
import pandas as pd
import ta
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

client = Client()

coins = [
"BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT",
"ADAUSDT","AVAXUSDT","LINKUSDT","DOTUSDT"
]

def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url,data=data)


def analyze(pair):

    klines = client.get_klines(symbol=pair, interval="15m", limit=200)

    df = pd.DataFrame(klines)
    df[4] = df[4].astype(float)

    price = df[4].iloc[-1]

    rsi = ta.momentum.RSIIndicator(df[4]).rsi().iloc[-1]

    ema = ta.trend.EMAIndicator(df[4], window=200).ema_indicator().iloc[-1]

    support = df[4].tail(50).min()
    resistance = df[4].tail(50).max()

    if price > ema and price <= support * 1.02 and rsi < 40:

        entry = round(price,2)

        tp1 = round(price*1.02,2)
        tp2 = round(price*1.05,2)
        tp3 = round(price*1.08,2)

        sl = round(price*0.98,2)

        post = f"""
📊 {pair} LONG SETUP

Entry: {entry}

Reason:
• Price reacting near support
• RSI oversold ({round(rsi,1)})
• Possible bounce

Targets
🎯 {tp1}
🎯 {tp2}
🎯 {tp3}

Stop Loss: {sl}

Trade carefully.
"""

        send_telegram(post)


for coin in coins:

    analyze(coin)