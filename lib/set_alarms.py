# -*- coding: utf-8 -*-

import psycopg2
import os
import datetime

from urllib import parse


parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])


def save_alarms_settings(timestamp, chat_id):
    connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = connection.cursor()
    time = datetime.datetime.fromtimestamp(timestamp).strftime('%H')
    alarm = int(time)
    cursor.execute("SELECT chat_id from alarms WHERE chat_id={chat_id};".format(chat_id=chat_id))
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.execute("INSERT INTO alarms (chat_id, alarm) SELECT {chat_id}, {alarm} WHERE NOT EXISTS (SELECT chat_id FROM alarms WHERE chat_id={chat_id});".format(chat_id=chat_id, alarm=alarm))
        text = "You alarm was set. Starting tomorrow you will receive prices every day at {0}.00 o'clock.".format(time)
    else:
        text = "You have active alarm already."
    connection.commit()
    connection.close()
    return text
