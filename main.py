import os
import requests
from flask import Flask
from threading import Thread
import google.generativeai as genai
from aiogram import Bot, Dispatcher, executor, types

# Kichik server (o'chib qolmasligi uchun)
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# KALITLAR (Render Environment-dan olish xavfsizroq)
GEMINI_KEY = "AIzaSyDDJAWrZad7U4exexVby13rTR3ejScgCaM"
TELEGRAM_TOKEN = "8648750227:AAFx7z..." # O'zingizniki tursin
LFM_KEY = os.getenv("LASTFM_API_KEY")

# Gemini sozlash
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Musiqa qidirish funksiyasi
def find_artist(track_name):
    url = f"http://ws.audioscrobbler.com/2.0/?method=track.search&track={track_name}&api_key={LFM_KEY}&format=json"
    try:
        data = requests.get(url).json()
        res = data['results']['trackmatches']['track'][0]
        return f"🎵 Qo'shiq: {res['name']}\n🎤 Ijrochi: {res['artist']}"
    except:
        return None

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Salom! Menga qo'shiq nomini yozing, men ijrochisini topaman.")

@dp.message_handler()
async def handle_message(message: types.Message):
    # Avval musiqani qidiradi
    music_info = find_artist(message.text)
    
    if music_info:
        await message.answer(music_info)
    else:
        # Musiqa topilmasa Gemini javob beradi
        response = model.generate_content(message.text)
        await message.answer(response.text)

if __name__ == '__main__':
    keep_alive()
    executor.start_polling(dp, skip_updates=True)
