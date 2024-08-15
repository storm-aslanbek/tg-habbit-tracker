from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from db import Client

client = Client()

cancel_main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Назад')
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


admin_main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Мои студенты'),
        KeyboardButton(text='Рассылать задание'),
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

student_list = []
query = ()
for value in client.collection.find(query, {"_id": 0, "name": 1}):
    student_list.append(value.get("name"))

async def students_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for student in student_list:
        keyboard.add(KeyboardButton(text=student))
    return keyboard.adjust(2).as_markup()


if __name__ == '__main__':
    print(student_list)