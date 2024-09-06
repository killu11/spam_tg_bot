import enum
from aiogram import types

class Buttons(enum.Enum) :
    """Кнопки админа"""
    reboot_spam = types.InlineKeyboardButton(text = 'Перезапустить', callback_data= 'reboot_spam')
    stop_send_text = types.InlineKeyboardButton(text = 'Остановить рассылку', callback_data= 'stop')
    
    """Кнопки дефолт юзера"""
    info_about_creators = types.InlineKeyboardButton(text = 'Контакты', callback_data= 'contact')

