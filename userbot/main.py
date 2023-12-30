from pyrogram import Client, filters, client, types
from pyrogram.enums import ParseMode
from pyrogram.errors.exceptions.flood_420 import FloodWait

import pyrogram, time

from data.config import *


key = []
try:
    with open('data/keys.txt', encoding='utf-8') as file:
        key = file.read().split('; ')
except FileNotFoundError:
    pass
while '' in key:
    key.remove('')

stop = []
try:
    with open('data/stop.txt', encoding='utf-8') as file:
        stop = file.read().split('; ')
except FileNotFoundError:
    pass
while '' in stop:
    stop.remove('')

app = Client("my_account", api_id=api_id, api_hash=api_hash)


@app.on_message(filters.command(["start"]))
async def start(cl: client, message: types.Message):
    await app.send_message(message.from_user.id, 'Бот для отслеживания сообщений с ключевыми фразами по группам\n'
                                                 '`/start` - главное меню\n'
                                                 '`/addk `фраза; фраза - добавить ключевую фразу\n'
                                                 '`/remk `фраза; фраза удалить ключевую фразу\n'
                                                 '`/adds `фраза; фраза - добавить стоп-фразу\n'
                                                 '`/rems `фраза; фраза - удалить стоп-фразу\n'
                                                 '`/join `чат1; чат2; чат3 - присоединиться к чатам\n'
                                                 f'Список ключевых фраз: '
                                                 f'{"; ".join(sorted(key))}\n'
                                                 f'Список стоп-фраз: '
                                                 f'{"; ".join(sorted(stop))}')


@app.on_message(filters.command(["addk"]))
async def addk(cl: client, message: types.Message):
    global key
    words = message.text.removeprefix('/addk ').lower().split('; ')
    for word in words:
        if word not in key:
            key.append(word)
            await app.send_message(message.from_user.id, f'Ключевая фраза `{word}` добавлена')
            continue
        await app.send_message(message.from_user.id, f'Ключевая фраза `{word}` уже есть в списке')
    with open('data/keys.txt', 'w', encoding='utf-8') as f:
        f.write('; '.join(key))


@app.on_message(filters.command(["remk"]))
async def remk(cl: client, message: types.Message):
    global key
    words = message.text.removeprefix('/remk ').lower().split('; ')
    for word in words:
        if word in key:
            key.remove(word)
            await app.send_message(message.from_user.id, f'Ключевая фраза `{word}` удалена')
            continue
        await app.send_message(message.from_user.id, f'Ключевой фразы `{word}` нет в списке')
    with open('keys.txt', 'w', encoding='utf-8') as f:
        f.write('; '.join(key))


@app.on_message(filters.command(["adds"]))
async def adds(cl: client, message: types.Message):
    global stop
    words = message.text.removeprefix('/adds ').lower().split('; ')
    for word in words:
        if word not in stop:
            stop.append(word)
            await app.send_message(message.from_user.id, f'Стоп-фраза `{word}` добавлена')
            continue
        await app.send_message(message.from_user.id, f'Стоп-фраза `{word}` уже есть в списке')
    with open('data/stop.txt', 'w', encoding='utf-8') as f:
        f.write('; '.join(stop))


@app.on_message(filters.command(["rems"]))
async def rems(cl: client, message: types.Message):
    global stop
    words = message.text.removeprefix('/rems ').lower().split('; ')
    for word in words:
        if word in stop:
            stop.remove(word)
            await app.send_message(message.from_user.id, f'Стоп-фраза `{word}` удалена')
            continue
        await app.send_message(message.from_user.id, f'Стоп-фразы `{word}` нет в списке')
    with open('stop.txt', 'w', encoding='utf-8') as f:
        f.write('; '.join(stop))


@app.on_message(filters.command('join'))
async def join_chats(cl: client, msg: types.Message):
    chats = msg.text.removeprefix('/join ').split(';')

    await app.send_message(msg.from_user.id, 'Начинаю заходить в чаты...')

    for chat_text in chats:
        chat_results = await app.invoke(pyrogram.raw.functions.contacts.Search(q=chat_text, limit=30))
        for chat in chat_results.chats:
            if chat.megagroup or chat.gigagroup and not chat.is_bot:
                try:
                    time.sleep(3)
                    await app.join_chat(chat.username)
                    time.sleep(1)
                    await app.send_message(msg.from_user.id, f'Зашел в чат `{chat.title}`')
                except FloodWait as e:
                    time_to_wait = str(e).split(" ")[8]
                    bot_msg = await app.send_message(msg.chat.id, f'Нужно подождать {time_to_wait} секунд для продолжения. Это правило самого телеграма от флуда')
                    time_int = int(time_to_wait)
                    while time_int > 1:
                        time.sleep(3)
                        time_int -= 3
                        await app.edit_message_text(msg.chat.id, bot_msg.id, f'Нужно подождать {time_int} секунд для продолжения. Это правило самого телеграма от флуда')
                except:
                    continue
    await app.send_message(msg.from_user.id, 'Я закончил заходить в группы')


@app.on_message(filters=filters.group)
async def my_handler(cl: client, message: types.Message):
    global key, stop
    text = message.text.lower() if message.text else message.caption.lower() if message.caption else ''
    for phrase in stop:
        if phrase in text:
            return
    for phrase in key:
        if not message.from_user.id:
            return
        if phrase in text:
            msg_text_value = f"💬`{message.chat.title}`\n🙋‍♂️<a href='tg://openmessage?user_id={message.from_user.id}'>{message.from_user.first_name if message.from_user.first_name else 'Ссылка на пользователя'}</a>\n@{message.from_user.username if message.from_user.username else 'Нету юзернейма от пользователя'}\n🟩🟩🟩🟩🟩🟩🟩🟩🟩\n{message.text if message.text else message.caption if message.caption else 'Нет доступа к тексту сообщения'}"
            await app.send_message(username, msg_text_value, parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    app.run()