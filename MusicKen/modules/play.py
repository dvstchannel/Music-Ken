import os
from os import path
from typing import Callable

import aiofiles
import aiohttp
import ffmpeg
import requests
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch

from MusicKen.config import ARQ_API_KEY, DURATION_LIMIT, KENKAN, SUPPORT_GROUP
from MusicKen.config import UPDATES_CHANNEL as updateschannel
from MusicKen.config import que
from MusicKen.function.admins import admins as a
from MusicKen.helpers.admins import get_administrators
from MusicKen.helpers.channelmusic import get_chat_id
from MusicKen.helpers.decorators import authorized_users_only, errors
from MusicKen.helpers.errors import DurationLimitError
from MusicKen.helpers.filters import command, other_filters
from MusicKen.helpers.gets import get_file_name, get_url
from MusicKen.services.callsmusic import callsmusic, queues
from MusicKen.services.callsmusic.callsmusic import client as USER
from MusicKen.services.converter.converter import convert
from MusicKen.services.downloaders import youtube

aiohttpsession = aiohttp.ClientSession()
chat_id = None
arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)

useer = "Musik"


def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        else:
            await cb.answer("Bạn không được phép!", show_alert=True)
            return

    return decorator


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("./etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((30, 550), f"{title}", (255, 215, 0), font=font)
    draw.text((30, 590), f"{duration}", (255, 215, 0), font=font)
    draw.text((30, 630), f"{views}", (255, 215, 0), font=font)
    draw.text(
        (30, 670),
        f"Permintaan : {requested_by}",
        (255, 215, 0),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(filters.command("playlist") & filters.group & ~filters.edited)
async def playlist(client, message):
    global que
    queue = que.get(message.chat.id)
    if not queue:
        await message.reply_text("Người chơi không hoạt động")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "**Bài hát hiện tại** di {}".format(message.chat.title)
    msg += "\n• " + now_playing
    msg += "\n• Yêu cầu bởi " + by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "**Hàng đợi bài hát**"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n• {name}"
            msg += f"\n• Yều cầu bởi {usr}\n"
    await message.reply_text(
        msg,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📖 Danh sách", callback_data="playlist"),
                    InlineKeyboardButton(text="🗑 Đóng", callback_data="cls")]
            ]
        ),
    )


# ============================= Settings =========================================


def updated_stats(chat, queue, vol=150):
    if chat.id in callsmusic.pytgcalls.active_calls:
        # if chat.id in active_chats:
        stats = "Pengaturan dari **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "Volume : {}%\n".format(vol)
            stats += "Bài hát trong hàng đợi: `{}`\n".format(len(que))
            stats += "Hiện đang phát một bài hát: **{}**\n".format(queue[0][0])
            stats += "Được yêu cầu bởi: {}".format(queue[0][1].mention)
    else:
        stats = None
    return stats


@Client.on_message(filters.command("current") & filters.group & ~filters.edited)
async def ee(client, message):
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        await message.reply(stats)
    else:
        await message.reply("**Vui lòng mở voice call ở nhóm trước trước!**")


@Client.on_message(filters.command("player") & filters.group & ~filters.edited)
@authorized_users_only
async def settings(client, message):
    playing = None
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        playing = True
    queue = que.get(chat_id)
    stats = updated_stats(message.chat, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))

        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply("**Vui lòng mở voice call ở nhóm trước trước!**")


@Client.on_callback_query(filters.regex(pattern=r"^(playlist)$"))
async def p_cb(b, cb):
    global que
    que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("**Không phát một bài hát**")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Bài hát hiện tại** di {}".format(cb.message.chat.title)
        msg += "\n• " + now_playing
        msg += "\n• Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Antrian Lagu**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n• {name}"
                msg += f"\n• Yêu cầu bởi {usr}\n"
        await cb.message.edit(
            msg,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton("📖 Danh sách", callback_data="playlist"),
                    InlineKeyboardButton(text="🗑 Đóng", callback_data="cls")]
            ]
                ]
            ),
        )


