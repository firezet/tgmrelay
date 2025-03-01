from pyrogram import Client, filters
from datetime import datetime
import sqlite3
import json
import string
import requests
from weather_config import openweather
from pprint import pprint

config = {
    "name": "tgmrelay",
    "messages": "messages.db",
    "api_id": 3899724,
    "api_hash": "78884de73e8aec575ecbe9cf4e11bf20",
    "source_chat_id": -1001851907744,
    "source_chat_kursk_nov": -1001651474042,
    "source_chat_kurskbomond": -1001421494607,
    "source_chat_Kurskk_dtp": -1001279355664,
    "source_chat_Kursk_gide": -1001322836648,
    "source_chat_zhest_kursk_46": -1001449911101,
    "target_chat_id": -1001702767543,
}


class Messages:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()
        with self.connection:
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS messages(target INTEGER, source INTEGER, message INTEGER, text VARCHAR(4096));")

    def exists(self, target, source, message: int):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM messages WHERE target=? AND source=? AND message=?;",
                                         (target, source, message)).fetchall()
            print(result)
            return bool(len(result))

    def add(self, target, source, message: int, text: str):
        with self.connection:
            return self.cursor.execute("INSERT INTO messages VALUES (?,?,?,?);", (target, source, message, text))

    def close(self):
        self.connection.close()

app = Client(config["name"], config["api_id"], config["api_hash"], system_version='Arch', no_updates=False, hide_password=True)
messages = Messages(config["messages"])
with app:
    print(app.export_session_string())


@app.on_message(filters.chat(config["source_chat_id"]))
async def filterpurge(client, message):
    # проводим проверку с помощью генератора множеств
    if {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('keywords.json')))) != set():
        await app.forward_messages(config["target_chat_id"], config["source_chat_id"], message.id, message.text)
        print(message.date)
        # store message in the database
        messages.add(config["target_chat_id"], message.chat.id, message.id, message.text)

@app.on_message(filters.chat(config["source_chat_kursk_nov"]))
async def filterpurge1(client, message):
    # проводим проверку с помощью генератора множеств
    if {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('keywords.json')))) != set():
        await app.forward_messages(config["target_chat_id"], config["source_chat_kursk_nov"], message.id, message.text)
        print(message.date)
        # store message in the database
        messages.add(config["target_chat_id"], message.chat.id, message.id, message.text)

@app.on_message(filters.chat(config["source_chat_kurskbomond"]))
async def filterpurge2(client, message):
    # проводим проверку с помощью генератора множеств
    if {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('keywords.json')))) != set():
        await app.forward_messages(config["target_chat_id"], config["source_chat_kurskbomond"], message.id, message.text)
        print(message.date)
        # store message in the database
        messages.add(config["target_chat_id"], message.chat.id, message.id, message.text)

@app.on_message(filters.chat(config["source_chat_Kurskk_dtp"]))
async def filterpurge3(client, message):
    # проводим проверку с помощью генератора множеств
    if {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('keywords.json')))) != set():
        await app.forward_messages(config["target_chat_id"], config["source_chat_Kurskk_dtp"], message.id, message.text)
        print(message.date)
        # store message in the database
        messages.add(config["target_chat_id"], message.chat.id, message.id, message.text)

@app.on_message(filters.chat(config["source_chat_Kursk_gide"]))
async def filterpurge4(client, message):
    # проводим проверку с помощью генератора множеств
    if {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('keywords.json')))) != set():
        await app.forward_messages(config["target_chat_id"], config["source_chat_Kursk_gide"], message.id, message.text)
        print(message.date)
        # store message in the database
        messages.add(config["target_chat_id"], message.chat.id, message.id, message.text)

@app.on_message(filters.chat(config["source_chat_zhest_kursk_46"]))
async def filterpurge5(client, message):
    # проводим проверку с помощью генератора множеств
    if {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('keywords.json')))) != set():
        await app.forward_messages(config["target_chat_id"], config["source_chat_zhest_kursk_46"], message.id, message.text)
        print(message.date)
        # store message in the database
        messages.add(config["target_chat_id"], message.chat.id, message.id, message.text)


async def test():
    async with app:
        await app.send_message("me", "Hi!")


@app.on_message()
def weather(city, openweather):
    lon = 36.1873
    lat = 51.73
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweather}&units=metric"
    )

    data = r.json()
    pprint(data)

    feelslike = data["main"]["feels_like"]
    #city = data["name"]
    cur_weather = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    sunsetter = datetime.fromtimestamp(data["sys"]["sunrise"])


    app.send_message(config["target_chat_id"], f'Погода в {city}e\nТемпература: {cur_weather}C°\n'
        f'Ощущается как: {feelslike}C°\n'
        f'Восход солнца: {sunsetter}\n'
        f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/сек\n'
        f'Хорошего дня!')




@app.on_message(filters.chat(config["source_chat_id"]))
def get_post(client, message):
    print('it works')
    # relay only new messages, for this purpose we store all past messages in db
    if not messages.exists(config["target_chat_id"], message.id, message.text):
        # relay message to target chat
        app.forward_messages(config["target_chat_id"], config["source_chat_id"], message.id, message.text)
        # store message in the database
        messages.add(config["target_chat_id"], message.chat.id, message.id, message.text)


def main():
    print(datetime.today().strftime(f'%H:%M:%S | Started.'))
    app.run()
    with app:
        city = "Курск"
        weather(city, openweather)



    #weather(city, openweather)
    #weather(city, openweather)
    #get_post(app, 'message')
    test()



if __name__ == '__main__':
    main()
