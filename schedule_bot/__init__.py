from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from . import mySchedule
from .log import logger
from .config import Config
from .opw import get_weather
from .sqlite_db import init_db
from .sqlite_db import insert_db
import pandas as pd

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
    /remind <Y.m.d> <message>
    /schedule_today
    """)


@insert_db
def echo(updater, context):
    print(updater)


@insert_db
def weather_from_location(updater, context):
    weather = get_weather('Moscow')
    temperature = weather['main']['temp']
    if isinstance(temperature, (int, float)):
        updater.message.reply_text('Temperature in Moscow: ' + str(temperature))
        return temperature
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


@insert_db
def schedule_today(updater, context):
    try:
        df = pd.read_excel("schedule_bot/Schedule.xlsx")
    except FileNotFoundError:
        updater.message.reply_text("File not found")
    else:
        if context.args[0] in list(df["День недели"]):
            df = df.loc[df["День недели"] == context.args[0]]
            temp = 'Предмет:{}\nЛектор:{}\nМесто встречи:{}\nНачало:{}\nКонец:{}'.format(
                df["Предмет"].values[0],
                df["Преподаватель"].values[0],
                df["Место встречи"].values[0],
                df["Начало"].values[0],
                df["Конец"].values[0]
            )
            updater.message.reply_text(temp)


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
    dp.add_handler(CommandHandler("schedule_today", schedule_today))

    updater.start_polling()
    # updater.idle()

    schedule_thread = Thread(target=mySchedule.start_schedule)
    schedule_thread.start()
    schedule_thread.join()
