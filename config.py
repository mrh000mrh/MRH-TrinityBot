# config.py - این فایل در گیت‌هاب میمونه
import os
import sqlite3

class Config:
    # تنظیمات پایه
    DATABASE_NAME = "database.db"
    ADMIN_ID = None  # بعداً در پنل مدیریت تنظیم میشه
    
    # تنظیمات پیشفرض - بعداً در پنل مدیریت پر میشن
    BOT_TOKEN = None
    LAQIRA_API_KEY = None
    LAQIRA_SECRET_KEY = None
    
    @classmethod
    def init_db(cls):
        """ایجاد جداول تنظیمات در دیتابیس"""
        conn = sqlite3.connect(cls.DATABASE_NAME)
        c = conn.cursor()
        
        # جدول تنظیمات ربات
        c.execute('''CREATE TABLE IF NOT EXISTS bot_settings
                    (key TEXT PRIMARY KEY, value TEXT)''')
        
        # جدول درگاه‌های پرداخت
        c.execute('''CREATE TABLE IF NOT EXISTS payment_gateways
                    (id INTEGER PRIMARY KEY, name TEXT, api_key TEXT, 
                     secret_key TEXT, is_active BOOLEAN)''')
        
        conn.commit()
        conn.close()
