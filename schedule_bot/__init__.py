from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from . import mySchedule
from .log import logger
from .config import Config
from .opw import get_weather
from .sqlite_db import init_db
from .sqlite_db import insert_db


from datetime import datetime
import schedule
from threading import Thread


@insert_db
def start(updater, context):
    updater.message.reply_text('Hi!')


@insert_db
def command_help(updater, context):
    updater.message.reply_text("""
    Commands:
    /weather
    /help
    /remind <Y.m.d> <message>""")


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


@insert_db
def remind(updater, context):
    try:
        date = datetime.strptime(context.args[0], "%Y.%m.%d").date()
    except ValueError:
        updater.message.reply_text("Enter the correct date: Y.m.d")
        return
    else:
        text = ' '.join(context.args[1:])
        # Сюда нужно модуль schedule вставить
        mySchedule.events.append((date, text))
        schedule.every().seconds.do(mySchedule.events_check, updater, context)
        updater.message.reply_text("Remembered")


def main():
    Config.read_opts()
    init_db()
    updater = Updater(token=Config.TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", command_help))
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_handler(CommandHandler("weather", weather_from_location))
    dp.add_handler(CommandHandler("remind", remind))

    updater.start_polling()
    # updater.idle()

    schedule_thread = Thread(target=mySchedule.start_schedule)
    schedule_thread.start()
    schedule_thread.join()

