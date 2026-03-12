from aiogram import Bot, Dispatcher, executor, types

# Bot tokeningizni quyidagi qo'shtirnoq ichiga yozing
API_TOKEN = 'BU_YERGA_TOKENNI_QO_YING'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Botingiz GitHub orqali ishlashga tayyor! ✅")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
