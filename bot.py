import pandas as pd
import ta
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

coins = [
"BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT",
"ADAUSDT","AVAXUSDT","LINKUSDT","DOTUSDT"
]


def get_klines(pair):
    try:
        url = "https://data-api.binance.vision/api/v3/klines"

        params = {
            "symbol": pair,
            "interval": "15m",
            "limit": 200
        }

        r = requests.get(url, params=params, timeout=10)

        if r.status_code != 200:
            print(f"Error fetching {pair}: {r.text}")
            return None

        return r.json()

    except Exception as e:
        print(f"Request failed for {pair}: {e}")
        return None
def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        data = {
            "chat_id": CHAT_ID,
            "text": message
        }

        requests.post(url, data=data, timeout=10)

    except Exception as e:
        print("Telegram error:", e)

send_telegram("Bot is running on GitHub Actions.")

def analyze(pair):

    klines = get_klines(pair)

    if not klines:
        return

    df = pd.DataFrame(klines)

    # Close price column
    df["close"] = df[4].astype(float)

    price = df["close"].iloc[-1]

    rsi = ta.momentum.RSIIndicator(df["close"]).rsi().iloc[-1]

    ema = ta.trend.EMAIndicator(df["close"], window=200).ema_indicator().iloc[-1]

    support = df["close"].tail(50).min()

    if price > ema and price <= support * 1.02 and rsi < 40:

        entry = round(price, 2)
        tp1 = round(price * 1.02, 2)
        tp2 = round(price * 1.05, 2)
        tp3 = round(price * 1.08, 2)
        sl = round(price * 0.98, 2)

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


def run_bot():
    for coin in coins:
        analyze(coin)


if __name__ == "__main__":
    run_bot()
