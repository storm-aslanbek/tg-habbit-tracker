import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import keyboards as kb
from db import Client

import config

router = Router()
client = Client()

class FormStates(StatesGroup):
    _id = State()
    name = State()
    age = State()
    gender = State()


@router.message(CommandStart())
async def start_message(message: Message, state: FSMContext):
    await state.set_state(FormStates._id)
    await state.update_data(_id=message.from_user.id)

    await state.set_state(FormStates.name)
    await message.answer('Здравствуйте! Ваше имя?')

@router.message(FormStates.name, F.text)
async def name_form(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FormStates.age)
    await message.answer(f'Приятно было познакомится {message.text}, Мне нужно знать ваш возраст')

@router.message(FormStates.age, F.text)
async def age_form(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(FormStates.gender)
    await message.answer(f'Ваш пол?', reply_markup=kb.gender_main)

@router.callback_query(FormStates.gender, F.data)
async def gender_form(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == 'male':
        await state.update_data(gender='Мужской')
    elif callback.data == 'female':
        await state.update_data(gender='Женский')

    data = await state.get_data()
    client.insert(data)
    await callback.message.answer(f'Ваши данные: \nid: {data["_id"]} \nИмя: {data["name"]} \nВозраст: {data["age"]} \nПол: {data["gender"]}')

    await callback.message.answer('Данные добавлены.', reply_markup=kb.move_main)

    await state.clear()

@router.message(F.text == 'Задания')
async def add_task(message: Message):
    await message.reply('Выберите тип задания', reply_markup=kb.task_types)


@router.message(F.text == 'В главное')
async def cancel(message: Message):
    await message.answer('Выберите действие', reply_markup=kb.move_main)

# @router.message(F.text)
# async def unfamiliar_text(message: Message):
#     await message.reply('Я вас не понимаю')