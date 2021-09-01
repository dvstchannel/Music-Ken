import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from MusicKen.config import SUDO_USERS
from MusicKen.helpers.filters import command
from MusicKen.services.callsmusic.callsmusic import client as USER


@Client.on_message(command("gs") & filters.user(SUDO_USERS) & ~filters.edited)
async def gcast(_, message: Message):
    sent = 0
    failed = 0
    if message.from_user.id not in SUDO_USERS:
        return
    wtf = await message.reply("Gửi tin nhắn toàn cầu...")
    if not message.reply_to_message:
        await wtf.edit("Trả lời bất kỳ tin nhắn văn bản nào cho gcast")
        return
    lmao = message.reply_to_message.text
    async for dialog in USER.iter_dialogs():
        try:
            await USER.send_message(dialog.chat.id, lmao)
            sent = sent + 1
            await wtf.edit(
                f"`Gửi tin nhắn toàn cầu` \n\n**Gửi đến:** `{sent}` chat \n**Không gửi được tới: ** {failed} chat"
            )
            await asyncio.sleep(0.7)
        except:
            failed = failed + 1
            await wtf.edit(
                f"`Gửi tin nhắn toàn cầu` \n\n**Gửi đến:** `{sent}` Chats \n**Không gửi được tới:** {failed} Chats"
            )
            await asyncio.sleep(0.7)

    return await wtf.edit(
        f"`Thông báo toàn cầu đã hoàn tất` \n\n**Gửi đến:** `{sent}` Chats \n**Không gửi được tới** {failed} Chats"
    )
