from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from db import Client

client = Client()

cancel_main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='В главное'),
    ]
])


move_main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Задания'),
        KeyboardButton(text='Изменить данные'),
        KeyboardButton(text='В главное'),
    ]
])


gender_main = InlineKeyboardMarkup(row_width = 2, inline_keyboard=[
    [
        InlineKeyboardButton(text='Мужской', callback_data='male'),
        InlineKeyboardButton(text='Женский', callback_data='female'),
    ]
])

task_types = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Ежедневная привычка'),
        KeyboardButton(text='Задачи по расписанию'),
        KeyboardButton(text='В главное'),
    ]
])

habit_main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Добавить привычку'),
        KeyboardButton(text='Таблица привычек'),
        KeyboardButton(text='Удалить привычку'),
        KeyboardButton(text='В главное'),
    ]
])

task_main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Добавить задачу'),
        KeyboardButton(text='Расписание'),
        KeyboardButton(text='Изменить статус задачи'),
        KeyboardButton(text='В главное'),
    ]
])

task_status_inline = InlineKeyboardMarkup(row_width = 2, inline_keyboard=[
    [
        InlineKeyboardButton(text='Не выполнено', callback_data='not_comleted'),
        InlineKeyboardButton(text='Выполняется', callback_data='in_progress'),
        InlineKeyboardButton(text='Выполнено', callback_data='completed'),
    ]
])

habit_list = []
habit_query = ()
for value in client.habit_collection.find(habit_query, {"_id": 0, "note": 1}):
    habit_list.append(value.get("note"))

async def del_habit_main():
    keyboard = ReplyKeyboardBuilder()
    for habit in habit_list:
        keyboard.add(KeyboardButton(text=habit))
    keyboard.add(KeyboardButton(text='В главное'))
    return keyboard.adjust(2).as_markup()

student_list = []
query = ()
for value in client.collection.find(query, {"_id": 0, "name": 1}):
    student_list.append(value.get("name"))


async def students_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for student in student_list:
        keyboard.add(KeyboardButton(text=student))
    keyboard.add(KeyboardButton(text='В главное'))
    return keyboard.adjust(2).as_markup()
