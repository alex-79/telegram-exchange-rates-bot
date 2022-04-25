#!venv/bin/python

from aiogram import Bot, Dispatcher, executor, types
import requests
import logging
import configparser
from datetime import date, timedelta

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
        buttons.append(types.InlineKeyboardButton(text=star + item['cc'], callback_data='btn_list_' + item['cc']))

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)

    await message.answer(
        f"Курси валют НБУ 🇺🇦",
        parse_mode=types.ParseMode.HTML,
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn_list_'))
async def callback_query_handler(callback: types.CallbackQuery):
    cc = callback.data[-3:]
    buttons = []

    if cc == 'RUB':
        msg = f"🚢🔥 русский военный корабль, иди на хуй\n🇺🇦 СЛАВА УКРАЇНІ!!!\n🇺🇦 ГЕРОЯМ СЛАВА!!!"
    else:
        today = date.today().strftime("%Y%m%d")
        response_today = requests.get(NBU_CURRENCY_URL.format(code = cc, date = today)).json()

        yesterday = (date.today() - timedelta(days=1)).strftime("%Y%m%d")
        response_yesterday = requests.get(NBU_CURRENCY_URL.format(code = cc, date = yesterday)).json()

        delta = response_today[0]['rate'] - response_yesterday[0]['rate']
        direct = ""
        if (delta > 0):
            direct = "({:.4f}".format(delta) + " грн.) 🔺"
        elif (delta < 0):
            direct = "({:.4f}".format(delta) + " грн.) 🔻"

        msg = f"{response_today[0]['exchangedate']}\n{response_today[0]['txt']} ({response_today[0]['cc']}): {response_today[0]['rate']} грн. {direct}"
        buttons.append(types.InlineKeyboardButton(text=f"Конвертувати грн в {cc}", callback_data='btn_conv_in_' + cc))
        buttons.append(types.InlineKeyboardButton(text=f"Конвертувати {cc} в грн", callback_data='btn_conv_out_' + cc))
        buttons.append(types.InlineKeyboardButton(text=f"Динаміка за 7 днів", callback_data='btn_graph_7_' + cc))

    keyboard = types.InlineKeyboardMarkup(1)
    keyboard.add(*buttons)

    await callback.message.answer(
        msg,
        parse_mode=types.ParseMode.HTML,
        reply_markup=keyboard
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)