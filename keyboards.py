from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

move_main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Мои достижения'),
        KeyboardButton(text='Расписание'),
        KeyboardButton(text='Изменить данные'),
    ]
])


gender_main = InlineKeyboardMarkup(row_width = 2, inline_keyboard=[
    [
        InlineKeyboardButton(text='Мужской', callback_data='male'),
        InlineKeyboardButton(text='Женский', callback_data='female'),
    ]
])


