from asyncio.queues import QueueEmpty

from pyrogram import Client, filters
from pyrogram.types import Message

from MusicKen.function.admins import set
from MusicKen.services.callsmusic import callsmusic


@Client.on_message(
    filters.command(["channelpause", "cpause"]) & filters.group & ~filters.edited
)
async def pause(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**Trò chuyện có được kết nối không?**")
        return
    chat_id = chid
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❗ **Không có gì đang chơi!**")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("▶️ **Bị tạm dừng!**")


@Client.on_message(
    filters.command(["channelresume", "cresume"]) & filters.group & ~filters.edited
)
async def resume(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**Cuộc trò chuyện có được kết nối không?**")
        return
    chat_id = chid
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❗ **Không có bài hát!**")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("⏸ **Tiếp tục!**")


@Client.on_message(
    filters.command(["channelend", "cend"]) & filters.group & ~filters.edited
)
async def stop(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**Trò chuyện có được kết nối không?**")
        return
    chat_id = chid
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ **Không có bài hát!**")
    else:
        try:
            callsmusic.queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("❌ **Dừng bài hát!**")


@Client.on_message(
    filters.command(["channelskip", "cskip"]) & filters.group & ~filters.edited
)
async def skip(_, message: Message):
    global que
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**Cuộc trò chuyện có được kết nối không?**")
        return
    chat_id = chid
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ **Không có bài hát tiếp theo nào để bỏ qua!**")
    else:
        callsmusic.queues.task_done(chat_id)

        if callsmusic.queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, callsmusic.queues.get(chat_id)["file"]
            )

        await message.reply_text("⏩ **Bỏ qua bài hát hiện tại!**")


@Client.on_message(filters.command("channeladmincache"))
async def admincache(client, message: Message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**Trò chuyện có được kết nối không?**")
        return
    set(
        chid,
        [
            member.user
            for member in await conchat.linked_chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("✅️ **Danh sách quản trị viên** đã **được làm mới**")
