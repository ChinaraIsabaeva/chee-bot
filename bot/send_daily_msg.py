# -*- coding: utf-8 -*-

import psycopg2
import os
import datetime
import json

from urllib import parse
from psycopg2.extras import RealDictCursor

from bot import Bot

from lib.json_encoder import MyEncoder
from lib.prices import get_prices


TOKEN = os.environ['TOKEN']
parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

connection = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


def send_prices_by_alert():
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT chat_id, time, alarm_type FROM alarms;")
    query = json.dumps(cursor.fetchall(), cls=MyEncoder)
    data = json.loads(query)
    current_hour = datetime.datetime.now().time().hour
    bot = Bot(TOKEN)
    connection.close()
    for row in data:
        if row.get('alarm_type') == 'hourly':
            chat_id = row.get('chat_id')
            text = get_prices()
            bot.send_daily_msg(chat_id, text)
        else:
            time = datetime.datetime.strptime(
                row.get('time'), '%d %b %Y %H:%M:%S'
            )
            if current_hour == time.time().hour:
                chat_id = row.get('chat_id')
                text = get_prices()
                bot.send_daily_msg(chat_id, text)


def main():
    send_prices_by_alert()


if __name__ == '__main__':
    main()
