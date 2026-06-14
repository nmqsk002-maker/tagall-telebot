import os
import telebot
from flask import Flask
from threading import Thread

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['tagall'])
def tag_all(message):
    chat_id = message.chat.id
    try:
        # Lấy danh sách thành viên (cần quyền Admin)
        members = bot.get_chat_administrators(chat_id)
        mention_text = "📢 Mọi người ơi: "
        for m in members:
            if not m.user.is_bot:
                mention_text += f"[{m.user.first_name}](tg://user?id={m.user.id}) "
        bot.send_message(chat_id, mention_text, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, "Bot cần quyền Admin để tag!")

# Tạo web server cho Render
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
