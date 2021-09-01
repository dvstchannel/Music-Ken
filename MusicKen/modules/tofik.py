# 🍀 © @tofik_dn
# ⚠️ Do not remove credits

import requests
from pyrogram import Client

from MusicKen.config import BOT_USERNAME as bu
from MusicKen.helpers.filters import command


@Client.on_message(command(["asupan", f"asupan@{bu}"]))
async def asupan(client, message):
    message.from_user.id
    message.from_user.first_name
    message.from_user.id
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/asupan/ptl").json()
        results = f"{resp['url']}"
        return await client.send_video(
            message.chat.id, video=results, caption=f"Đây là lượng {rpk} đừng ngủ"
        )
    except Exception:
        await message.reply_text("Có gì đó không ổn LOL...")


@Client.on_message(command(["wibu", f"wibu@{bu}"]))
async def wibu(client, message):
    message.from_user.id
    message.from_user.first_name
    message.from_user.id
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/asupan/wibu").json()
        results = f"{resp['url']}"
        return await client.send_video(
            message.chat.id, video=results, caption=f"Dán bau si {rpk} WIBU NEVER DIEEEEEE"
        )
    except Exception:
        await message.reply_text("Có gì đó không ổn LOL...")


@Client.on_message(command(["chika", f"chika@{bu}"]))
async def chika(client, message):
    message.from_user.id
    message.from_user.first_name
    message.from_user.id
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/chika").json()
        results = f"{resp['url']}"
        return await client.send_video(
            message.chat.id, video=results, caption=f"Chika xinh đẹp {rpk}"
        )
    except Exception:
        await message.reply_text("Có gì đó không ổn LOL...")


@Client.on_message(command(["truth", f"truth@{bu}"]))
async def truth(client, message):
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/truth").json()
        results = f"{resp['message']}"
        return await message.reply_text(results)
    except Exception:
        await message.reply_text("Có gì đó không ổn LOL...")


@Client.on_message(command(["dare", f"dare@{bu}"]))
async def dare(client, message):
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/dare").json()
        results = f"{resp['message']}"
        return await message.reply_text(results)
    except Exception:
        await message.reply_text("Có gì đó không ổn LOL...")


@Client.on_message(command(["lyrics", f"lyrics@{bu}"]))
async def lirik(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("**Đang tìm gì?**")
            return
        query = message.text.split(None, 1)[1]
        rep = await message.reply_text("🔎 **Tìm kiếm lời bài hát**")
        resp = requests.get(
            f"https://tede-api.herokuapp.com/api/lirik?l={query}"
        ).json()
        result = f"{resp['data']}"
        await rep.edit(result)
    except Exception:
        await rep.edit(
            "**Lời bài hát không tìm thấy.** Hãy thử tìm kiếm với tên bài hát rõ ràng hơn"
        )
