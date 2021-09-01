# Daisyxmusic (Telegram bot project )
# Copyright (C) 2021  Inukaasith

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import asyncio

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant

from MusicKen.config import SUDO_USERS
from MusicKen.helpers.decorators import authorized_users_only, errors
from MusicKen.services.callsmusic.callsmusic import client as USER


@Client.on_message(filters.command(["userbotjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Trước tiên hãy thêm tôi làm quản trị viên nhóm của bạn</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "MusicKen"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>{user.first_name} đã có trong cuộc trò chuyện của bạn</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>⛑ Flood Wait Error ⛑\n{user.first_name} không thể tham gia nhóm của bạn do có nhiều yêu cầu tham gia cho userbot! Đảm bảo rằng người dùng không bị cấm trong nhóm."
            "\n\nHoặc thêm bot Trợ lý theo cách thủ công vào Nhóm của bạn và thử lại.</b>",
        )
        return
    await message.reply_text(
        f"<b>{user.first_name} đã tham gia thành công cuộc trò chuyện của bạn</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b>Người dùng không thể rời khỏi nhóm của bạn! Có lẽ là chờ đợi lũ lụt."
            "\n\nHoặc xóa tôi khỏi Nhóm của bạn theo cách thủ công</b>",
        )
        return


@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left = 0
        failed = 0
        lol = await message.reply("**Trợ lý Để lại tất cả các cuộc trò chuyện**")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left + 1
                await lol.edit(
                    f"Trợ lý còn lại ... Đã thành công:{left} trò chuyện. Thất bại: {failed} trò chuyện."
                )
            except:
                failed = failed + 1
                await lol.edit(
                    f"Trợ lý còn lại ... Đã thành công: {left} trò chuyện. Thất bại: {failed} trò chuyện."
                )
            await asyncio.sleep(0.7)
        await client.send_message(
            message.chat.id, f"Thành công {left} trò chuyện. Thất bại {failed} trò chuyện."
        )


@Client.on_message(
    filters.command(["userbotjoinchannel", "ubjoinc"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("Trò chuyện có được kết nối không?")
        return
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Trước tiên hãy thêm tôi làm quản trị viên kênh của bạn</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "MusicKen"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>{user.first_name} đã có trên kênh của bạn</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>⛑ Flood Wait Error ⛑\n{user.first_name} không thể tham gia nhóm của bạn do có nhiều yêu cầu tham gia cho userbot! Đảm bảo rằng người dùng không bị cấm trong nhóm."
            "\n\nHoặc thêm bot Trợ lý theo cách thủ công vào Nhóm của bạn và thử lại.</b>",
        )
        return
    await message.reply_text(
        f"<b>{user.first_name} đã tham gia cuộc trò chuyện của bạn</b>",
    )
