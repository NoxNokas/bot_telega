from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from .log import logger
from .config import Config
from .opw import get_weather


def start(updater, context):
    updater.message.reply_text('Hi!')


def command_help(updater, context):
    updater.message.reply_text("Hi! I'm use less help")


def echo(updater, context):
    updater.message.reply_text(updater.message.text)


def weather_from_location(updater, context):
    weather = get_weather('Moscow')
    temperature = weather['main']['temp']
    if type(temperature) in (int, float):
        updater.message.reply_text(temperature)
    else:
        updater.message.reply_text("ERROR")


def main():
    Config.read_opts()
    updater = Updater(token=Config.TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", command_help))
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_handler(CommandHandler("weather", weather_from_location))

    updater.start_polling()
    updater.idle()
