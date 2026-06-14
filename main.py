import os
import telebot
from flask import Flask
from threading import Thread

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Sử dụng một từ điển để lưu trữ thành viên theo từng nhóm (chat_id)
# Lưu ý: Vì dùng biến này, nếu Render khởi động lại, danh sách sẽ mất.
# Để lưu vĩnh viễn, bạn cần dùng database, nhưng với nhóm nhỏ, cách này là đủ.
members_db = {}

@bot.message_handler(func=lambda message: True)
def collect_members(message):
    chat_id = message.chat.id
    user = message.from_user
    
    # Bỏ qua nếu là bot
    if user.is_bot:
        return
    
    # Tạo danh sách cho nhóm nếu chưa có
    if chat_id not in members_db:
        members_db[chat_id] = {}
    
    # Lưu ID và tên của thành viên vào database tạm
    members_db[chat_id][user.id] = user.first_name
    
    # Xử lý lệnh tagall
    if message.text and message.text.startswith('/tagall'):
        tag_all(message)

def tag_all(message):
    chat_id = message.chat.id
    if chat_id not in members_db or not members_db[chat_id]:
        bot.reply_to(message, "Chưa có ai nhắn tin trong nhóm để mình lưu lại!")
        return
    
    mention_text = "📢 **Thông báo đến các thành viên đã hoạt động:**\n\n"
    for user_id, name in members_db[chat_id].items():
        mention_text += f"[{name}](tg://user?id={user_id}) "
    
    bot.send_message(chat_id, mention_text, parse_mode='Markdown')

# Web server để giữ Render luôn thức
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