@Client.on_callback_query(
    filters.regex(pattern=r"^(play|pause|skip|leave|puse|resume|menu|cls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que
    if (
        cb.message.chat.title.startswith("Channel Music: ")
        and chat.title[14:].isnumeric()
    ):
        chet_id = int(chat.title[13:])
    else:
        chet_id = cb.message.chat.id
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "pause":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("Trò chuyện không được kết nối!", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("Nhạc đã tạm dừng!")
            await cb.message.edit(
                updated_stats(m_chat, qeue), reply_markup=r_ply("play")
            )

    elif type_ == "play":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("Trò chuyện không được kết nối!", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("Âm nhạc tiếp tục!")
            await cb.message.edit(
                updated_stats(m_chat, qeue), reply_markup=r_ply("pause")
            )

    elif type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("Người chơi không hoạt động")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Đang chơi** in {}".format(cb.message.chat.title)
        msg += "\n- " + now_playing
        msg += "\n- Yêu cầu bởi " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Xếp hàng**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n- Yêu cầu bởi {usr}\n"
        await cb.message.edit(msg)

    elif type_ == "resume":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("Trò chuyện chưa được kết nối hoặc đã chơi", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("Âm nhạc tiếp tục!")
    elif type_ == "puse":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("Trò chuyện chưa được kết nối hoặc đã bị tạm dừng", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("Nhạc đã tạm dừng!")
    elif type_ == "cls":
        await cb.answer("Menu đã đóng")
        await cb.message.delete()

    elif type_ == "skip":
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer("Trò chuyện không được kết nối!", show_alert=True)
        else:
            callsmusic.queues.task_done(chet_id)

            if callsmusic.queues.is_empty(chet_id):
                callsmusic.pytgcalls.leave_group_call(chet_id)

                await cb.message.edit("- Không có thêm danh sách phát..\n- Leaving VC!")
            else:
                callsmusic.pytgcalls.change_stream(
                    chet_id, callsmusic.queues.get(chet_id)["file"]
                )
                await cb.answer("Skipped")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(
                    f"- Bài hát bị bỏ qua\n- Đang chơi**{qeue[0][0]}**"
                )

    else:
        if chet_id in callsmusic.pytgcalls.active_calls:
            try:
                callsmusic.queues.clear(chet_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chet_id)
            await cb.message.edit("Successfully Left the Chat!")
        else:
            await cb.answer("Chat is not connected!", show_alert=True)


@Client.on_message(command(["ytplay", "yt", "p"]) & other_filters)
@errors
async def play(_, message: Message):
    global que
    lel = await message.reply("🔄 **Đang xử lý bài hát**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "<b>Nhớ thêm bot Trợ lý vào Kênh của bạn</b>",
                    )
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>Trước tiên hãy thêm tôi làm quản trị viên nhóm của bạn</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await lel.edit(
                        "<b>Trợ lý Bot đã tham gia thành công vào nhóm của bạn</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>⛑ Flood Wait Error ⛑\n{user.first_name} không thể tham gia nhóm của bạn do có nhiều yêu cầu tham gia cho userbot! Đảm bảo rằng người dùng không bị cấm trong nhóm."
                        "\n\nHoặc thêm Trợ lý Bot theo cách thủ công vào Nhóm của bạn và thử lại</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i> {user.first_name} đã bị cấm khỏi nhóm này, hãy yêu cầu quản trị viên bỏ cấm bot trợ lý sau đó thêm Bot trợ lý theo cách thủ công.</i>"
        )
        return
    message.from_user.id
    message.from_user.first_name
    text_links = None
    await lel.edit("🔎 **Tìm kiếm bài hát**")
    message.from_user.id
    if message.reply_to_message:
        entities = []
        toxt = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.entities:
            entities = message.reply_to_message.entities + entities
        elif message.reply_to_message.caption_entities:
            entities = message.reply_to_message.entities + entities
        urls = [entity for entity in entities if entity.type == "url"]
        text_links = [entity for entity in entities if entity.type == "text_link"]
    else:
        urls = None
    if text_links:
        urls = True
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ **Video có thời lượng hơn** `{DURATION_LIMIT}` **phút không thể chơi!**"
            )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📖 Danh sách", callback_data="playlist"),
                    InlineKeyboardButton(text="🗑 Đóng", callback_data="cls")]
            ]
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "http://fc04.deviantart.net/fs70/i/2010/205/7/d/owo_wallpaper_by_Thundervalley.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Đã thêm cục bộ"
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("🎵 **Đang xử lý bài hát**")
        ydl_opts = {"format": "141/bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "**Bài hát không được tìm thấy.** Coba cari dengan judul lagu yang lebih jelas, Ketik `/help` bila butuh bantuan"
            )
            print(str(e))
            return
        dlurl = url
        dlurl = dlurl.replace("youtube", "youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📖 ᴘʟᴀʏʟɪꜱᴛ", callback_data="playlist"),
                ],
                [
                    InlineKeyboardButton(
                        "💵 XEM HDSD", url="https://"
                    ),
                ],
                [InlineKeyboardButton(text="🗑 ĐÓNG", callback_data="cls")],
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        await lel.edit("🎵 **Đang xử lý bài hát**")
        ydl_opts = {"format": "141/bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "**Bài hát không được tìm thấy.** Hãy thử tìm kiếm với tên bài hát rõ ràng hơn!"
            )
            print(str(e))
            return
        dlurl = url
        dlurl = dlurl.replace("youtube", "youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📖 ᴘʟᴀʏʟɪꜱᴛ", callback_data="playlist"),
                ],
                [
                    InlineKeyboardButton(
                        "💵 XEM HDSD", url="https://"
                    ),
                ],
                [InlineKeyboardButton(text="🗑 ĐÓNG callback_data="cls")],
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"[{title[:60]}]({url})\n**⏱ Thời lượng :** {duration}\n"
            + f"🔇 **Antri :** {position}!\n🎧 **Permintaan :** {requested_by}",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        except:
            message.reply("Nhóm trò chuyện thoại không hoạt động, tôi không thể tham gia")
            return
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"🏷 **Tiêu đề:** [{title[:60]}]({url})\n⏱ **Durasi:** {duration}\n🔊 **Tình trạng:** Đang phát\n"
            + f"🎧 **Yêu cầu nhạc:** {message.from_user.mention}",
        )
        return await lel.delete()
        os.remove("final.png")


@Client.on_message(command("lplay") & other_filters)
@errors
async def stream(_, message: Message):

    lel = await message.reply("🔁 **Chế biến** cục cứt chiên bơ...")
    message.from_user.id
    message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
        [
                [
                    InlineKeyboardButton("📖 Danh sách", callback_data="playlist"),
                    InlineKeyboardButton(text="🗑 Đóng", callback_data="cls")]
            ]
        ]
    )

    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Vượt quá {DURATION_LIMIT} phút không được phép chơi!"
            )

        file_name = get_file_name(audio)
        file_path = await convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif url:
        file_path = await convert(youtube.download(url))
    else:
        return await lel.edit_text("❗ Làm ơn cho tôi một bài hát để chơi!")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo=f"{KENKAN}",
            caption=f"🔊 **Bài hát bạn yêu cầu đang Xếp hàng vào vị trí** `{position}`",
            reply_markup=keyboard,
        )
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
            photo=f"{KENKAN}",
            reply_markup=keyboard,
            caption="🎧 **Đang phát bài hát yêu cầu:** {}!".format(
                message.from_user.mention()
            ),
        )
        return await lel.delete()


# Have u read all. If read RESPECT :-)
