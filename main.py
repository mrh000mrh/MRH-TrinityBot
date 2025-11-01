# main.py
import telebot
import sqlite3
import logging
from config import BOT_TOKEN

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN)

def init_db():
    """ایجاد دیتابیس و جداول"""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, username TEXT, balance INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, name TEXT, price INTEGER)''')
    
    conn.commit()
    conn.close()

def main_menu():
    """منوی اصلی"""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🛍 خرید', '👤 پنل کاربری')
    markup.row('💬 پشتیبانی', 'ℹ️ راهنما')
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """دستور شروع"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    # ذخیره کاربر در دیتابیس
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, balance) VALUES (?, ?, ?)", 
              (user_id, username, 0))
    conn.commit()
    conn.close()
    
    bot.send_message(message.chat.id, 
                    f"سلام {username}!\nبه ربات فروش کانفیگ خوش آمدید 🌸",
                    reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    """مدیریت پیام‌ها"""
    if message.text == '🛍 خرید':
        bot.send_message(message.chat.id, "بخش خرید به زودی فعال می‌شود...")
    elif message.text == '👤 پنل کاربری':
        bot.send_message(message.chat.id, "پنل کاربری در حال توسعه...")
    else:
        bot.send_message(message.chat.id, "دستور نامعتبر!")

if __name__ == "__main__":
    init_db()
    print("✅ ربات با موفقیت راه‌اندازی شد!")
    print("🤖 در حال اجرا...")
    bot.polling()
