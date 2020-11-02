import datetime
import time

import schedule

events = []


def start_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


def events_check(updater, context):
    for event in events:
        dt = event[0] - datetime.datetime.now().date()
        if dt.days <= 0:
            updater.message.reply_text(f"You'r event: {event[1]}")
            # context.bot.send_message(updater['message']['chat']['id'], f"You have an event: {event[1]}")
            events.remove(event)
    return schedule.CancelJob

