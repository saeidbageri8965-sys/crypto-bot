import ccxt
import pandas as pd
import pandas_ta as ta
import requests
import os

# خواندن اطلاعات امنیتی از تنظیمات گیت‌هاب
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
    try:
        requests.get(url, timeout=10)
    except:
        print("خطا در ارسال به تلگرام")

# لیست ارزها برای بررسی
symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'AVAX/USDT', 'SUI/USDT']
exchange = ccxt.kucoin()

print("🚀 شروع اسکن بازار...")

for symbol in symbols:
    try:
        # دریافت داده‌های ۱ ساعته
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
        df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
        
        # محاسبه شاخص RSI
        df['RSI'] = ta.rsi(df['close'], length=14)
        last_rsi = df['RSI'].iloc[-1]
        price = df['close'].iloc[-1]
        
        print(f"Check {symbol}: RSI is {last_rsi:.2f}")

        # شرط سیگنال خرید (RSI زیر ۳۰ یعنی اشباع فروش و احتمال رشد)
        if last_rsi < 30:
            msg = f"✅ سیگنال خرید پیدا شد!\n💎 ارز: {symbol}\n💰 قیمت: {price}\n📊 شاخص RSI: {last_rsi:.2f}"
            send_msg(msg)
            
    except Exception as e:
        print(f"خطا در تحلیل {symbol}: {e}")

print("✅ پایان اسکن.")
