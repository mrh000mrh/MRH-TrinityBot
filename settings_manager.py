# settings_manager.py
import sqlite3
from config import Config

class SettingsManager:
    def __init__(self):
        self.conn = sqlite3.connect(Config.DATABASE_NAME)
    
    def set_setting(self, key, value):
        """ذخیره تنظیمات در دیتابیس"""
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO bot_settings (key, value) VALUES (?, ?)", 
                 (key, value))
        self.conn.commit()
    
    def get_setting(self, key, default=None):
        """خواندن تنظیمات از دیتابیس"""
        c = self.conn.cursor()
        c.execute("SELECT value FROM bot_settings WHERE key = ?", (key,))
        result = c.fetchone()
        return result[0] if result else default
    
    def add_payment_gateway(self, name, api_key, secret_key):
        """اضافه کردن درگاه پرداخت جدید"""
        c = self.conn.cursor()
        c.execute('''INSERT INTO payment_gateways 
                    (name, api_key, secret_key, is_active) 
                    VALUES (?, ?, ?, ?)''', 
                 (name, api_key, secret_key, True))
        self.conn.commit()
    
    def close(self):
        self.conn.close()
