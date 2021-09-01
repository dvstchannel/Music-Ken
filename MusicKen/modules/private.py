import logging

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from MusicKen.config import (
    BOT_USERNAME,
    KENKAN,
    OWNER,
    PROJECT_NAME,
    SOURCE_CODE,
    SUPPORT_GROUP,
    UPDATES_CHANNEL,
)
from MusicKen.helpers.decorators import authorized_users_only
from MusicKen.modules.msg import Messages as tr

logging.basicConfig(level=logging.INFO)


@Client.on_message(filters.command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_sticker(
        "CAACAgUAAxkBAAFF-KFg-jaEvlhu_kNknYQjxsuyDvp--AACjAMAAtpWSVeocCICILIfRSAE"
    )
    await message.reply_text(
        f"""👋🏻 Xin chao tên tôi [{PROJECT_NAME}](https://telegra.ph/file/ed136c19e7f6afddb4912.jpg)
Dikekolah oleh {OWNER}
・✦▭▭▭▭✧◦✦◦✧▭▭▭▭✦ ・
☑️ Tôi có nhiều tính năng dành cho những bạn thích bài hát
🔘 Phát các bài hát trong nhóm
🔘 Đang phát các bài hát trên kênh
🔘 Tải xuống các bài hát
🔘 Tìm kiếm liên kết youtube
・✦▭▭▭▭✧◦✦◦✧▭▭▭▭✦ ・
☑️ Nhấp vào nút trợ giúp để biết thêm thông tin
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⚔️ Xem tiếp", callback_data=f"help+1"),
                    InlineKeyboardButton(
                        "Dùng chua bot ngay ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "💵 Hướng dẫn sử dụng", url="https://www.owohub.cf"
                    ),
                ],
            ]
        ),
        reply_to_message_id=message.message_id,
    )


@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
    await message.reply_photo(
        photo=f"{KENKAN}",
        caption=f"""**🔴 {PROJECT_NAME} is online**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="🔵 TÁC GIẢ", url=f"t.me/{OWNER}")],
                [
                    InlineKeyboardButton("🌟 TRỢ LÝ 🌟", url=f"{SOURCE_CODE}"),
                    InlineKeyboardButton(
                        "💵 XEM HƯỚNG DẪN", url="https://"
                    ),
                ],
            ]
        ),
    )


@Client.on_message(filters.private & filters.incoming & filters.command(["help"]))
def _help(client, message):
    client.send_message(
        chat_id=message.chat.id,
        text=tr.HELP_MSG[1],
        parse_mode="markdown",
        disable_web_page_preview=True,
        disable_notification=True,
        reply_markup=InlineKeyboardMarkup(map(1)),
        reply_to_message_id=message.message_id,
    )


help_callback_filter = filters.create(
    lambda _, __, query: query.data.startswith("help+")
)


@Client.on_callback_query(help_callback_filter)
def help_answer(client, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    msg = int(callback_query.data.split("+")[1])
    client.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=tr.HELP_MSG[msg],
        reply_markup=InlineKeyboardMarkup(map(msg)),
    )


def map(pos):
    if pos == 1:
        button = [
            [
                InlineKeyboardButton(text="⬅️ Sebelummya", callback_data="help+5"),
                InlineKeyboardButton(text="Selanjutnya ➡️", callback_data="help+2"),
            ]
        ]
    elif pos == len(tr.HELP_MSG) - 1:
        url = f"https://t.me/{SUPPORT_GROUP}"
        button = [
            [
                InlineKeyboardButton(text="⚔️ ʙᴀɴᴛᴜᴀɴ", callback_data=f"help+1"),
                InlineKeyboardButton(
                    text="DÙNG CHÙA NGAY ➕",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="👥 TÁC GIẢ", url=f"https://t.me/{OWNER}"
                ),
                InlineKeyboardButton(
                    text="🌟 TRỢ LÝ 🌟", url=f"https://t.me/{SOURCE_CODE}"
                ),
            ],
            [
                InlineKeyboardButton("🌟 TRỢ LÝ 🌟", url=f"{SOURCE_CODE}"),
                InlineKeyboardButton(
                    "💵 DONATE ĐI", url="https://tra"
                ),
            ],
        ]
    else:
        button = [
            [
                InlineKeyboardButton(
                    text="⬅️ Quay lại", callback_data=f"help+{pos-1}"
                ),
                InlineKeyboardButton(
                    text="Xem tiếp ➡️", callback_data=f"help+{pos+1}"
                ),
            ],
        ]
    return button


@Client.on_message(filters.command("reload") & filters.group & ~filters.edited)
@authorized_users_only
async def admincache(client, message: Message):
    await message.reply_photo(
        photo=f"{KENKAN}",
        caption="✅ **Bot đã khởi động lại thành công!**\n\n **Danh sách quản trị viên đã được cập nhật**",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="🔵 TÁC GIẢ", url=f"t.me/{OWNER}")],
                [
                    InlineKeyboardButton("🌟 TRỢ LÝ 🌟", url=f"{SOURCE_CODE}"),
                    InlineKeyboardButton(
                        "💵 ĐỌC HDSD TRƯỚC KHI DÙNG", url="https://t"
                    ),
                ],
            ]
        ),
    )


@Client.on_message(filters.command("help") & ~filters.private & ~filters.channel)
async def ghelp(_, message: Message):
    await message.reply_text(
        """
**🔰 DÙNG CHÙA THÌ TỰ MÒ LỆNH ĐI CHA 🔰**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="🔵 Tác giả", url=f"t.me/{OWNER}")],
                [
                    InlineKeyboardButton(
                        text="👥 Trợ lý", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton(
                        text="HDSD 📣", url=f"{SOURCE_CODE}"
                    ),
                ],
            ]
        ),
    )
