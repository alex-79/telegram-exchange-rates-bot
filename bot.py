#!venv/bin/python

from aiogram import Bot, Dispatcher, executor, types
import requests
import logging
import configparser
from datetime import date

logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read('bot.ini')

BOT_TOKEN = config['general']['token']
NBU_LIST_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
NBU_CURRENCY_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={code}&date={date}&json"

# initialize bot & dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler( commands={"start", "restart"})
async def start_handler(message: types.Message):

    response = requests.get(NBU_LIST_URL).json()
    buttons = []

    for item in response:
        star = ''
        if item['cc'] in ('USD', 'EUR'):
            star = '⭐ '
        buttons.append(types.InlineKeyboardButton(text=star + item['cc'], callback_data='btn_' + item['cc']))

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)

    await message.answer(
        f"Курси валют НБУ 🇺🇦",
        parse_mode=types.ParseMode.HTML,
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn_'))
async def callback_query_handler(callback: types.CallbackQuery):
    cc = callback.data[-3:]

    if cc == 'RUB':
        msg = f"🚢🔥 русский военный корабль, иди на хуй\n🇺🇦 СЛАВА УКРАЇНІ!!!\n🇺🇦 ГЕРОЯМ СЛАВА!!!"
    else:
        today = date.today().strftime("%Y%m%d")
        response = requests.get(NBU_CURRENCY_URL.format(code = cc, date = today)).json()
        msg = f"{response[0]['exchangedate']}\n{response[0]['txt']} ({response[0]['cc']}): {response[0]['rate']} грн."

    await callback.answer(
        text=msg,
        show_alert=True
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)