from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from .log import logger
from .config import Config
from .opw import get_weather
from .sqlite_db import init_db
from .sqlite_db import insert_db


@insert_db
def start(updater, context):
    updater.message.reply_text('Hi!')


@insert_db
def command_help(updater, context):
    updater.message.reply_text("Commands:\n/weather\n/help")


@insert_db
def echo(updater, context):
    print(updater)


@insert_db
def weather_from_location(updater, context):
    weather = get_weather('Moscow')
    temperature = weather['main']['temp']
    if isinstance(temperature, (int, float)):
        updater.message.reply_text('Temperature in Moscow: ' + str(temperature))
    else:
        updater.message.reply_text("ERROR")


def main():
    Config.read_opts()
    init_db()
    updater = Updater(token=Config.TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", command_help))
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_handler(CommandHandler("weather", weather_from_location))

    updater.start_polling()
    updater.idle()
