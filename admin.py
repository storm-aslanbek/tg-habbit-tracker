from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import keyboards as kb

router = Router()

@router.message(F.text == 'Мои студенты')
async def my_students(message: Message):
    await message.answer('Выберите студента',
                         reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [
                KeyboardButton('Асланбек'),
            ]
        ]))

@router.message(F.text == 'Асланбек')
async def aslanbek_admin(message: Message):
    await message.answer('Выберите действие которое вы хотите выполнить для студента',
                         reply_markup=kb.admin_main_students)