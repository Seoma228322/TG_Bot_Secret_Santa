from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def start_button():
    kb = [
        [KeyboardButton(text="Начать")]
    ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def gift_sent_button():
    kb = [
        [KeyboardButton(text="Подарил подарок")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def admin_menu():
    kb = [
        [KeyboardButton(text="Начать жеребьевку")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
