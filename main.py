import os
from flask import Flask
from threading import Thread
import google.generativeai as genai
from aiogram import Bot, Dispatcher, executor, types

# Koyeb uchun kichik server (o'chib qolmasligi uchun)
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# KALITLAR
GEMINI_KEY = "AIzaSyDDJAWrZad7U4exexVby13rTR3ejScgCaM"
TELEGRAM_TOKEN = "8648750227:AAFx7ziF1nSg5YDoPfguX93YkCjhLWdSp3M"

# Gemini sozlash
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Gemini bot Koyeb serverida ishga tushdi. Savol bering!")

@dp.message_handler()
async def chat(message: types.Message):
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except:
        await message.answer("Birozdan keyin qayta urinib ko'ring...")

if __name__ == '__main__':
    keep_alive()
    executor.start_polling(dp, skip_updates=True)
import requests
import os

# Render-dagi kalitni oladi
LFM_KEY = os.getenv("LASTFM_API_KEY")

def find_artist(track_name):
    url = f"http://ws.audioscrobbler.com/2.0/?method=track.search&track={track_name}&api_key={LFM_KEY}&format=json"
    data = requests.get(url).json()
    try:
        res = data['results']['trackmatches']['track'][0]
        return f"🎵 Qo'shiq: {res['name']}\n🎤 Ijrochi: {res['artist']}"
    except:
        return "Topolmadim 😔"
