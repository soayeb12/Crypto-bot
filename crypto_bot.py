import requests
import asyncio
from telegram import Bot

# BotFather থেকে প্রাপ্ত টোকেন এখানে দিন
BOT_TOKEN = "7550695469:AAHnAnS-UBYxbBjZrWnKAGNhIadrSKcl-xs"
CHANNEL_ID = "@crypto_verseofficial"  # আপনার চ্যানেলের ইউজারনেম দিন

# CoinGecko API URLs
url_bitcoin = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
url_ethereum = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
url_px_token = "https://api.dexscreener.com/latest/dex/search/?q=PX"

# বট চালানো
bot = Bot(token=BOT_TOKEN)

# asynchronous ফাংশন তৈরি করা
async def send_message():
    while True:
        try:
            # বিটকয়েনের দাম সংগ্রহ
            response_bitcoin = requests.get(url_bitcoin)
            if response_bitcoin.status_code == 200:
                data_bitcoin = response_bitcoin.json()
                bitcoin_price = data_bitcoin['bitcoin']['usd']
            else:
                bitcoin_price = "Unavailable"

            # ইথেরিয়ামের দাম সংগ্রহ
            response_ethereum = requests.get(url_ethereum)
            if response_ethereum.status_code == 200:
                data_ethereum = response_ethereum.json()
                ethereum_price = data_ethereum['ethereum']['usd']
            else:
                ethereum_price = "Unavailable"

            # PX টোকেনের দাম সংগ্রহ
            response_px = requests.get(url_px_token)
            if response_px.status_code == 200:
                data_px = response_px.json()
                if data_px['pairs']:
                    px_price = data_px['pairs'][0]['priceUsd']  # PX টোকেনের দাম
                    exchange_name = data_px['pairs'][0]['dexId']  # ডেক্সের নাম
                    px_token_name = data_px['pairs'][0]['baseToken']['name']  # PX টোকেনের নাম
                else:
                    px_price = "Unavailable"
                    exchange_name = "N/A"
                    px_token_name = "PX"
            else:
                px_price = "Unavailable"
                exchange_name = "N/A"
                px_token_name = "PX"

            # আপডেট টেক্সট
            message = f"💰 **Cryptocurrency Prices:**\n\n"
            message += f"🔸 Bitcoin: ${bitcoin_price} USD\n"
            message += f"🔹 Ethereum: ${ethereum_price} USD\n"
            message += f"🔸 {px_token_name} (PX): ${px_price} USD\n"
            message += f"🔹 Exchange: {exchange_name}"

            # টেলিগ্রাম চ্যানেলে মেসেজ পাঠানো
            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")

            # প্রতি ১ মিনিটে আপডেট
            await asyncio.sleep(60)

        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(60)

# asyncio মাধ্যমে বট চালানো
asyncio.run(send_message())
