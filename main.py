# در main.py - بعد از importها
from settings_manager import SettingsManager

# دستورات مدیریتی
@bot.message_handler(commands=['setup'])
def setup_bot(message):
    """پنل تنظیمات اولیه"""
    if message.from_user.id != ADMIN_ID:  # ADMIN_ID رو دستی تنظیم کنید
        return
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('⚙️ تنظیم توکن ربات', '💰 اضافه کردن درگاه پرداخت')
    markup.row('📊 مشاهده تنظیمات', '🔙 بازگشت')
    
    bot.send_message(message.chat.id, 
                    "🔧 **پنل مدیریت تنظیمات**\n\n"
                    "از اینجا می‌تونید تنظیمات رو انجام بدید:",
                    reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '⚙️ تنظیم توکن ربات')
def set_bot_token(message):
    """تنظیم توکن ربات"""
    msg = bot.send_message(message.chat.id, 
                          "لطفاً توکن ربات رو ارسال کنید:\n"
                          "مثال: 8001396064:AAGWDRn9uDK_t--eG0POnDiFamThRjN628k")
    bot.register_next_step_handler(msg, process_bot_token)

def process_bot_token(message):
    """پردازش توکن دریافتی"""
    token = message.text.strip()
    settings = SettingsManager()
    settings.set_setting('bot_token', token)
    settings.close()
    
    bot.send_message(message.chat.id, 
                    "✅ توکن ربات با موفقیت ذخیره شد!\n"
                    "ربات رو restart کنید.")

@bot.message_handler(func=lambda message: message.text == '💰 اضافه کردن درگاه پرداخت')
def add_payment_gateway(message):
    """منوی اضافه کردن درگاه پرداخت"""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🔵 Laqira Protocol', '🔴 زرین‌پال')
    markup.row('🟢 نکست پی', '🟡 ایدی پی')
    markup.row('🔙 بازگشت')
    
    bot.send_message(message.chat.id,
                    "🎯 **انتخاب درگاه پرداخت**\n\n"
                    "کدوم درگاه رو می‌خواید اضافه کنید؟",
                    reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🔵 Laqira Protocol')
def setup_laqira(message):
    """تنظیمات Laqira"""
    msg = bot.send_message(message.chat.id,
                          "🔵 **تنظیمات Laqira Protocol**\n\n"
                          "لطفاً API Key رو ارسال کنید:")
    bot.register_next_step_handler(msg, process_laqira_api)

def process_laqira_api(message):
    api_key = message.text.strip()
    msg = bot.send_message(message.chat.id, "لطفاً Secret Key رو ارسال کنید:")
    bot.register_next_step_handler(msg, process_laqira_secret, api_key)

def process_laqira_secret(message, api_key):
    secret_key = message.text.strip()
    
    settings = SettingsManager()
    settings.add_payment_gateway('Laqira', api_key, secret_key)
    settings.close()
    
    bot.send_message(message.chat.id,
                    "✅ درگاه Laqira با موفقیت اضافه شد!\n\n"
                    "میتونید از دستور /pay برای تست استفاده کنید.")
