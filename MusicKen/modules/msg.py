from MusicKen.config import ASSISTANT_NAME, OWNER, PROJECT_NAME


class Messages:
    HELP_MSG = [
        ".",
        f"""
**👋🏻 Xin chào, Chào mừng trở lại [{PROJECT_NAME}](https://telegra.ph/file/ed136c19e7f6afddb4912.jpg)

⚪️ {PROJECT_NAME} có thể phát nhạc trong nhóm của bạn Trò chuyện thoại cũng như Trò chuyện thoại trên kênh

⚪️ Assistant Name >> @{ASSISTANT_NAME}\n\n☑️ Nhấp vào Tiếp theo để biết thêm thông tin**
""",
        f"""
**🛠️ THỰC HIỆN TỪNG BƯỚC **

1) Thêm @{ASSISTANT_NAME} vào nhóm cần phát nhạc.
2) Set Admin cho Bot với quyền quản lý cuộc gọi thoại.
3) Mở voice chat lên và nhập lệnh /userbotjoin
• Nếu Assistant Bot tham gia vào nhóm bắt đầu oder âm nhạc,
• Nếu Trợ lý Bot không tham gia, vui lòng thêm @{ASSISTANT_NAME}

**Đối với kênh chơi nhạc 📣**

1) Đặt Bot làm quản trị viên kênh
2) Gửi /userbotjoinchannel trong nhóm được liên kết
3) Bây giờ gửi lệnh trong các nhóm được liên kết
""",
        """
**🔰 CÁCH ODER NHẠC**

**=>> Đang phát bài hát 🎧**

• /play (tên bài hát) - Để phát bài hát bạn yêu cầu qua youtube
• /ytplay (tên bài hát) - như trên
• /yt (tên bài hát) - như trên
• /p (tên bài hát) - như trên
• /lplay - Trả lời tệp âm thanh trên nhóm sẽ được tự động phát trên VCG
• /player: Chuyển đến menu Cài đặt trình phát
• /skip: Bỏ qua bản nhạc hiện tại
• /pause:  Tạm dừng
• /resume: Tiếp tục một bản nhạc đã tạm dừng
• /end: ​​ Dừng phát lại phương tiện
• /current: Hiển thị bản nhạc hiện đang phát
• /playlist: Hiển thị danh sách phát

Tất cả các lệnh đều có thể được sử dụng ngoại trừ các lệnh /player /skip /pause /resume /end tất cả các lệnh đều có thể được sử dụng ngoại trừ các lệnh

**==>>Tải bài hát 📥**

• /song [tên bài hát]: Tải xuống âm thanh bài hát từ youtube
""",
        f"""
**=>> Kênh chơi nhạc 🛠**

⚪️ Chỉ dành cho quản trị viên nhóm được liên kết:

• /cplay (nama lagu) - phát bài hát bạn yêu cầu
• /cplaylist - Hiển thị danh sách hiện đang chơi
• /cccurrent - Chương trình đang phát
• /cplayer - mở bảng cài đặt trình phát nhạc
• /cpause - tạm dừng phát lại bài hát
• /cresume - tiếp tục chơi bài hát
• /cskip - Phát bài hát tiếp theo
• /cend - dừng chơi nhạc
• /userbotjoinchannel - mời trợ lý vào cuộc trò chuyện của bạn

⚪️ Nếu bạn không thích chơi trong các nhóm được liên kết:

1) Nhận ID kênh của bạn.
2) Tạo nhóm với tiêu đề: Channel Music: #ID_KÊNH
3) Thêm Bot làm quản trị viên kênh với đầy đủ quyền
4) Thêm @{ASSISTANT_NAME} vào kênh với tư cách quản trị viên.
5) Chỉ cần gửi đơn hàng trong nhóm của bạn

**=>> Thêm công cụ 🧑‍🔧**

- /admincache: Cập nhật thông tin quản trị nhóm của bạn. Hãy thử nếu Bot không nhận ra quản trị viên
- /userbotjoin: Mời gọi @{ASSISTANT_NAME} trợ lý cho nhóm của bạn
""",
        f"""👋🏻 Xin chào tên tôi là [{PROJECT_NAME}](https://telegra.ph/file/ed136c19e7f6afddb4912.jpg)
Trường học bởi {OWNER}
・✦▭▭▭▭✧◦✦◦✧▭▭▭▭✦ ・
☑️ Tôi có nhiều tính năng dành cho những bạn thích bài hát
🔘 Phát các bài hát trong nhóm
🔘 Phát các bài hát trên kênh
🔘 Tải xuống các bài hát
🔘 Tìm kiếm liên kết youtube
・✦▭▭▭▭✧◦✦◦✧▭▭▭▭✦ ・
☑️ Nhấp vào nút trợ giúp để biết thêm thông tin
""",
    ]
