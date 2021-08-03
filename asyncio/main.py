import sqlite3
import asyncio
import sys

import aiosmtplib


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    super_loop = asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def get_from_db():
    connect = sqlite3.connect("contacts.db")
    cursor = connect.cursor()
    res = connect.execute("SELECT * FROM contacts").fetchall()
    result = []
    for i in res:
        result.append({"name": i[1], "email": i[3]})
    return result


async def send_hello_world(username, to_user):
    client = aiosmtplib.SMTP(hostname="smtp.gmail.com", port=465, use_tls=True)
    await client.connect()
    await client.login("имейл", "пароль")
    message = f"hello {username} thanks for subscribing!"
    await client.sendmail("имейл", to_user, message)
    await client.quit()


async def main():
    ready_messages = []
    get_users = get_from_db()
    for user in get_users:
        co1 = send_hello_world(
            user["name"],
            user["email"],
        )
        ready_messages.append(co1)
    send = await asyncio.gather(*ready_messages)
    return send

event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main())
