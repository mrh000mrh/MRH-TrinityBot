# main.py
import telebot
import sqlite3
import logging
from config import Config, setup_admin
from settings_manager import SettingsManager

# ابتدا دیتابیس رو initialize میکنیم
Config.init_db()

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ایجاد ربات - توکن موقت
bot = telebot.TeleBot("temp_token")

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
    conn = sqlite3.connect(Config.DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, balance) VALUES (?, ?, ?)", 
              (user_id, username, 0))
    conn.commit()
    conn.close()
    
    bot.send_message(message.chat.id, 
                    f"سلام {username}!\nبه ربات فروش کانفیگ خوش آمدید 🌸",
                    reply_markup=main_menu())

@bot.message_handler(commands=['setup'])
def setup_bot(message):
    """پنل تنظیمات اولیه"""
    # فعلاً دسترسی به همه میدهیم - بعداً محدود میکنیم
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('⚙️ تنظیم توکن ربات', '💰 اضافه کردن درگاه پرداخت')
    markup.row('🔧 تنظیم ادمین اصلی', '📊 مشاهده تنظیمات')
    
    bot.send_message(message.chat.id, 
                    "🔧 **پنل مدیریت تنظیمات**\n\n"
                    "از اینجا می‌تونید تنظیمات رو انجام بدید:",
                    reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🔧 تنظیم ادمین اصلی')
def set_main_admin(message):
    """تنظیم ادمین اصلی"""
    admin_id = message.from_user.id
    setup_admin(admin_id)
    bot.send_message(message.chat.id, 
                    f"✅ شما به عنوان ادمین اصلی تنظیم شدید!\n"
                    f"آی‌دی شما: {admin_id}")

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
    print("✅ ربات با موفقیت راه‌اندازی شد!")
    print("🤖 برای تنظیمات اولیه از دستور /setup استفاده کنید")
    bot.polling()
