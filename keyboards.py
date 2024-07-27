from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

cancel_main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Назад')
    ]
])

admin_main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Мои студенты'),
        KeyboardButton(text='Рассылать задание'),
    ]
])

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

admin_main_students = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Отправить задание'),
        KeyboardButton(text='Посмотреть достижения студента'),
        KeyboardButton(text='Посмотреть расписание для студента'),
        KeyboardButton(text='Изменить рассписание студента'),
    ]
])
