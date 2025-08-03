# helpers.py - ابزارهای کمکی پروژه شیپر فضوله

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

def extract_user_id_from_message(msg: types.Message):
    """
    استخراج آیدی عددی از پیام، شامل:
    - ریپلای
    - منشن
    - یوزرنیم با @
    - آیدی عددی مستقیم
    """
    if msg.reply_to_message:
        return msg.reply_to_message.from_user.id
    text = msg.text.strip()

    # بررسی وجود آیدی عددی
    id_match = re.findall(r"\b\d{6,12}\b", text)
    if id_match:
        return int(id_match[0])

    # بررسی منشن
    if msg.entities:
        for entity in msg.entities:
            if entity.type == "mention":
                mention = text[entity.offset:entity.offset + entity.length]
                return mention  # باید به کاربر resolve شود

    return None

def build_yes_no_keyboard(yes_callback: str, no_callback: str):
    """
    ساخت کیبورد برای سؤال‌های بله / خیر مثل: آیا بنده وکیلم؟
    """
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("✅ با اجازه بزرگترا", callback_data=yes_callback),
        InlineKeyboardButton("❌ متاسفم", callback_data=no_callback)
    )
    return kb

def build_back_keyboard(callback_data="back_to_menu"):
    """
    دکمه بازگشت به منوی اصلی
    """
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 بازگشت به منو", callback_data=callback_data))
    return kb

def mention_html(user: types.User):
    """
    تولید لینک منشن شده HTML با نام نمایشی کاربر
    """
    name = user.full_name.replace("<", "").replace(">", "")
    return f'<a href="tg://user?id={user.id}">{name}</a>'

def escape_html(text: str):
    """
    جلوگیری از خطای رندر HTML در تلگرام
    """
    return text.replace("<", "").replace(">", "")
